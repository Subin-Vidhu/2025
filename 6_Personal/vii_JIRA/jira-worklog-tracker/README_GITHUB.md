# 🎯 JIRA Daily Worklog Tracker

A Chrome extension that helps you track daily worklogs in Jira with detailed breakdowns by user and date. Perfect for teams using Jira Free!

[![Download Latest Release](https://img.shields.io/github/v/release/Subin-Vidhu/jira-worklog-tracker?label=Download&style=for-the-badge)](https://github.com/Subin-Vidhu/jira-worklog-tracker/releases/latest)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Browser Support](https://img.shields.io/badge/Browser-Chrome%20%7C%20Firefox%20%7C%20Edge-brightgreen.svg?style=for-the-badge)](#installation)

## 🚀 Quick Install

### For Chrome/Edge/Brave:
1. **[Download Latest Release](https://github.com/Subin-Vidhu/jira-worklog-tracker/releases/latest)** 
2. Extract the ZIP file
3. Go to `chrome://extensions/` → Enable Developer Mode → Load Unpacked
4. Select the extracted folder

### For Firefox:
1. **[Download Firefox Version](https://github.com/Subin-Vidhu/jira-worklog-tracker/releases/latest)**
2. Extract `jira-worklog-tracker-firefox.zip`
3. Go to `about:debugging` → This Firefox → Load Temporary Add-on
4. Select `manifest.json` from extracted folder

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

## 🎬 How It Works

1. **Navigate to JIRA** and run your JQL search
2. **Click the "📊 Daily Worklog Tracker" button** that appears
3. **Select date** and optionally specify a user
4. **View detailed worklog breakdown** instantly

### Example JQL Searches:
```jql
assignee = "YOUR_NAME" AND worklogDate >= "2025-08-26"
project = "PROJECT_KEY" AND worklogDate >= "2025-08-26"
worklogAuthor = "YOUR_NAME" AND worklogDate = "2025-08-26"
```

## 💡 Perfect For

- **Daily stand-up meetings** - "What did everyone work on yesterday?"
- **Manager reporting** - "How much time was spent on Project X?"
- **Personal tracking** - "What did I accomplish this week?"
- **Team analysis** - "Who's working on what issues?"

## 🛠️ Installation Guide

### Chrome/Edge/Brave (Manual Installation)

1. **Download** the latest `jira-worklog-tracker.zip` from [Releases](https://github.com/Subin-Vidhu/jira-worklog-tracker/releases)
2. **Extract** the ZIP file to a folder
3. **Open Chrome** and navigate to `chrome://extensions/`
4. **Enable "Developer mode"** (toggle in top-right)
5. **Click "Load unpacked"** and select the extracted folder
6. **Done!** The extension is now installed

### Firefox (Manual Installation)

1. **Download** the `jira-worklog-tracker-firefox.zip` from [Releases](https://github.com/Subin-Vidhu/jira-worklog-tracker/releases)
2. **Extract** the ZIP file
3. **Open Firefox** and go to `about:debugging`
4. **Click "This Firefox"** → **"Load Temporary Add-on"**
5. **Select** the `manifest.json` file from the extracted folder

## 🔧 Usage

### Basic Usage:
1. Navigate to any JIRA page with issues
2. Look for the blue "📊 Daily Worklog Tracker" button
3. Click to open the worklog analyzer
4. Enter date (YYYY-MM-DD format)
5. Optionally enter a specific user name
6. Click "Analyze Worklogs" to see results

### Pro Tips:
- Leave user field empty to discover all users first
- User names are case-sensitive
- Works best with recent worklog data
- Button appears after running JQL searches

## 🆘 Troubleshooting

### Extension Button Not Showing?
- Refresh the JIRA page
- Make sure you're on an issue search page
- Try running a JQL search first

### No Worklogs Found?
- Check the date format (YYYY-MM-DD)
- Verify user name spelling (case sensitive)
- Try leaving user field empty to see all users

### Permission Errors?
- Make sure you're logged into JIRA
- Check that you have worklog view permissions
- Try refreshing your JIRA session

## 🔄 Updates

### Manual Updates:
1. Download the new version from releases
2. Extract to the same folder (overwrite files)
3. Go to `chrome://extensions/` and click the reload button

## 📝 Changelog

### v1.0.0 (Initial Release)
- ✅ Basic worklog analysis functionality
- ✅ User detection and filtering
- ✅ Detailed breakdowns and summaries
- ✅ Support for Jira Cloud and Server
- ✅ Privacy-focused local processing

## 🤝 Contributing

Found a bug or have a feature request?

1. **Issues**: [Report bugs or suggest features](https://github.com/Subin-Vidhu/jira-worklog-tracker/issues)
2. **Pull Requests**: Contributions welcome!
3. **Feedback**: Leave feedback in the issues section

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Support This Project

- ⭐ **Star this repository** if you find it useful
- 🐛 **Report bugs** to help improve it
- 💡 **Suggest features** for future versions
- 🔄 **Share with your team** members

## 🔒 Privacy

- **No data collection** - Everything stays in your browser
- **No external servers** - Uses only JIRA's APIs  
- **No registration required** - Just install and use
- **Open source** - You can see exactly what it does

---

**Made with ❤️ for JIRA users who need better worklog reporting!**

---

## 📊 Browser Compatibility

| Browser | Support | Installation |
|---------|---------|-------------|
| Chrome | ✅ Full | Manual (Developer Mode) |
| Firefox | ✅ Full | Manual (Temporary Add-on) |
| Edge | ✅ Full | Manual (Developer Mode) |
| Brave | ✅ Full | Manual (Developer Mode) |
| Opera | ✅ Full | Manual (Developer Mode) |

---

**Questions? Check the [Installation Guide](INSTALLATION_GUIDE.md) or create an [Issue](https://github.com/Subin-Vidhu/jira-worklog-tracker/issues)!**
