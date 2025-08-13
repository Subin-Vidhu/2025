import socket, ssl, urllib.request, traceback, sys
hosts = [
    'fdapacslive.protosonline.in',
    'fdapacstest.protosonline.in',
    'pacsingest.protosonline.in'
]
print('Python version', sys.version)
for host in hosts:
    print('\n===', host, '===')
    # DNS
    try:
        print('DNS ->', socket.gethostbyname_ex(host)[2])
    except Exception as e:
        print('DNS FAIL:', e)
        continue
    # TCP
    try:
        with socket.create_connection((host, 443), timeout=8):
            print('TCP 443 OK')
    except Exception as e:
        print('TCP FAIL:', repr(e))
        continue
    # HTTPS GET (verified)
    try:
        with urllib.request.urlopen('https://' + host + '/', timeout=12) as r:
            print('HTTPS GET status', r.status)
    except Exception as e:
        print('HTTPS verified FAIL:', type(e).__name__, e)
    # HTTPS GET (unverified)
    try:
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen('https://' + host + '/', timeout=12, context=ctx) as r:
            print('HTTPS (ignore cert) status', r.status)
    except Exception as e:
        print('HTTPS unverified FAIL:', type(e).__name__, e)
