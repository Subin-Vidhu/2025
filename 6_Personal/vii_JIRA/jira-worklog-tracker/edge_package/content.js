// Jira Daily Worklog Tracker - Chrome Extension Content Script

class JiraWorklogTracker {
  constructor() {
    this.initialized = false;
    this.init();
  }

  init() {
    if (this.isJiraPage()) {
      this.addWorklogButton();
      this.observePageChanges();
      this.initialized = true;
    }
  }

  isJiraPage() {
    return window.location.href.includes('atlassian.net') || 
           window.location.href.includes('jira') ||
           document.querySelector('[data-testid="issue-table"]') ||
           document.querySelector('.navigator-content');
  }

  addWorklogButton() {
    // Remove existing button if present
    const existingButton = document.getElementById('worklog-tracker-btn');
    if (existingButton) existingButton.remove();

    // Find a good place to add the button
    const toolbar = this.findToolbar();
    if (toolbar) {
      const button = this.createButton();
      toolbar.appendChild(button);
    }
  }

  findToolbar() {
    const selectors = [
      '[data-testid="issue-table-toolbar"]',
      '.issue-table-toolbar',
      '.navigator-content .search-results-meta',
      '.issue-nav',
      '.issue-header-content',
      '.content-related',
      '.search-results-meta'
    ];

    for (const selector of selectors) {
      const element = document.querySelector(selector);
      if (element) return element;
    }

    // Fallback: create our own toolbar
    const content = document.querySelector('.content-body, .navigator-content, #content, .search-results-count-and-sorting');
    if (content) {
      const toolbar = document.createElement('div');
      toolbar.id = 'worklog-tracker-toolbar';
      toolbar.style.cssText = `
        padding: 10px;
        background: #f4f5f7;
        border: 1px solid #ddd;
        margin-bottom: 10px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        gap: 10px;
      `;
      content.insertBefore(toolbar, content.firstChild);
      return toolbar;
    }

    return null;
  }

  createButton() {
    const button = document.createElement('button');
    button.id = 'worklog-tracker-btn';
    button.innerHTML = 'Daily Worklog Tracker';
    button.className = 'aui-button worklog-tracker-button';
    button.style.cssText = `
      background: #0052cc;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
      margin: 5px;
      font-size: 14px;
      font-weight: 500;
    `;

    button.onmouseover = () => {
      button.style.background = '#0065ff';
    };

    button.onmouseout = () => {
      button.style.background = '#0052cc';
    };

    button.onclick = () => this.openWorklogDialog();
    return button;
  }

  // Fixed method name to match what's being called
  openWorklogDialog() {
    this.showDialog();
  }

  showWorklogDialog() {
    this.showDialog();
  }

  showDialog() {
    // Remove existing dialog
    const existingDialog = document.getElementById('worklog-dialog');
    if (existingDialog) existingDialog.remove();

    const existingBackdrop = document.querySelector('.worklog-backdrop');
    if (existingBackdrop) existingBackdrop.remove();

    const backdrop = this.createBackdrop();
    const dialog = this.createDialog();
    
    document.body.appendChild(backdrop);
    document.body.appendChild(dialog);
  }

  createBackdrop() {
    const backdrop = document.createElement('div');
    backdrop.className = 'worklog-backdrop';
    backdrop.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      z-index: 9999;
    `;
    backdrop.onclick = () => {
      this.closeDialog();
    };
    return backdrop;
  }

  closeDialog() {
    const dialog = document.getElementById('worklog-dialog');
    const backdrop = document.querySelector('.worklog-backdrop');
    
    if (dialog) dialog.remove();
    if (backdrop) backdrop.remove();
  }

  createDialog() {
    const dialog = document.createElement('div');
    dialog.id = 'worklog-dialog';
    dialog.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: white;
      border: 2px solid #0052cc;
      border-radius: 8px;
      padding: 20px;
      width: 500px;
      max-width: 90vw;
      max-height: 80vh;
      overflow-y: auto;
      z-index: 10000;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    const today = new Date().toISOString().split('T')[0];
    const self = this; // Store reference for onclick handlers

    dialog.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h3 style="margin: 0; color: #0052cc;">Daily Worklog Tracker</h3>
        <button id="close-dialog-btn" 
                style="background: none; border: none; font-size: 18px; cursor: pointer; color: #666;">×</button>
      </div>
      
      <div style="margin-bottom: 15px;">
        <label style="display: block; margin-bottom: 5px; font-weight: bold;">Date:</label>
        <input type="date" id="worklog-date" value="${today}" 
               style="width: calc(100% - 16px); padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
      </div>
      
      <div style="margin-bottom: 15px;">
        <label style="display: block; margin-bottom: 5px; font-weight: bold;">User (optional):</label>
        <input type="text" id="worklog-user" placeholder="Leave empty to see all users" 
               style="width: calc(100% - 16px); padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
        <small style="color: #666;">Enter exact display name or leave empty to discover all users</small>
      </div>
      
      <div style="display: flex; gap: 10px;">
        <button id="analyze-btn"
                style="flex: 1; background: #0052cc; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer;">
          Analyze Worklogs
        </button>
        <button id="cancel-btn"
                style="flex: 1; background: #f4f5f7; color: #333; border: 1px solid #ccc; padding: 10px; border-radius: 4px; cursor: pointer;">
          Cancel
        </button>
      </div>
      
      <div id="worklog-results" style="margin-top: 20px;"></div>
    `;

    // Add event listeners after creating the dialog
    setTimeout(() => {
      const closeBtn = document.getElementById('close-dialog-btn');
      const analyzeBtn = document.getElementById('analyze-btn');
      const cancelBtn = document.getElementById('cancel-btn');

      if (closeBtn) closeBtn.onclick = () => self.closeDialog();
      if (analyzeBtn) analyzeBtn.onclick = () => self.analyzeWorklogs();
      if (cancelBtn) cancelBtn.onclick = () => self.closeDialog();
    }, 100);

    return dialog;
  }

  async analyzeWorklogs() {
    const dateInput = document.getElementById('worklog-date');
    const userInput = document.getElementById('worklog-user');
    const resultsDiv = document.getElementById('worklog-results');

    if (!dateInput || !userInput || !resultsDiv) {
      console.error('Required elements not found');
      return;
    }

    const targetDate = dateInput.value;
    const targetUser = userInput.value.trim();

    if (!targetDate) {
      resultsDiv.innerHTML = '<p style="color: red;">Please select a date.</p>';
      return;
    }

    resultsDiv.innerHTML = '<p>Analyzing worklogs... <span style="font-weight: bold;">Loading...</span></p>';

    try {
      const issueKeys = this.getIssueKeysFromPage();
      
      if (issueKeys.length === 0) {
        resultsDiv.innerHTML = `
          <div style="padding: 15px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px;">
            <p><strong>No issues found on this page</strong></p>
            <p>Make sure you're on a Jira issue search page with visible issues.</p>
            <p>Try running a JQL search first.</p>
            <p><strong>Found issues:</strong> ${issueKeys.join(', ')}</p>
          </div>
        `;
        return;
      }

      console.log('Found issues:', issueKeys);
      const worklogData = await this.fetchWorklogsForDate(issueKeys, targetDate, targetUser);
      this.displayResults(worklogData, targetDate, targetUser, resultsDiv);

    } catch (error) {
      console.error('Error analyzing worklogs:', error);
      resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
  }

  getIssueKeysFromPage() {
    const selectors = [
      'a[href*="/browse/"]',
      '[data-testid="issue-table"] a[href*="/browse/"]',
      '.issue-table a[href*="/browse/"]',
      '.navigator-content a[href*="/browse/"]',
      'tr[data-issue-key]',
      '[data-issue-key]'
    ];
    
    let issueKeys = [];
    
    for (const selector of selectors) {
      const elements = document.querySelectorAll(selector);
      console.log(`Selector "${selector}" found ${elements.length} elements`);
      
      if (elements.length > 0) {
        if (selector.includes('data-issue-key')) {
          issueKeys = Array.from(elements).map(el => el.getAttribute('data-issue-key')).filter(key => key);
        } else {
          issueKeys = Array.from(elements).map(link => {
            const href = link.getAttribute('href');
            const match = href.match(/\/browse\/([A-Z]+-\d+)/);
            return match ? match[1] : null;
          }).filter(key => key !== null);
        }
        
        if (issueKeys.length > 0) {
          console.log('Found issue keys:', issueKeys);
          return [...new Set(issueKeys)]; // Remove duplicates
        }
      }
    }
    
    // Fallback: look for issue key patterns in visible text
    const pageText = document.body.innerText;
    const issueKeyPattern = /\b[A-Z]+-\d+\b/g;
    const matches = pageText.match(issueKeyPattern);
    
    if (matches) {
      issueKeys = [...new Set(matches)].slice(0, 10);
      console.log('Found issue keys from text:', issueKeys);
      return issueKeys;
    }
    
    console.log('No issue keys found');
    return [];
  }

  async fetchWorklogsForDate(issueKeys, targetDate, targetUser) {
    const userSummary = new Map();
    
    for (const issueKey of issueKeys) {
      try {
        console.log(`Fetching worklogs for ${issueKey}`);
        const worklogs = await this.getIssueWorklogs(issueKey);
        const dailyWorklogs = worklogs.filter(worklog => {
          const worklogDate = worklog.started.split('T')[0];
          return worklogDate === targetDate;
        });
        
        console.log(`Found ${dailyWorklogs.length} worklogs for ${issueKey} on ${targetDate}`);
        
        dailyWorklogs.forEach(worklog => {
          const author = worklog.author;
          const displayName = author.displayName || author.name || author.emailAddress;
          
          // If specific user requested, filter by that user
          if (targetUser && displayName !== targetUser) return;
          
          if (!userSummary.has(displayName)) {
            userSummary.set(displayName, {
              displayName,
              totalSeconds: 0,
              issues: new Map(),
              worklogCount: 0
            });
          }
          
          const userInfo = userSummary.get(displayName);
          userInfo.totalSeconds += worklog.timeSpentSeconds;
          userInfo.worklogCount++;
          
          if (!userInfo.issues.has(issueKey)) {
            userInfo.issues.set(issueKey, []);
          }
          userInfo.issues.get(issueKey).push(worklog);
        });
      } catch (error) {
        console.warn(`Failed to fetch worklogs for ${issueKey}:`, error);
      }
    }
    
    return userSummary;
  }

  async getIssueWorklogs(issueKey) {
    const response = await fetch(`/rest/api/3/issue/${issueKey}/worklog`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data.worklogs || [];
  }

  displayResults(userSummary, targetDate, targetUser, resultsDiv) {
    if (userSummary.size === 0) {
      resultsDiv.innerHTML = `
        <div style="padding: 15px; background: #f8d7da; border: 1px solid #f5c6cb; border-radius: 4px;">
          <p><strong>No worklogs found</strong></p>
          <p>Date: ${targetDate}</p>
          ${targetUser ? `<p>User: ${targetUser}</p>` : ''}
          <p>Make sure the date and user name are correct.</p>
        </div>
      `;
      return;
    }

    const sortedUsers = Array.from(userSummary.entries()).sort((a, b) => b[1].totalSeconds - a[1].totalSeconds);
    
    let html = `
      <div style="border-top: 2px solid #0052cc; padding-top: 15px;">
        <h4>Worklog Results for ${targetDate}</h4>
    `;

    sortedUsers.forEach(([displayName, info]) => {
      const totalHours = this.secondsToHours(info.totalSeconds);
      const issueCount = info.issues.size;
      
      html += `
        <div style="margin-bottom: 15px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; background: #f9f9f9;">
          <h5 style="margin: 0 0 8px 0; color: #0052cc;">${displayName}</h5>
          <p style="margin: 0 0 8px 0;"><strong>Total: ${totalHours}</strong> (${info.worklogCount} entries across ${issueCount} issues)</p>
          <details style="margin-top: 8px;">
            <summary style="cursor: pointer; color: #0052cc;">View detailed breakdown</summary>
            <div style="margin-top: 10px; padding-left: 15px;">
      `;
      
      info.issues.forEach((worklogs, issueKey) => {
        const issueTotal = worklogs.reduce((sum, log) => sum + log.timeSpentSeconds, 0);
        html += `
          <div style="margin-bottom: 8px;">
            <strong><a href="/browse/${issueKey}" target="_blank" style="color: #0052cc; text-decoration: none;">${issueKey}</a></strong> - ${this.secondsToHours(issueTotal)}
            <ul style="margin: 5px 0; padding-left: 20px;">
        `;
        
        worklogs.forEach(log => {
          const comment = log.comment ? ` - "${log.comment.substring(0, 40)}${log.comment.length > 40 ? '...' : ''}"` : '';
          html += `<li>${this.secondsToHours(log.timeSpentSeconds)}${comment}</li>`;
        });
        
        html += '</ul></div>';
      });
      
      html += '</div></details></div>';
    });

    // Add summary
    const totalTime = sortedUsers.reduce((sum, [, info]) => sum + info.totalSeconds, 0);
    const totalEntries = sortedUsers.reduce((sum, [, info]) => sum + info.worklogCount, 0);
    
    html += `
        <div style="margin-top: 15px; padding: 12px; background: #d1ecf1; border: 1px solid #bee5eb; border-radius: 6px;">
          <h4 style="margin: 0 0 8px 0;">Summary</h4>
          <p style="margin: 0;"><strong>Total Time Logged: ${this.secondsToHours(totalTime)}</strong></p>
          <p style="margin: 0;">Users: ${sortedUsers.length} | Total Entries: ${totalEntries}</p>
          <p style="margin: 0; font-size: 12px; color: #666;">Quick copy: "${targetUser || 'All users'} - ${targetDate}: ${this.secondsToHours(totalTime)}"</p>
        </div>
      </div>
    `;

    resultsDiv.innerHTML = html;
  }

  secondsToHours(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    return hours + (minutes > 0 ? `h ${minutes}m` : 'h');
  }

  observePageChanges() {
    const observer = new MutationObserver(() => {
      if (this.isJiraPage() && !document.getElementById('worklog-tracker-btn')) {
        setTimeout(() => this.addWorklogButton(), 1000);
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  }
}

// Listen for messages from popup
if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'showWorklogDialog') {
      if (window.jiraWorklogTracker) {
        window.jiraWorklogTracker.showDialog();
      } else {
        initializeTracker();
        setTimeout(() => {
          if (window.jiraWorklogTracker) {
            window.jiraWorklogTracker.showDialog();
          }
        }, 500);
      }
      sendResponse({status: 'success'});
    }
  });
}

// Initialize the extension
function initializeTracker() {
  try {
    if (!window.jiraWorklogTracker) {
      window.jiraWorklogTracker = new JiraWorklogTracker();
      console.log('Jira Worklog Tracker initialized');
    }
  } catch (error) {
    console.error('Error initializing Jira Worklog Tracker:', error);
  }
}

// Multiple initialization attempts
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeTracker);
} else {
  initializeTracker();
}

setTimeout(initializeTracker, 1000);

// Export for global access
window.JiraWorklogTracker = JiraWorklogTracker;