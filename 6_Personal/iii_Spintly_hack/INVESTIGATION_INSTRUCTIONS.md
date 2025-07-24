# Spintly API Investigation Instructions

## 🎯 Objective
Reverse engineer the Spintly dashboard API to create automated access to office access history data.

## 📋 Prerequisites
- Access to Spintly dashboard: https://smart-access.spintly.com/dashboard/access/history
- Valid login credentials
- Chrome/Firefox browser with Developer Tools

## 🔍 Investigation Steps

### Step 1: Initial Setup
1. **Login to Spintly Dashboard**
   - Go to: https://smart-access.spintly.com/login
   - Login with your credentials
   - Navigate to: https://smart-access.spintly.com/dashboard/access/history

2. **Open Developer Tools**
   - Press F12 or right-click → Inspect
   - Go to Console tab
   - Clear any existing logs

### Step 2: Run Investigation Script
1. **Copy the entire content** from `browser_investigation_script.js`
2. **Paste into browser console** and press Enter
3. **Wait for initial setup** to complete (you'll see green checkmarks)

### Step 3: Capture Network Traffic
1. **Refresh the page** or navigate to access history again
2. **Wait for page to fully load** (let all data load)
3. **Run analysis**: Type `window.spintlyInvestigation.analyze()` and press Enter

### Step 4: Save Results
1. **Copy the JSON output** from console (between the === lines)
2. **Save as**: `investigation_results.json` in this folder
3. **Also check Downloads folder** for auto-downloaded file

## 📊 What We're Looking For

### Authentication Data
- [ ] Session cookies (especially authentication tokens)
- [ ] CSRF tokens
- [ ] Authorization headers
- [ ] API keys or bearer tokens

### API Endpoints
- [ ] Access history API endpoint
- [ ] Authentication/login endpoint
- [ ] Data format (JSON/XML)
- [ ] Request parameters (pagination, filters, etc.)

### Request Details
- [ ] HTTP method (GET/POST)
- [ ] Required headers
- [ ] Request body format
- [ ] Response structure

## 🚨 Troubleshooting

### If No API Calls Are Captured:
1. **Check Network Tab** in DevTools manually
2. **Try different actions**:
   - Refresh page
   - Change date filters
   - Navigate between pages
   - Click pagination buttons

### If Authentication Fails:
1. **Check for 401/403 errors** in Network tab
2. **Look for redirect to login page**
3. **Verify cookies are being sent**

### If Table Data is Empty:
1. **Wait longer** for page to load
2. **Check if data loads via AJAX**
3. **Try scrolling down** to trigger lazy loading

## 📝 Manual Backup Method

If the script doesn't work, manually check:

### Network Tab Investigation:
1. Open DevTools → Network tab
2. Clear network log
3. Refresh the access history page
4. Look for XHR/Fetch requests
5. Right-click on API calls → Copy as cURL

### Manual Data Extraction:
```javascript
// Run this in console to extract table data manually
const rows = document.querySelectorAll("table tbody tr");
const data = [];
rows.forEach(row => {
    const cells = row.querySelectorAll("td");
    if (cells.length >= 6) {
        data.push({
            name: cells[0].innerText.trim(),
            datetime: cells[1].innerText.trim(),
            direction: cells[5].innerText.trim()
        });
    }
});
console.log(JSON.stringify(data, null, 2));
```

## 📁 Files to Create

After investigation, you should have:
- [ ] `investigation_results.json` - Complete captured data
- [ ] `api_endpoints.txt` - List of discovered endpoints
- [ ] `curl_commands.txt` - Working curl commands
- [ ] `postman_collection.json` - Postman collection (we'll create this)

## 🔄 Next Steps

Once investigation is complete:
1. **Analyze the results** together
2. **Create working curl commands**
3. **Build Postman collection**
4. **Test API access**
5. **Create FastAPI wrapper**

## ⚠️ Important Notes

- **Don't share credentials** in any files
- **Be careful with sensitive data** in logs
- **Test in incognito mode** to verify session requirements
- **Document any rate limiting** you encounter