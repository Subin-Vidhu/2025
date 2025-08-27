# 🎯 JIRA Daily Worklog Tracker

A Chrome extension that helps you track daily worklogs in Jira with detailed breakdowns by user and date. Perfect for teams using Jira Free!

[![Download Latest Release](https://img.shields.io/github/v/release/Subin-Vidhu/jira-worklog-tracker?label=Download&style=for-the-badge)](https://github.com/Subin-Vidhu/jira-worklog-tracker/releases/latest)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Browser Support](https://img.shields.io/badge/Browser-Chrome%20%7C%20Firefox%20%7C%20Edge-brightgreen.svg?style=for-the-badge)](#installation)

## 🚀 Installation Steps

### 1. Create Extension Folder
Create a new folder on your computer called `jira-worklog-tracker`

### 2. Download Files
Create these files in your extension folder:

#### Required Files:
- `manifest.json` - Extension configuration
- `content.js` - Main extension logic
- `popup.html` - Extension popup interface
- `popup.js` - Popup functionality
- `styles.css` - Extension styles

### 3. Create Icon Files (Optional)
Create simple icon files or download from any free icon site:
- `icon16.png` (16x16px)
- `icon32.png` (32x32px) 
- `icon48.png` (48x48px)
- `icon128.png` (128x128px)

*If you don't have icons, remove the icon references from `manifest.json`*

### 4. Load Extension in Chrome

1. **Open Chrome Extensions Page**:
   - Go to `chrome://extensions/`
   - Or click ⋮ → More Tools → Extensions

2. **Enable Developer Mode**:
   - Toggle "Developer mode" in the top right corner

3. **Load Extension**:
   - Click "Load unpacked"
   - Select your `jira-worklog-tracker` folder
   - Click "Select Folder"

4. **Verify Installation**:
   - You should see "Jira Daily Worklog Tracker" in your extensions list
   - The extension icon will appear in your Chrome toolbar

## 🛠️ Usage Instructions

### Method 1: Using the Button (Recommended)
1. **Navigate to Jira** and run your JQL search:
   ```jql
   assignee = "SUBIN S" AND worklogDate >= "2025-08-26" AND worklogDate <= "2025-08-26"
   ```

2. **Look for the Button**: A blue "📊 Daily Worklog Tracker" button will appear on the page

3. **Click the Button**: This opens the worklog analysis dialog

4. **Enter Details**:
   - **Date**: Select the date you want to analyze
   - **User**: Enter exact user name or leave empty for all users

5. **View Results**: Get detailed breakdowns with totals and individual worklog entries

### Method 2: Using the Extension Popup
1. **Click Extension Icon** in Chrome toolbar
2. **Check Status**: Popup shows if you're on a Jira page
3. **Click "Open Worklog Tracker"** to activate the dialog

## ✨ Features

### 🔍 Smart User Detection
- Automatically finds all users with worklogs on specified date
- Shows exact user names to avoid typos
- Supports partial name matching

### 📊 Detailed Analysis
- **Total time logged** per user/date
- **Breakdown by issue** with clickable links
- **Individual worklog entries** with comments
- **Summary statistics** for easy reporting

### 🎯 Flexible Filtering
- **By Date**: Any date in YYYY-MM-DD format
- **By User**: Specific user or all users
- **By Issues**: Works with current search results

### 📋 Easy Reporting
- **Quick copy summary** for status reports
- **Detailed breakdowns** for time tracking
- **Visual formatting** for easy reading

## 🔧 Troubleshooting

### Extension Not Loading
- Make sure all files are in the same folder
- Check that `manifest.json` is valid JSON
- Refresh the extensions page and try again

### Button Not Appearing
- Refresh the Jira page
- Make sure you're on an issue search page with visible issues
- Try running a JQL search first
- Check browser console for errors

### No Worklogs Found
- Verify the date format is YYYY-MM-DD
- Check that the user name matches exactly (case sensitive)
- Make sure there are actually worklogs for that date
- Try leaving user field empty to see all users first

### API Errors
- Make sure you're logged into Jira
- Check that you have permission to view worklogs
- Some corporate Jira instances may block API access

## 🔒 Privacy & Security

### What the Extension Does:
- ✅ Reads worklog data from your current Jira instance
- ✅ Processes data locally in your browser
- ✅ Shows results in a popup dialog

### What the Extension Does NOT Do:
- ❌ Store any data permanently
- ❌ Send data to external servers
- ❌ Access other websites or tabs
- ❌ Collect personal information

## 📱 Browser Compatibility

- ✅ **Chrome** (Recommended)
- ✅ **Edge** (Chromium-based)
- ✅ **Brave**
- ✅ **Opera**
- ❌ Firefox (requires different manifest format)

## 🆕 Version History

### v1.0.0
- Initial release
- Basic worklog analysis functionality
- User detection and filtering
- Detailed breakdowns and summaries

## 🐛 Common Issues & Solutions

### Issue: "No issues found on this page"
**Solution**: Make sure you're on a Jira issue search results page with visible issues.

### Issue: "HTTP 401/403 errors"
**Solution**: Check your Jira permissions and make sure you're logged in.

### Issue: User name doesn't match
**Solution**: Use the "all users" option first to see exact names, then copy the exact name.

### Issue: Button appears but doesn't work
**Solution**: Try refreshing the page and ensuring the content script loaded properly.

## 💡 Tips for Best Results

1. **Run JQL First**: Always run your JQL search before using the tracker
2. **Check All Users**: Use empty user field first to discover available users
3. **Copy Exact Names**: User names are case-sensitive
4. **Recent Dates**: Extension works best with recent worklog data
5. **Refresh if Needed**: If something doesn't work, try refreshing the page

## 🤝 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Open browser console (F12) to check for errors
3. Try refreshing the page and Jira session
4. Verify your Jira permissions

---
**Made for Jira Free users who need better worklog reporting! 🎯**