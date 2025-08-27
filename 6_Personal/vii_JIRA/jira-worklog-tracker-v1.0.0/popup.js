// Popup script for Jira Worklog Tracker extension

document.addEventListener('DOMContentLoaded', async () => {
  const statusMessage = document.getElementById('status-message');
  const openTrackerBtn = document.getElementById('open-tracker');
  const refreshBtn = document.getElementById('refresh-page');

  // Check if current tab is a Jira page
  async function checkCurrentTab() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      if (!tab.url) {
        updateStatus('error', 'Cannot access current page');
        return;
      }

      const isJiraPage = tab.url.includes('atlassian.net') || 
                        tab.url.includes('jira') ||
                        tab.url.includes('atlassian.com');
      
      if (isJiraPage) {
        updateStatus('success', 'Jira page detected. Extension ready to use.');
        openTrackerBtn.disabled = false;
        openTrackerBtn.textContent = 'Open Worklog Tracker';
      } else {
        updateStatus('error', 'Not a Jira page. Navigate to Jira first.');
        openTrackerBtn.disabled = true;
      }
    } catch (error) {
      updateStatus('error', `Error checking page: ${error.message}`);
      openTrackerBtn.disabled = true;
    }
  }

  function updateStatus(type, message) {
    statusMessage.innerHTML = `<div class="status ${type}"><div>${message}</div></div>`;
  }

  // Open tracker button - send message to content script
  openTrackerBtn.addEventListener('click', async () => {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      
      // Send message to content script to show dialog
      chrome.tabs.sendMessage(tab.id, { action: 'showWorklogDialog' }, (response) => {
        if (chrome.runtime.lastError) {
          // Content script not ready, inject it
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            files: ['content.js']
          }).then(() => {
            // Try sending message again after injection
            setTimeout(() => {
              chrome.tabs.sendMessage(tab.id, { action: 'showWorklogDialog' });
            }, 1000);
          }).catch(error => {
            updateStatus('error', `Failed to load extension: ${error.message}`);
          });
        }
      });
      
      // Close popup
      window.close();
    } catch (error) {
      updateStatus('error', `Failed to activate tracker: ${error.message}`);
    }
  });

  // Refresh button
  refreshBtn.addEventListener('click', async () => {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      await chrome.tabs.reload(tab.id);
      window.close();
    } catch (error) {
      updateStatus('error', `Failed to refresh: ${error.message}`);
    }
  });

  // Initial check
  await checkCurrentTab();
});