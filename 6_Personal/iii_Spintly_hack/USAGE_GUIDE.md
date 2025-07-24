# 📖 Spintly Time Analysis - Usage Guide

## 🚀 Quick Start Options

### Option 1: Web Dashboard (Easiest)
1. **Start FastAPI**: `python spintly_fastapi_app.py`
2. **Open Dashboard**: http://localhost:8000
3. **Select Date**: Choose date in Time Analysis section
4. **Analyze**: Click "📊 Analyze Time"
5. **Export**: Click "💾 Export CSV"

### Option 2: Browser Console (Most Flexible)
1. **Go to Spintly**: https://smart-access.spintly.com/dashboard/access/history
2. **Open Console**: F12 → Console tab
3. **Choose Script**:
   - **Single Day**: Copy `spintly_live_time_analyzer.js`
   - **Multi-Day**: Copy `spintly_multi_day_analyzer.js`
4. **Paste & Run**: Paste in console, press Enter
5. **Get Results**: Instant analysis + CSV download

## 📊 What You Get (Matching Your Python Script)

### Time Analysis Tables
```
┌────────────┬─────────────┬─────────────┬─────────────┬────────┬─────────────┬─────────────────────┐
│    Date    │ Total Time  │Office Hours │ Break Time  │ Target │ Difference  │       Status        │
├────────────┼─────────────┼─────────────┼─────────────┼────────┼─────────────┼─────────────────────┤
│Jul 23      │09:45:32     │08:30:00     │01:15:32     │✓       │🟢 +00:00:00│🟢 Target met       │
└────────────┴─────────────┴─────────────┴─────────────┴────────┴─────────────┴─────────────────────┘
```

### CSV Export (Same Format as Python)
```csv
Date,Name,Office Time With Seconds,Office Time Without Seconds,Sign With Seconds,Difference With Seconds,Sign Without Seconds,Difference Without Seconds,Status,Message With Seconds,Message Without Seconds
2025-07-23,Subin,08:30:15,08:30:00,+,00:00:15,+,00:00:00,Target met,,
```

## 🎯 Browser Console Commands

### Single Day Analysis
```javascript
// Copy and paste spintly_live_time_analyzer.js
// Automatically analyzes current page data
```

### Multi-Day Analysis
```javascript
// Copy and paste spintly_multi_day_analyzer.js
// Analyzes last 7 days by default

// Custom commands available after running:
window.analyzeLastWeek()     // Last 7 days
window.analyzeLastMonth()    // Last 30 days
window.analyzeCustomRange('2025-07-15', '2025-07-23')  // Custom range
```

## 🔗 API Endpoints

### Time Analysis APIs
```bash
# Today's analysis
GET http://localhost:8000/api/time-analysis/today

# Specific date
GET http://localhost:8000/api/time-analysis/2025-07-23

# Date range
GET http://localhost:8000/api/time-analysis/range/2025-07-15/2025-07-23

# Export CSV
GET http://localhost:8000/api/csv-export/2025-07-23
```

## ⚙️ Configuration

### Time Settings (Matching Your Python)
- **Office Hours**: 7:30 AM - 7:30 PM
- **Target Time**: 8.5 hours (8h 30m)
- **Break Calculation**: Total duration - active time
- **Overtime Cap**: 1 hour/day for positive differences

### Customization
To change settings, edit these constants in the scripts:
```javascript
const OFFICE_START = { hour: 7, minute: 30 };
const OFFICE_END = { hour: 19, minute: 30 };
const TARGET_TIME = 8.5 * 3600; // seconds
```

## 🔄 Workflow Comparison

### Before (Manual Python Process)
1. Download CSV from Spintly ⏱️ 2 min
2. Run Python script ⏱️ 1 min
3. Check results ⏱️ 1 min
4. **Total**: 4 minutes per check

### After (Live Browser Analysis)
1. Open Spintly dashboard ⏱️ 30 sec
2. Paste script in console ⏱️ 10 sec
3. Get instant results + CSV ⏱️ 5 sec
4. **Total**: 45 seconds per check

### After (Web Dashboard)
1. Open dashboard ⏱️ 5 sec
2. Select date & analyze ⏱️ 10 sec
3. Export CSV if needed ⏱️ 5 sec
4. **Total**: 20 seconds per check

## 🎉 Benefits Achieved

### ✅ **Live Updates**
- No more manual CSV downloads
- Real-time data from browser
- Instant analysis results

### ✅ **Same Logic**
- Identical calculations to your Python script
- Same CSV format
- Same time analysis methodology

### ✅ **Multiple Options**
- Browser console for flexibility
- Web dashboard for convenience
- API endpoints for integration

### ✅ **Enhanced Features**
- Multi-day analysis
- Date range selection
- Auto CSV download
- Visual status indicators

## 🆘 Troubleshooting

### Browser Console Issues
- **No data found**: Make sure you're on the access history page
- **Script errors**: Clear console and try again
- **No CSV download**: Copy the CSV content manually

### FastAPI Issues
- **App not starting**: Check if port 8000 is free
- **No data**: Run the update script first
- **Analysis errors**: Verify date format (YYYY-MM-DD)

### Data Issues
- **Wrong calculations**: Verify office hours settings
- **Missing records**: Check if all data is loaded on page
- **Time zone issues**: All times should be in IST

## 📞 Quick Commands Reference

```javascript
// In browser console after running scripts:

// Single day analysis (auto-runs)
runSpintlyTimeAnalysis()

// Multi-day analysis
runMultiDayAnalysis(7)  // Last 7 days
analyzeLastWeek()       // Same as above
analyzeLastMonth()      // Last 30 days
analyzeCustomRange('2025-07-15', '2025-07-23')

// Access results
window.spintlyTimeAnalysis.results      // Single day results
window.spintlyMultiDayAnalysis.results  // Multi-day results
```

---

**You now have a complete live replacement for your Python CSV workflow!** 🎉