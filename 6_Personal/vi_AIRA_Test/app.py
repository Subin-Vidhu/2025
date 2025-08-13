import json, threading, time, os, smtplib, ssl, socket, tempfile, shutil, hashlib, secrets
from urllib.error import HTTPError, URLError
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen, Request
from email.message import EmailMessage
from datetime import datetime, timezone
from http.cookies import SimpleCookie

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'services.json')
STATUS_LOG = os.path.join(BASE_DIR, 'status_log.jsonl')
CHECK_INTERVAL_SEC = int(os.getenv('CHECK_INTERVAL_SEC', '60'))
NOTIFY_COOLDOWN_SEC = int(os.getenv('NOTIFY_COOLDOWN_SEC', '900'))
LOCK = threading.Lock()
LATENCY_HISTORY = {}
MAX_HISTORY = 20  # short ring for sparkline

# Authentication settings
SECRET_KEY = 'PROTOS25'  # This is now only on the server side
ACTIVE_SESSIONS = {}  # Store active session tokens


def generate_session_token():
    """Generate a secure session token."""
    return secrets.token_urlsafe(32)

def is_authenticated(request_handler):
    """Check if the request has valid authentication."""
    # Check for existing token-based auth (backwards compatibility)
    token = os.getenv('DASHBOARD_TOKEN')
    if token and request_handler.headers.get('X-Auth-Token') == token:
        return True
    
    # Check for session-based auth
    cookie_header = request_handler.headers.get('Cookie')
    if cookie_header:
        cookies = SimpleCookie()
        cookies.load(cookie_header)
        session_token = cookies.get('pacs_session')
        if session_token and session_token.value in ACTIVE_SESSIONS:
            # Check if session is still valid (24 hours)
            session_time = ACTIVE_SESSIONS[session_token.value]
            if time.time() - session_time < 24 * 3600:  # 24 hours
                return True
            else:
                # Session expired, remove it
                del ACTIVE_SESSIONS[session_token.value]
    
    return False

def authenticate_user(password):
    """Authenticate user with password and return session token."""
    if password == SECRET_KEY:
        session_token = generate_session_token()
        ACTIVE_SESSIONS[session_token] = time.time()
        return session_token
    return None

def load():
    """Load services list with corruption fallback."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            f.write('[]')
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        log('WARNING: services.json corrupted, creating backup and resetting list')
        # backup corrupted file
        ts = int(time.time())
        shutil.copyfile(DATA_FILE, f"{DATA_FILE}.bad.{ts}")
        with open(DATA_FILE, 'w') as f:
            f.write('[]')
        return []


def save(data):
    """Atomic save to reduce risk of partial writes."""
    fd, tmp_path = tempfile.mkstemp(prefix='svc_', suffix='.json', dir=BASE_DIR)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, DATA_FILE)
    except Exception:
        # best effort fallback
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            log('ERROR: failed to save services.json:', e)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


def utcnow():
    return datetime.now(timezone.utc).isoformat()


def log(*args):
    print('[monitor]', *args)


def check_service(svc):
    host = svc['host']
    port = svc.get('port')
    protocol = svc.get('protocol', 'https')
    target = f"{protocol}://{host}"
    if port and port not in (80, 443):
        target = f"{protocol}://{host}:{port}"
    path = svc.get('path', '/') or '/'
    url = target + path
    ok = False
    error = None
    http_code = None
    start = time.time()
    # Step 1: TCP connectivity
    try:
        with socket.create_connection((host, port or (443 if protocol == 'https' else 80)), timeout=10):
            pass
    except Exception as e:
        # Can't establish TCP so return immediately as DOWN
        error = f'tcp:{e.__class__.__name__}'
        return 'down', error, http_code, int((time.time() - start) * 1000)

    def attempt(fetch_unverified=False, use_head=True):
        method = 'HEAD' if use_head else 'GET'
        req = Request(url, method=method, headers={'User-Agent': 'PACSMonitor/1.0'})
        ctx = None
        if fetch_unverified:
            ctx = ssl._create_unverified_context()
        try:
            with urlopen(req, timeout=12, context=ctx) as r:
                return True, None, r.status
        except HTTPError as he:
            # Treat most <500 codes as service reachable (auth/403/404 still means service responding)
            if 200 <= he.code < 500:
                return True, None, he.code
            return False, f'http:{he.code}', he.code
        except ssl.SSLError as se:
            return False, f'ssl:{se.__class__.__name__}', None
        except Exception as e:
            return False, f'http:{e.__class__.__name__}', None

    # Try HEAD first (only if TCP succeeded)
    ok, error, code = attempt(use_head=True)
    if not ok and (error and error.startswith('http:')):
        ok, error, code = attempt(use_head=False)
    if not ok and error and error.startswith('ssl:'):
        ok, error2, code = attempt(fetch_unverified=True, use_head=False)
        if ok:
            error = 'ssl:unverified'
        elif error2:
            error = error2
    http_code = code
    latency_ms = int((time.time() - start) * 1000)
    return ('up' if ok else 'down'), error, http_code, latency_ms


def send_notifications(changed_svcs):
    if not changed_svcs:
        return
    lines = [f"{svc['name']} -> {svc['last_status'].upper()}" for svc in changed_svcs]
    body = 'Service status change:\n' + '\n'.join(lines)
    # Email
    smtp_host = os.getenv('SMTP_HOST')
    if smtp_host:
        msg = EmailMessage()
        msg['Subject'] = 'PACS Monitor Alert'
        msg['From'] = os.getenv('SMTP_FROM', os.getenv('SMTP_USER', 'monitor@example'))
        msg['To'] = os.getenv('ALERT_EMAIL', 'alerts@example')
        msg.set_content(body)
        try:
            ctx = ssl.create_default_context()
            port = int(os.getenv('SMTP_PORT', '587'))
            with smtplib.SMTP(smtp_host, port, timeout=15) as s:
                if os.getenv('SMTP_STARTTLS', '1') == '1':
                    s.starttls(context=ctx)
                user = os.getenv('SMTP_USER')
                pwd = os.getenv('SMTP_PASS')
                if user and pwd:
                    s.login(user, pwd)
                s.send_message(msg)
        except Exception as e:
            log('Email send failed:', e)
    # Telegram
    bot = os.getenv('TELEGRAM_BOT_TOKEN')
    chat = os.getenv('TELEGRAM_CHAT_ID')
    if bot and chat:
        import urllib.parse, urllib.request
        txt = urllib.parse.quote(body)
        url = f"https://api.telegram.org/bot{bot}/sendMessage?chat_id={chat}&text={txt}"
        try:
            urllib.request.urlopen(url, timeout=10).read()
        except Exception as e:
            log('Telegram send failed:', e)


def monitor_once():
    changes = []
    now = utcnow()
    with LOCK:
        data = load()
        for svc in data:
            if not svc.get('active', True):
                continue
            new_status, err, http_code, latency_ms = check_service(svc)
            prev = svc.get('last_status', 'unknown')
            svc['last_checked'] = now
            if http_code is not None:
                svc['last_http_status'] = http_code
            svc['last_latency_ms'] = latency_ms
            if new_status == 'up':
                svc.pop('last_error', None)
            else:
                if err:
                    svc['last_error'] = err
            # update latency history
            hid = svc['id']
            hist = LATENCY_HISTORY.setdefault(hid, [])
            hist.append(latency_ms)
            if len(hist) > MAX_HISTORY:
                del hist[0:len(hist)-MAX_HISTORY]
            notify = False
            if new_status != prev:
                svc['last_change'] = now
                notify = True
            else:
                last_notified = svc.get('last_notified')
                if new_status == 'down' and last_notified:
                    try:
                        dt = datetime.fromisoformat(last_notified)
                        if (datetime.now(timezone.utc) - dt).total_seconds() > NOTIFY_COOLDOWN_SEC:
                            notify = True
                    except Exception:
                        notify = True
            svc['last_status'] = new_status
            if notify:
                svc['last_notified'] = now
                changes.append(svc)
        save(data)
        # Append to historical log
        try:
            with open(STATUS_LOG, 'a') as logf:
                for svc in data:
                    if 'last_checked' == now:  # logic wrong purposely avoid heavy write? replaced below
                        pass
                for svc_changed in changes:
                    logf.write(json.dumps({
                        'ts': now,
                        'id': svc_changed['id'],
                        'status': svc_changed['last_status'],
                        'latency_ms': svc_changed.get('last_latency_ms'),
                        'http': svc_changed.get('last_http_status'),
                        'error': svc_changed.get('last_error')
                    }) + '\n')
        except Exception as e:
            log('WARN could not append status log:', e)
    if changes:
        log('Status changes:', ', '.join(f"{c['id']}={c['last_status']}" for c in changes))
        send_notifications(changes)


def check_single_service(service_id):
    """Check a single service by ID and update its status."""
    now = utcnow()
    with LOCK:
        data = load()
        service = next((svc for svc in data if svc['id'] == service_id), None)
        if not service:
            log(f'Service {service_id} not found')
            return
        
        if not service.get('active', True):
            log(f'Service {service_id} is inactive, skipping')
            return
            
        new_status, err, http_code, latency_ms = check_service(service)
        prev = service.get('last_status', 'unknown')
        service['last_checked'] = now
        if http_code is not None:
            service['last_http_status'] = http_code
        service['last_latency_ms'] = latency_ms
        if new_status == 'up':
            service.pop('last_error', None)
        else:
            if err:
                service['last_error'] = err
        # latency history
        hist = LATENCY_HISTORY.setdefault(service_id, [])
        hist.append(latency_ms)
        if len(hist) > MAX_HISTORY:
            del hist[0:len(hist)-MAX_HISTORY]
        
        notify = False
        if new_status != prev:
            service['last_change'] = now
            notify = True
        
        service['last_status'] = new_status
        if notify:
            service['last_notified'] = now
        
        save(data)
        log(f'Single check: {service_id}={new_status}')
        
        # Log change if status changed
        if notify:
            try:
                with open(STATUS_LOG, 'a') as logf:
                    logf.write(json.dumps({
                        'ts': now,
                        'id': service['id'],
                        'status': service['last_status'],
                        'latency_ms': service.get('last_latency_ms'),
                        'http': service.get('last_http_status'),
                        'error': service.get('last_error')
                    }) + '\n')
            except Exception as e:
                log('WARN could not append status log:', e)


def monitor_loop():
    while True:
        time.sleep(CHECK_INTERVAL_SEC)
        try:
            monitor_once()
        except Exception as e:
            log('Monitor iteration error:', e)


class Handler(BaseHTTPRequestHandler):
    def _auth_ok(self):
        return is_authenticated(self)
        
    def _safe_write(self, data: bytes):
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as e:
            # Client disconnected mid-response; ignore.
            log('Client disconnected during write:', e.__class__.__name__)
        except Exception as e:
            log('Unexpected write error:', e)

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        try:
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Auth-Token')
            self.end_headers()
            self._safe_write(body)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as e:
            log('Client aborted before headers/body complete:', e.__class__.__name__)
        except Exception as e:
            log('Handler _json error:', e)

    def do_OPTIONS(self):  # CORS preflight
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Auth-Token')
        self.end_headers()

    def log_message(self, *args):
        return  # silence default logging

    def do_GET(self):
        # Allow access to login page and static files without authentication
        if self.path == '/' or self.path == '/index.html':
            self.serve_file(os.path.join(BASE_DIR, 'static', 'index.html'), 'text/html')
            return
        if self.path.startswith('/static/'):
            # Normalize path to prevent directory escape
            rel = self.path[len('/static/'):]
            safe = os.path.normpath(rel).replace('..', '')
            self.serve_file(os.path.join(BASE_DIR, 'static', safe), None)
            return
        
        # All other endpoints require authentication
        if not self._auth_ok():
            self._json(401, {'error': 'Authentication required'})
            return
            
        if self.path.startswith('/api/services/') and not self.path.endswith('/'):
            # Get single service
            service_id = self.path.split('/')[-1]
            with LOCK:
                data = load()
                service = next((s for s in data if s['id'] == service_id), None)
                if service:
                    self._json(200, service)
                else:
                    self._json(404, {'error': 'Service not found'})
            return
        if self.path.startswith('/api/services'):
            with LOCK:
                self._json(200, load())
            return
        if self.path.startswith('/api/check'):
            # Manual trigger immediate check in background
            threading.Thread(target=monitor_once, daemon=True).start()
            self._json(200, {'started': True})
            return
        if self.path.startswith('/api/history/'):
            sid = self.path.split('/')[-1]
            with LOCK:
                hist = LATENCY_HISTORY.get(sid, [])
            self._json(200, {'id': sid, 'latency_ms': hist})
            return
        if self.path.startswith('/api/check/'):
            # Check single service by ID
            service_id = self.path.split('/')[-1]
            threading.Thread(target=lambda: check_single_service(service_id), daemon=True).start()
            self._json(200, {'started': True, 'service_id': service_id})
            return
        if self.path.startswith('/api/ping'):
            if self._auth_ok():
                self._json(200, {'ok': True, 'time': utcnow()})
            else:
                self._json(401, {'error': 'Authentication required'})
            return
        if self.path.startswith('/metrics'):
            # Prometheus metrics
            with LOCK:
                data = load()
            lines = [
                '# HELP service_up Service reachability (1=up,0=down)',
                '# TYPE service_up gauge',
                '# HELP service_latency_ms Last observed latency in milliseconds',
                '# TYPE service_latency_ms gauge',
                '# HELP service_http_status Last HTTP status observed',
                '# TYPE service_http_status gauge'
            ]
            for s in data:
                lid = s['id']
                up = 1 if s.get('last_status') == 'up' else 0
                labels = f'id="{lid}",name="{s.get("name",lid)}"'
                lines.append(f'service_up{{{labels}}} {up}')
                if 'last_latency_ms' in s:
                    lines.append(f'service_latency_ms{{{labels}}} {s["last_latency_ms"]}')
                if s.get('last_http_status'):
                    lines.append(f'service_http_status{{{labels}}} {s["last_http_status"]}')
            body = ('\n'.join(lines) + '\n').encode()
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; version=0.0.4')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self._safe_write(body)
            except Exception as e:
                log('metrics error:', e)
            return
        self._json(404, {'error': 'not found'})

    def do_POST(self):
        # Login endpoint doesn't require authentication
        if self.path.startswith('/api/login'):
            length = int(self.headers.get('Content-Length', 0))
            try:
                payload = json.loads(self.rfile.read(length) or '{}')
                session_token = authenticate_user(payload.get('password', ''))
                if session_token:
                    # Set secure cookie
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Set-Cookie', f'pacs_session={session_token}; HttpOnly; SameSite=Strict; Max-Age=86400')  # 24 hours
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Credentials', 'true')
                    self.end_headers()
                    response = json.dumps({'success': True, 'message': 'Authentication successful'}).encode()
                    self._safe_write(response)
                else:
                    self._json(401, {'success': False, 'message': 'Invalid password'})
            except Exception as e:
                log('Login error:', e)
                self._json(400, {'success': False, 'message': 'Invalid request'})
            return
            
        # Logout endpoint
        if self.path.startswith('/api/logout'):
            cookie_header = self.headers.get('Cookie')
            if cookie_header:
                cookies = SimpleCookie()
                cookies.load(cookie_header)
                session_token = cookies.get('pacs_session')
                if session_token and session_token.value in ACTIVE_SESSIONS:
                    del ACTIVE_SESSIONS[session_token.value]
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Set-Cookie', 'pacs_session=; HttpOnly; SameSite=Strict; Max-Age=0')  # Clear cookie
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({'success': True, 'message': 'Logged out'}).encode()
            self._safe_write(response)
            return
        
        # All other POST endpoints require authentication
        if not self._auth_ok():
            self._json(401, {'error': 'Authentication required'})
            return
            
        if self.path.startswith('/api/services'):
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length) or '{}')
            with LOCK:
                data = load()
                payload.setdefault('id', payload.get('name'))
                payload.setdefault('last_status', 'unknown')
                payload.setdefault('active', True)
                # env optional
                if 'env' in payload and not payload['env']:
                    payload.pop('env')
                # Remove existing with same id
                data = [d for d in data if d['id'] != payload['id']] + [payload]
                save(data)
            self._json(200, payload)
            return
        self._json(404, {'error': 'not found'})

    def do_PUT(self):  # treat same as POST (id must exist)
        return self.do_POST()

    def do_DELETE(self):
        if not self._auth_ok():
            self._json(401, {'error': 'Authentication required'})
            return
        if self.path.startswith('/api/services/'):
            sid = self.path.split('/')[-1]
            with LOCK:
                data = load()
                data = [d for d in data if d['id'] != sid]
                save(data)
            self._json(200, {'deleted': sid})
            return
        self._json(404, {'error': 'not found'})

    def serve_file(self, path, ctype):
        if not os.path.exists(path):
            self._json(404, {'error': 'not found'})
            return
        if ctype is None:
            if path.endswith('.js'):
                ctype = 'application/javascript'
            elif path.endswith('.css'):
                ctype = 'text/css'
            else:
                ctype = 'application/octet-stream'
        try:
            with open(path, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self._safe_write(data)
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError) as e:
            log('Client aborted serving file:', path, e.__class__.__name__)
        except Exception as e:
            log('Error serving file:', path, e)


def main():
    # Kick off monitor thread
    threading.Thread(target=monitor_loop, daemon=True).start()
    # Immediate first pass so UI is populated quickly
    threading.Thread(target=monitor_once, daemon=True).start()
    port = int(os.getenv('PORT', '8080'))
    log(f'Serving on http://localhost:{port}')
    ThreadingHTTPServer(('', port), Handler).serve_forever()


if __name__ == '__main__':
    main()
