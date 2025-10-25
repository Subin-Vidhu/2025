# 🔧 Telegram Webhook Setup Fix

## 🚨 The Problem
Telegram webhooks require:
- **HTTPS URLs only** (not HTTP)  
- **Public URLs** (not localhost)

Your current error: `"Bad Request: bad webhook: An HTTPS URL must be provided for webhook"`

## 🛠 Solutions (Choose One)

### Option 1: Use ngrok (Recommended for Testing)

1. **Download ngrok**: https://ngrok.com/download
2. **Expose your n8n instance**:
```bash
ngrok http 5678
```
3. **Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`)
4. **Set webhook with HTTPS URL**:
```bash
curl -X POST "https://api.telegram.org/bot8483914760:AAEEp8Tccbc5blGme5bZOxI-dr1e6WbRopM/setWebhook" \
-H "Content-Type: application/json" \
-d '{"url": "https://YOUR_NGROK_URL.ngrok.io/webhook/debug-jira"}'
```

### Option 2: Use Your Router's Public IP with Port Forwarding

1. **Set up port forwarding** on your router: Port 5678 → 192.168.0.196:5678
2. **Get your public IP**: https://whatismyipaddress.com/
3. **Set up HTTPS** (complex - requires SSL certificate)

### Option 3: Use Polling Instead of Webhooks (Easiest)

Create a polling-based workflow instead of webhook:

```json
{
  "name": "Subin's Jira Polling Bot",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [{"field": "seconds", "secondsInterval": 10}]
        }
      },
      "id": "polling-trigger",
      "name": "Check for Messages",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [0, 0]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "https://api.telegram.org/bot8483914760:AAEEp8Tccbc5blGme5bZOxI-dr1e6WbRopM/getUpdates",
        "sendQuery": true,
        "queryParameters": {
          "parameters": [
            {"name": "offset", "value": "={{ $json.lastUpdateId || 0 }}"},
            {"name": "timeout", "value": "10"}
          ]
        }
      },
      "id": "get-updates",
      "name": "Get Telegram Updates",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [200, 0]
    }
  ]
}
```

## 🚀 Quick Fix with ngrok (Recommended)

### Step 1: Install ngrok
```bash
# Download from https://ngrok.com/download
# Or if you have chocolatey:
choco install ngrok

# Or if you have scoop:
scoop install ngrok
```

### Step 2: Start ngrok
```bash
ngrok http 5678
```

You'll see output like:
```
Session Status                online
Account                       user@example.com
Forwarding                    https://abc123.ngrok.io -> http://localhost:5678
```

### Step 3: Update Webhook
```bash
# Replace abc123.ngrok.io with your actual ngrok URL
curl -X POST "https://api.telegram.org/bot8483914760:AAEEp8Tccbc5blGme5bZOxI-dr1e6WbRopM/setWebhook" \
-H "Content-Type: application/json" \
-d '{"url": "https://abc123.ngrok.io/webhook/debug-jira"}'
```

### Step 4: Test
Send a message to your Telegram bot - it should now work!

## 🔄 Alternative: Remove Webhook (Use Polling)

If you don't want to deal with webhooks:

```bash
# Remove webhook
curl -X POST "https://api.telegram.org/bot8483914760:AAEEp8Tccbc5blGme5bZOxI-dr1e6WbRopM/deleteWebhook"

# Then use polling method instead
```

## ✅ Verification

After setting up with ngrok, verify webhook:
```bash
curl "https://api.telegram.org/bot8483914760:AAEEp8Tccbc5blGme5bZOxI-dr1e6WbRopM/getWebhookInfo"
```

Should return:
```json
{
  "ok": true,
  "result": {
    "url": "https://abc123.ngrok.io/webhook/debug-jira",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

---

**Next Action**: Install ngrok and follow Step 1-4 above! 🚀