🎉 **JIRA Daily Worklog Tracker v1.0.0 - Initial Release**

A Chrome extension that helps you track daily worklogs in JIRA with detailed breakdowns by user and date. Perfect for teams using JIRA Free!

## 📁 Extension Location
`6_Personal/vii_JIRA/jira-worklog-tracker/`

## 🚀 Quick Install

### For Chrome/Edge/Brave:
1. **Download** `jira-worklog-tracker.zip` below
2. **Extract** the ZIP file to a folder
3. **Open Chrome** → Go to `chrome://extensions/`
4. **Enable "Developer Mode"** (toggle in top-right)
5. **Click "Load unpacked"** → Select the extracted folder
6. **Done!** Extension is installed

### For Firefox:
1. **Download** `jira-worklog-tracker-firefox.zip` below
2. **Extract** the ZIP file
3. **Open Firefox** → Go to `about:debugging`
4. **Click "This Firefox"** → **"Load Temporary Add-on"**
5. **Select** the `manifest.json` file from extracted folder

## ✨ Features

🎯 **Smart Worklog Analysis**
- Analyze worklogs for any date with one click
- Filter by specific users or view all team members
- Automatic user detection and suggestion

📊 **Detailed Breakdowns**
- Total time logged per user
- Time breakdown by issue with clickable links
- Individual worklog entries with comments
- Summary statistics for easy reporting

⚡ **Easy Integration**
- Works seamlessly with Jira Cloud and Server
- Automatically detects Jira pages
- No configuration required
- Respects your existing Jira permissions

🔒 **Privacy & Security**
- All processing happens locally in your browser
- No data stored or transmitted externally
- Uses your existing Jira authentication
- No tracking or analytics

## 🎯 Perfect For

- **Daily stand-up meetings** - "What did everyone work on yesterday?"
- **Manager reporting** - "How much time was spent on Project X?"
- **Personal tracking** - "What did I accomplish this week?"
- **Team analysis** - "Who's working on what issues?"

## 🛠️ How to Use

1. **Navigate to JIRA** and run your JQL search:
   ```jql
   assignee = "YOUR_NAME" AND worklogDate >= "2025-08-26"
   project = "PROJECT_KEY" AND worklogDate >= "2025-08-26"
   ```

2. **Look for the blue button**: "📊 Daily Worklog Tracker"
3. **Click the button** to open the analyzer
4. **Enter date** (YYYY-MM-DD format) and optionally a user name
5. **View detailed results** with time breakdowns and summaries

## 📋 What's Included

- ✅ **Chrome/Edge/Brave extension** (`jira-worklog-tracker.zip`)
- ✅ **Firefox extension** (`jira-worklog-tracker-firefox.zip`)
- ✅ **Microsoft Edge extension** (`jira-worklog-tracker-edge.zip`)
- ✅ **Complete documentation** and installation guides
- ✅ **Privacy policy** and usage instructions

## 🔧 Browser Compatibility

| Browser | Support | Installation Method |
|---------|---------|-------------------|
| Chrome | ✅ Full | Developer Mode (Manual) |
| Firefox | ✅ Full | Temporary Add-on (Manual) |
| Edge | ✅ Full | Developer Mode (Manual) |
| Brave | ✅ Full | Developer Mode (Manual) |
| Opera | ✅ Full | Developer Mode (Manual) |

## 🆘 Troubleshooting

### Extension Button Not Showing?
- Refresh the JIRA page
- Make sure you're on an issue search page with visible issues
- Try running a JQL search first

### No Worklogs Found?
- Check the date format is YYYY-MM-DD
- Verify user name spelling (case sensitive)
- Try leaving user field empty to see all users first

### Permission Errors?
- Make sure you're logged into JIRA
- Check that you have worklog view permissions
- Try refreshing your JIRA session

## 🔄 Updates

This extension updates manually. To update:
1. Download the new version from releases
2. Extract to the same folder (overwrite files)
3. Go to `chrome://extensions/` and click the reload button

## 🤝 Support & Feedback

- **Documentation**: Check the README files in the extension folder
- **Issues**: [Report problems or suggest features](https://github.com/Subin-Vidhu/2025/issues)
- **Source Code**: [View on GitHub](https://github.com/Subin-Vidhu/2025/tree/main/6_Personal/vii_JIRA/jira-worklog-tracker)

---

## 🔒 Privacy Statement

- **No data collection** - Everything stays in your browser
- **No external servers** - Uses only JIRA's APIs
- **No registration required** - Just install and use
- **Open source** - You can see exactly what it does

---

**🆓 Completely FREE - No registration, fees, or subscriptions required!**

**Made with ❤️ for JIRA users who need better worklog reporting!**
