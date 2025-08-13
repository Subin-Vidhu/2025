## PACS / Orthanc Servers Monitoring Dashboard (No External Frameworks)

A lightweight, modern, self‑contained monitoring dashboard (Python stdlib + vanilla JS) to track uptime of PACS / Orthanc (or any HTTP) endpoints. It periodically checks each configured service, shows live status, and sends alerts via Email and/or Telegram when a service changes state or remains down.

All files live in this single folder. No third‑party packages are required.

---

### Features
* Dark, modern card UI (matching provided theme)
* Periodic health checks (default every 60s)
* Live dashboard auto-refresh (15s) + manual refresh (+ manual backend "Check Now")
* Add / Edit / Delete services from UI (CRUD)
* Email + Telegram alerts on status changes (and periodic reminders while down)
* Latency (ms) and last HTTP status code captured per check
* Optional token-based auth (`DASHBOARD_TOKEN` with `X-Auth-Token` header)
* Prometheus metrics endpoint (`/metrics`) for integration
* Historical change log (`status_log.jsonl`) append-only
* Alert cooldown to prevent spam (default 15 min while a service stays down)
* Graceful handling of unreachable hosts / DNS / SSL issues (falls back to unverified when needed)
* Simple JSON persistence (`services.json`) with atomic writes & corruption backup
* Pure stdlib: no `pip install` needed

---

### File Layout
```
app.py               # Python HTTP server + monitor loop
services.json        # Service definitions & status metadata
static/              # Front-end assets
	index.html
	app.js
	styles.css
readme.md            # This file
```

---

### 1. Prerequisites
* Python 3.9+ (any recent CPython version is fine)
* Outbound network access to the monitored domains (and SMTP / Telegram if using alerts)

No libraries to install.

---

### 2. Configure Services (`services.json`)
Each entry:
```
{
	"id": "fdapacslive",        # unique ID (stable key)
	"name": "fdapacslive",      # display name
	"host": "fdapacslive.protosonline.in",
	"port": 8049,                # omit or 443 for standard https
	"protocol": "https",        # http or https
	"path": "/",                # optional path
	"active": true,              # can be toggled off without deleting
	"last_status": "unknown"    # runtime fields (updated automatically)
}
```
You can seed with the provided defaults (already created). Modify manually or via the UI.

---

### 3. Alert Configuration (Environment Variables)
Set only what you need. If email or Telegram config is missing, that channel is skipped.

| Variable | Purpose |
|----------|---------|
| `SMTP_HOST` | SMTP server hostname |
| `SMTP_PORT` | (Optional) Port (default 587) |
| `SMTP_STARTTLS` | `1` (default) to use STARTTLS, `0` to disable |
| `SMTP_USER` / `SMTP_PASS` | Credentials if required |
| `SMTP_FROM` | From address (defaults to `SMTP_USER`) |
| `ALERT_EMAIL` | Destination email for alerts |
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather |
| `TELEGRAM_CHAT_ID` | Chat / group ID for notifications |
| `PORT` | HTTP listen port for dashboard (default 8080) |
| `CHECK_INTERVAL_SEC` | (Optional) override check frequency |
| `NOTIFY_COOLDOWN_SEC` | (Optional) override cooldown |

#### Windows (cmd.exe) Example
```
set SMTP_HOST=smtp.example.com
set SMTP_USER=monitor@example.com
set SMTP_PASS=YourPasswordHere
set ALERT_EMAIL=ops-team@example.com
set TELEGRAM_BOT_TOKEN=123456:ABCDEF...
set TELEGRAM_CHAT_ID=987654321
set PORT=8080
python app.py
```

#### PowerShell Example
```
$env:SMTP_HOST = "smtp.example.com"
$env:SMTP_USER = "monitor@example.com"
$env:SMTP_PASS = "YourPasswordHere"
$env:ALERT_EMAIL = "ops-team@example.com"
$env:TELEGRAM_BOT_TOKEN = "123456:ABCDEF..."
$env:TELEGRAM_CHAT_ID = "987654321"
python app.py
```

---

### 4. Run the Dashboard
From this folder:
```
python app.py
```
Open: http://localhost:8080/

You should see all configured services with initial UNKNOWN status; they will update after the first check cycle (up to 60s by default). To force a manual view refresh, use the Refresh button (front-end re-fetch only; it does not trigger an immediate backend probe between intervals).

---

### 5. Using the UI
* Add: Click "Add" -> fill form -> Save
* Edit: Click a card's Edit button
* Delete: Click Del (confirmation prompted by browser)
* Deactivate (temporarily stop monitoring): Edit a service and uncheck Active
* Status colors: Green = UP, Red = DOWN, Amber = UNKNOWN/unseen
* Timestamps show relative time for last state change & last check

---

### 6. How Health Checks Work
For each active service every interval:
1. TCP connect to `host:port` (timeout 8s)
2. HTTP HEAD request (fallback to GET) to `protocol://host[:port]/path`
3. Status `up` if reachable and returns any 2xx–4xx code (5xx counts as down). 4xx still proves service/process is alive.
4. Changes recorded + notifications sent on transitions or periodic reminders while down (after cooldown).

Adjust logic inside `check_service` in `app.py` as desired.

---

### 7. Alert Logic
* Immediate notification on state change (UP→DOWN or DOWN→UP)
* While DOWN, repeat notification after `NOTIFY_COOLDOWN_SEC` (default 900s)
* UP steady state generates no repeats
* Both channels (email / Telegram) try independently; failures are logged to stdout

---

### 8. Customizing Intervals / Cooldowns
You can override constants via environment variables:
```
set CHECK_INTERVAL_SEC=30
set NOTIFY_COOLDOWN_SEC=600
```
(If not set, defaults inside `app.py` are used.)

---

### 9. Optional: Token Auth
Set environment variable:
```
set DASHBOARD_TOKEN=yourSecretToken123
```
Client requests must include header:
```
X-Auth-Token: yourSecretToken123
```
In the browser console you can set:
```
window.DASHBOARD_TOKEN = 'yourSecretToken123'; triggerCheckNow();
```

---

### 10. Running as a Background Service (Windows)
Simplest: Use `start /B python app.py` in a dedicated cmd window or create a basic Task Scheduler entry that runs on startup.

For production: Place behind Nginx / Caddy for TLS termination (or use `openssl` + `ssl.wrap_socket` if desired).

---

### 11. Updating / Extending
Ideas:
* Average / percentile latency per service
* SLA / uptime % calculations
* WebSocket push instead of polling
* Multi-user auth + role separation
* Retry/backoff strategy per service
* UI to download `status_log.jsonl`

---

### 12. Troubleshooting
| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| All services stay UNKNOWN | No checks yet | Wait 60s or lower interval |
| Always DOWN | Firewall / DNS / wrong port | Verify host resolves, test with `ping` / `curl` |
| Email not sent | SMTP var missing / auth fail | Check env vars and server logs |
| Telegram silent | Bot token or chat ID wrong | Use `getUpdates` API to confirm chat ID |
| JSON resets | Accidental manual edit with invalid JSON | Validate JSON before saving |

Logs print to stdout; wrap with a simple redirect if you want a file: `python app.py > monitor.log 2>&1`.

---

### 13. Security Notes
* No authentication by default (add reverse proxy or token snippet above)
* Avoid exposing directly to the public internet without protections
* Limit environment variable visibility (remove secrets from version control)

---

### 14. License / Usage
Internal tooling snippet – adapt freely within your organization.

---

### 15. Quick Start Recap
```
cd this/folder
python app.py
# Browse http://localhost:8080/
```

Customize `services.json` anytime. The monitor thread reloads from disk each cycle.

---

---

### 16. Manual Check & Metrics
* Immediate probe: in console run `triggerCheckNow()` (optionally after setting `window.DASHBOARD_TOKEN`).
* Metrics: browse `http://localhost:8080/metrics` to view Prometheus exposition format.

### 17. Basic Testing Steps
1. Start server: `python app.py`
2. Confirm services show as UNKNOWN then become UP.
3. Temporarily block a host (edit its hostname to invalid) -> should go DOWN and (if email/telegram configured) alert.
4. Restore host -> should flip to UP and alert again.
5. Visit `/metrics` and check for `service_up{id="..."}` lines.
6. Open `status_log.jsonl` to see JSON change events appended.

### 18. Example Log Line
```
{"ts":"2025-08-13T03:40:12.123456+00:00","id":"fdapacslive","status":"down","latency_ms":812,"http":502,"error":"http:502"}
```

---

Happy monitoring.
