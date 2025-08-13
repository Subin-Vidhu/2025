# 🏥 PACS Medical Server Monitoring Dashboard

## What is This?

This is a **medical imaging server monitoring tool** that keeps watch over your hospital's PACS (Picture Archiving and Communication System) servers. Think of it as a "health checker" for the computer systems that store and manage medical images like X-rays, CT scans, and MRIs.

**In Simple Terms:** This application continuously checks if your medical imaging servers are working properly and alerts you immediately if something goes wrong, so patients and doctors don't experience delays in accessing medical images.

## Key Benefits

- ✅ **24/7 Automated Monitoring** - Never miss when a server goes down
- 🚨 **Instant Alerts** - Get notified via Email and Telegram immediately
- 📊 **Visual Dashboard** - See all your servers' status at a glance
- 📈 **Performance Tracking** - Monitor response times and identify slow servers
- 🔧 **Zero Setup Complexity** - No databases or complex installations required
- 📱 **Works Anywhere** - Access from any web browser on any device

## How It Works (Simple Workflow)

1. **Continuous Monitoring**: Every 60 seconds, the system automatically "pings" each of your PACS servers
2. **Health Check**: For each server, it checks if it can connect and get a response
3. **Status Recording**: Records whether each server is UP (working) or DOWN (not responding)
4. **Alert System**: If a server goes down, immediately sends alerts to configured email addresses and Telegram
5. **Dashboard Display**: Shows real-time status of all servers in a user-friendly web interface
6. **Historical Tracking**: Keeps a log of all status changes for troubleshooting and reporting

## Technical Overview

A lightweight, modern, self‑contained monitoring dashboard built with Python's standard library and vanilla JavaScript. It tracks uptime of PACS/Orthanc servers or any HTTP endpoints, provides real-time status updates, and sends alerts when services change state.

**No external dependencies required** - everything runs from this single folder.

## 🚀 Quick Start (For Beginners)

### Step 1: Basic Setup
```cmd
cd path\to\this\folder
python app.py
```
Then open your web browser and go to: http://localhost:8080

### Step 2: Authentication
When you first visit the dashboard, you'll see a login screen:
- **Access Key**: Enter `PROTOS25` (the secret key for this system)
- Click **"Access Dashboard"** 

🔒 **Security Note**: This key is required every time you access the dashboard for the first time in a new browser session.

### Step 3: Understanding the Dashboard

When you access the dashboard (after entering the secret key), you'll see:
- **Green cards**: Servers that are working properly (UP)
- **Red cards**: Servers that are having problems (DOWN)  
- **Orange/Yellow cards**: Servers that haven't been checked yet (UNKNOWN)
- **Response times**: How quickly each server responds (lower is better)
- **Last checked**: When each server was last tested
- **Logout button**: Click the 🚪 Logout button in the top-right to return to login screen

### Step 4: Adding Your Own Servers

1. Click the **"+ Add Service"** button
2. Fill in the form:
   - **Name**: A friendly name for your server (e.g., "Main PACS Server")
   - **Host**: The server address (e.g., "medical-server.hospital.com")
   - **Port**: The port number (usually 80, 443, or a custom number like 8042)
   - **Protocol**: Choose "https" (secure) or "http" (standard)
   - **Path**: Usually just leave as "/" (root directory)
3. Click **"Save"**

Your new server will appear as a card and start being monitored automatically!

## 🔧 Advanced Configuration

### Setting Up Alerts (Optional but Recommended)

To receive notifications when servers go down, you can configure:

#### Email Alerts
Set these environment variables before running the application:
```cmd
set SMTP_HOST=smtp.gmail.com
set SMTP_USER=your-email@gmail.com
set SMTP_PASS=your-app-password
set ALERT_EMAIL=alerts@hospital.com
```

#### Telegram Alerts (Popular Choice)
1. Create a Telegram bot by messaging @BotFather
2. Get your chat ID by messaging @userinfobot
3. Set these variables:
```cmd
set TELEGRAM_BOT_TOKEN=123456789:ABCDEF...
set TELEGRAM_CHAT_ID=987654321
```

#### Customizing Check Frequency
```cmd
set CHECK_INTERVAL_SEC=30    (check every 30 seconds instead of 60)
set NOTIFY_COOLDOWN_SEC=600  (wait 10 minutes between repeat alerts)
```

### Windows Examples

**Command Prompt (cmd.exe):**
```cmd
set SMTP_HOST=smtp.gmail.com
set SMTP_USER=monitor@hospital.com  
set SMTP_PASS=your-password
set ALERT_EMAIL=it-team@hospital.com
set PORT=8080
python app.py
```

**PowerShell:**
```powershell
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_USER = "monitor@hospital.com"
$env:SMTP_PASS = "your-password"
$env:ALERT_EMAIL = "it-team@hospital.com"
python app.py
```

## 🔍 Understanding How the System Works

### The Monitoring Process (Behind the Scenes)

1. **Startup**: When you run `python app.py`, the system:
   - Starts a web server on port 8080
   - Loads your list of servers from `services.json`
   - Begins the monitoring loop in the background

2. **Health Check Process**: Every 60 seconds, for each server:
   - **Step 1**: Try to establish a TCP connection to the server
   - **Step 2**: Send an HTTP request (like opening a webpage)
   - **Step 3**: Check if the server responds within 10 seconds
   - **Step 4**: Record the response time (latency in milliseconds)
   - **Step 5**: Update the server status (UP if responding, DOWN if not)

3. **Status Evaluation**: A server is considered:
   - **UP**: Responds with any HTTP status code from 200-499 (even authentication errors count as "alive")
   - **DOWN**: No response, connection timeout, or HTTP 500+ server errors
   - **UNKNOWN**: Not yet checked since system startup

4. **Alert Logic**: When a server status changes:
   - **UP → DOWN**: Immediately send alert "Server X is down"
   - **DOWN → UP**: Immediately send alert "Server X is back online"
   - **Still DOWN**: Send reminder alerts every 15 minutes (configurable)

### File Structure Explained

```
📁 vi_AIRA_Test/
├── 🐍 app.py                    # Main application (web server + monitoring)
├── 📊 services.json             # Your servers configuration
├── 📝 status_log.jsonl         # Historical log of all changes
├── 🔧 diag.py                  # Diagnostic tool for testing connections
└── 📁 static/
    ├── 🌐 index.html           # Web dashboard interface
    ├── ⚙️ app.js              # Interactive features (add/edit/delete)
    └── 🎨 styles.css          # Modern dark theme styling
```

### What Each File Does

- **`app.py`**: The brain of the operation - runs the web server and monitoring
- **`services.json`**: Stores your server list and their current status
- **`status_log.jsonl`**: Keeps a permanent record of when servers went up/down
- **`static/index.html`**: The webpage you see in your browser
- **`static/app.js`**: Makes the webpage interactive (buttons, forms, live updates)
- **`static/styles.css`**: Makes everything look modern and professional

## 📱 Using the Web Dashboard

### Dashboard Features Explained

1. **Statistics Bar** (top of page):
   - Shows total servers, how many are UP/DOWN, and average response time

2. **Server Cards**: Each server gets its own card showing:
   - **Name**: Friendly identifier
   - **Status Badge**: Green (UP), Red (DOWN), or Orange (UNKNOWN)
   - **Response Time**: How fast the server responded (lower is better)
   - **Last Checked**: When it was last tested
   - **Action Buttons**: Check now, Edit, or Delete

3. **Control Buttons**:
   - **↻ Refresh Data**: Get latest status from backend
   - **🔄 Check All**: Force immediate check of all servers
   - **+ Add Service**: Add a new server to monitor

### Adding Servers - Step by Step

1. Click **"+ Add Service"**
2. **Fill out the form**:
   - **Name**: Something descriptive like "Main PACS Server" or "Backup Imaging System"
   - **Host**: The server address (domain name or IP address)
   - **Port**: Leave blank for standard ports, or enter custom port number
   - **Protocol**: Choose HTTPS for secure connections, HTTP for standard
   - **Path**: Usually just "/" unless you need a specific webpage path
   - **Active**: Keep checked to monitor, uncheck to temporarily disable
3. **Click Save**

The new server will appear immediately and start being checked within 60 seconds.

## 🛠️ Technical Features

### Advanced Features
* **Modern UI**: Dark theme, responsive design, works on mobile devices
* **Real-time Updates**: Dashboard refreshes automatically every 15 seconds
* **Manual Controls**: Force immediate checks of individual servers or all servers
* **Search & Filter**: Find specific servers quickly in large lists
* **Performance Monitoring**: Track response times and identify slow servers
* **Historical Logging**: Every status change is permanently recorded
* **Security**: Optional token-based authentication for access control
* **Integration Ready**: Provides Prometheus metrics endpoint for enterprise monitoring
* **Resilient**: Handles SSL certificate issues, DNS problems, and network timeouts gracefully

### Network Requirements
* Python 3.9 or newer (most modern Windows systems have this)
* Internet/network access to reach your PACS servers
* If using email alerts: access to your organization's SMTP server
* If using Telegram: internet access to api.telegram.org

### Currently Monitoring
This installation is pre-configured to monitor several medical imaging servers:
- fdapacslive.protosonline.in (Port: HTTPS default)
- orthanc1 (pacsingest.protosonline.in)
- protosradium, protosruby, radiumpacs, skpacs, testpacs
- And several others from the protosonline.in medical network

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

| Problem | What You See | Solution |
|---------|-------------|----------|
| All servers show UNKNOWN | Orange/yellow cards, no status | **Wait 60 seconds** - first check cycle hasn't completed yet |
| Server always shows DOWN | Red card, even though server works | Check if server address and port are correct |
| No email alerts | System works but no emails | Verify SMTP settings and check spam folder |
| Telegram not working | No Telegram messages | Double-check bot token and chat ID |
| Can't access dashboard | Browser shows "can't connect" | Make sure `python app.py` is running |
| Dashboard shows old data | Status doesn't update | Click the "↻ Refresh Data" button |

### Testing Your Setup

1. **Test Basic Functionality**:
   ```cmd
   python app.py
   # Should see: [monitor] Serving on http://localhost:8080
   ```

2. **Test Server Connectivity**:
   ```cmd
   python diag.py
   # This will test connections to your configured servers
   ```

3. **Test Dashboard Access**:
   - Open browser to http://localhost:8080
   - Should see cards for all servers (may show UNKNOWN initially)

### Understanding Server Status Codes

When you see numbers like "401", "200", "404" on server cards, these are HTTP response codes:
- **200**: Perfect - server is working normally
- **401**: Good - server is running but requires login (normal for PACS)
- **404**: OK - server is running but page not found (still alive)
- **500+**: Problem - server has internal errors
- **No number**: Server is completely unreachable

## 🔒 Security Features

### Built-in Authentication
- **Secret Key Protection**: Access requires entering "PROTOS25" 
- **Session Management**: Key is remembered during your browser session
- **Auto-logout**: Session expires when browser is closed for security
- **Secure Access**: Only authorized personnel can view server status

### Optional Advanced Security

**Additional Token Authentication**: For extra security layers, you can still configure the original token system:
```cmd
set DASHBOARD_TOKEN=your-additional-secret-token
```

### Security Best Practices
- **Secret Key Management**: The access key "PROTOS25" is built into the system for secure access
- **Network Security**: Don't expose this directly to the internet without additional security
- **Credential Protection**: Keep email/Telegram credentials secure and don't commit them to version control
- **Production Deployment**: Consider running behind a reverse proxy (Nginx/Apache) for additional security layers

## 🏥 Real-World Usage Scenarios

### Typical Hospital/Clinic Setup

1. **IT Manager** sets up the monitoring system on a dedicated Windows computer
2. **Configures** all PACS servers, workstations, and imaging equipment
3. **Sets up alerts** to notify the IT team via email and Telegram group chat
4. **Monitors 24/7** to ensure medical staff always have access to patient images

### What Gets Monitored

- **Main PACS Server**: Stores all medical images
- **Backup PACS**: Secondary storage system
- **Workstations**: Computers doctors use to view images
- **Web Viewers**: Browser-based image viewing systems
- **Integration Points**: Systems that connect to other hospital software

### Benefits for Medical Facilities

- **Prevent Patient Care Delays**: Know immediately when imaging systems fail
- **Reduce Downtime**: Faster problem detection means faster fixes
- **Compliance**: Maintain uptime records required by healthcare regulations
- **Cost Savings**: Prevent expensive emergency IT service calls
- **Peace of Mind**: 24/7 automated monitoring without manual checking

## 📈 Advanced Usage

### Running as a Windows Service

For production use, you can run this as a background Windows service:

1. **Simple Background Process**:
   ```cmd
   start /B python app.py
   # Runs in background, will stop when you log out
   ```

2. **Task Scheduler** (Recommended):
   - Open Windows Task Scheduler
   - Create new task to run `python app.py` at system startup
   - Configure to run whether user is logged on or not

### Integration with Other Systems

- **Prometheus Metrics**: Visit http://localhost:8080/metrics for monitoring data
- **JSON API**: Use `/api/services` endpoint for programmatic access
- **Historical Data**: Parse `status_log.jsonl` for reporting and analysis
- **Custom Scripts**: Modify `app.py` to add custom notification methods

### Scaling for Large Organizations

- Monitor hundreds of servers (tested with 100+ concurrent checks)
- Use multiple instances for different departments
- Export data to enterprise monitoring tools
- Customize check intervals per service type

## 📞 Support and Customization

### Getting Help

1. **Check the logs**: The application prints helpful messages to the console
2. **Test connectivity**: Use `diag.py` to troubleshoot connection issues  
3. **Verify configuration**: Ensure `services.json` has correct server details
4. **Browser console**: Check for JavaScript errors (F12 → Console tab)

### Customizing the System

The code is designed to be easily modified:
- **Add new notification methods**: Edit the `send_notifications()` function
- **Change UI appearance**: Modify `static/styles.css`
- **Adjust monitoring logic**: Update the `check_service()` function
- **Add new features**: Extend the REST API in `app.py`

### Future Enhancement Ideas

- **Mobile app**: Create iOS/Android companion app
- **Advanced analytics**: Add uptime percentages and SLA reporting
- **Multi-location**: Monitor servers across different hospital sites
- **Integration**: Connect with existing hospital IT management systems
- **Backup monitoring**: Check database backups and disaster recovery systems

---

## 📝 License & Usage

This is internal tooling designed for healthcare and enterprise environments. Feel free to adapt and modify for your organization's specific needs.

---

## 🎯 Summary

This monitoring system provides **enterprise-grade server monitoring** with a **simple setup process**. Perfect for hospitals, clinics, and any organization that needs reliable monitoring of critical servers with instant alert capabilities.

**Key Value**: Never again will critical medical imaging systems fail without your immediate knowledge, ensuring continuous patient care and regulatory compliance.
