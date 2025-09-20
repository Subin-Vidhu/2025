# Chrome Tabs URL Manager Extension

A lightweight Chrome extension that allows users to easily export all open browser tab URLs for backup, sharing, or organizational purposes.

## 📋 Overview

This Chrome extension provides a simple and efficient way to:
- Extract URLs from all currently open tabs
- Copy the URL list to clipboard
- Download URLs as a text file
- Manage browser sessions effectively

## 🚀 Features

### Core Functionality
- **Export All Tabs**: Instantly collect URLs from all open tabs in the current browser window
- **Clipboard Integration**: One-click copy of all URLs to system clipboard
- **File Export**: Download URLs as a timestamped text file
- **Clean Interface**: Minimalist popup design for quick access

### Technical Features
- **Manifest V3 Compatible**: Built using the latest Chrome extension standards
- **Lightweight**: Minimal permissions and resource usage
- **Error Handling**: Robust error handling for tab access issues
- **Cross-Platform**: Works on Windows, Mac, and Linux

## 📁 Project Structure

```
viii_Chrome_tabs_url_manager/
├── export_tabs_extension/
│   ├── manifest.json     # Extension configuration and metadata
│   ├── popup.html       # User interface for the extension popup
│   ├── popup.js         # Main functionality and event handling
│   ├── tab_export.png   # Extension icon (16x16, 32x32, 48x48, 128x128)
└── README.md           # This documentation file
```

## 📋 File Details

### `manifest.json`
- **Manifest Version**: 3 (latest Chrome extension standard)
- **Permissions**: Only requests `tabs` permission for accessing tab URLs
- **Extension Name**: "Export Tabs URLs"
- **Version**: 1.0
- **Action**: Popup-based interface
- **Icons**: Custom PNG icon (`tab_export.png`) for multiple sizes (16px, 32px, 48px, 128px)

### `popup.html`
- Clean, responsive interface (520px width)
- Large textarea for URL display (60% viewport height)
- Three action buttons: Copy, Download, Close
- Monospace font for better URL readability
- Modern styling with rounded buttons and proper spacing

### `popup.js`
- **Main Function**: `listTabs()` - Queries all tabs and extracts URLs
- **Clipboard API**: Modern `navigator.clipboard.writeText()` for copying
- **File Download**: Creates blob URLs for text file downloads
- **Timestamp Format**: ISO format with safe filename characters
- **Error Handling**: Try-catch blocks with user-friendly error messages

## 🛠 Installation

### Developer Mode Installation
1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top-right corner)
3. Click "Load unpacked"
4. Select the `export_tabs_extension` folder
5. The extension icon will appear in your browser toolbar

### Usage
1. Click the extension icon in the Chrome toolbar
2. The popup will automatically load all open tab URLs
3. Choose your preferred action:
   - **Copy to clipboard**: Copies all URLs for pasting elsewhere
   - **Download .txt**: Downloads a timestamped text file
   - **Close**: Closes the popup window

## 🔧 Technical Implementation

### Permissions
- `tabs`: Required to access tab information (URLs, titles)

### API Usage
- `chrome.tabs.query({})`: Retrieves all tabs regardless of window
- `navigator.clipboard.writeText()`: Modern clipboard API
- `URL.createObjectURL()`: Creates downloadable blob URLs

### Browser Compatibility
- Chrome (Manifest V3 support required)
- Chromium-based browsers (Edge, Brave, etc.)

## 📤 Output Formats

### Clipboard Output
```
https://example1.com
https://example2.com
https://example3.com
```

### Downloaded File
- **Filename Pattern**: `tabs-urls-YYYY-MM-DDTHH-MM-SS-sssZ.txt`
- **Content**: One URL per line
- **Encoding**: UTF-8 plain text

## 🎯 Use Cases

### Personal Productivity
- **Session Backup**: Save current browsing session before closing
- **Research Organization**: Export research tabs for later reference
- **Device Migration**: Transfer open tabs to another device

### Professional Applications
- **Meeting Preparation**: Share relevant links with team members
- **Project Documentation**: Archive project-related resources
- **Client Reports**: Include reference links in deliverables

### Educational Purposes
- **Study Sessions**: Save educational resources for later review
- **Assignment Research**: Export reference materials
- **Course Materials**: Organize learning resources

## 🔒 Privacy & Security

### Data Handling
- **Local Processing**: All operations performed locally in browser
- **No Data Collection**: Extension doesn't store or transmit user data
- **Minimal Permissions**: Only requests necessary tab access
- **No External Connections**: Operates entirely offline

### Security Features
- Modern Manifest V3 security standards
- Content Security Policy compliance
- No external script dependencies
- Safe file download mechanisms

## 🚀 Future Enhancements

### Planned Features
- **Selective Export**: Choose specific tabs to export
- **Format Options**: JSON, CSV, or HTML output formats
- **Window Filtering**: Export tabs from specific browser windows
- **Title Inclusion**: Option to include page titles with URLs
- **Duplicate Detection**: Identify and handle duplicate URLs

### Technical Improvements
- **Bulk Operations**: Handle large numbers of tabs efficiently
- **Progress Indicators**: Show export progress for large tab sets
- **Keyboard Shortcuts**: Add hotkey support for quick access
- **Settings Panel**: User preferences for output format and behavior

## 📝 Development Notes

### Code Quality
- ES6+ async/await syntax
- Modern DOM APIs
- Clean separation of concerns
- Comprehensive error handling

### Performance Considerations
- Efficient tab querying
- Memory-conscious blob handling
- Minimal DOM manipulation
- Fast clipboard operations

## 🤝 Contributing

This extension is part of a personal project collection. For improvements or suggestions:

1. Review the existing code structure
2. Test changes in developer mode
3. Ensure Manifest V3 compliance
4. Verify cross-browser compatibility

## 📄 License

This project is part of a personal development portfolio. The code is provided as-is for educational and personal use purposes.

---

**Created**: 2025 | **Category**: Browser Extensions | **Technology**: Chrome Extension API, JavaScript, HTML/CSS
