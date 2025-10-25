# Subin's Personal Jira Assistant - Complete Setup Guide

## 🎯 Overview
This is your personalized Jira reminder system that works through Telegram. It includes:
- **Automated reminders**: 3 times per day on weekdays
- **Interactive commands**: `/today`, `/log`, `/status`, `/next`
- **Personal focus**: Only shows YOUR tasks and current work
- **Smart prioritization**: Identifies what you should work on next

## 📁 Files Created

### 1. `Subin_Personal_Jira_Assistant.json`
**Purpose**: Main workflow that sends automated reminders
**Triggers**: 9 AM, 2 PM, 5 PM on weekdays
**Features**:
- Shows only tasks assigned to you
- Identifies what you're currently working on
- Recommends next tasks based on priority
- Provides quick stats and interactive buttons

### 2. `Subin_Jira_Command_Handler.json`
**Purpose**: Handles interactive commands and button presses
**Webhook**: Responds to Telegram messages and button clicks
**Commands**:
- `/today` - Detailed daily plan
- `/log TASK-123 2h "description"` - Log time to Jira
- `/status` - Quick status check
- `/next` - Get next task recommendation

## 🚀 Setup Instructions

### Step 1: Import Workflows to n8n
1. Open your n8n interface
2. Go to **Workflows** → **Import from file**
3. Import `Subin_Personal_Jira_Assistant.json`
4. Import `Subin_Jira_Command_Handler.json`

### Step 2: Configure Jira Credentials
Both workflows use the same Jira credentials:
- **Credential ID**: `pgUQDXug0CqSuSyX`
- **Name**: `Jira SW Cloud account`

If this doesn't exist, create new Jira Software Cloud API credentials:
1. Go to **Settings** → **Credentials**
2. Add new **Jira Software Cloud API**
3. Use your Jira domain and API token

### Step 3: Set Up Telegram Webhook
For the command handler to work:
1. Copy the webhook URL from the command handler workflow
2. Set up Telegram webhook:
```bash
curl -X POST "https://api.telegram.org/bot8483914760:AAEEp8Tccbc5blGme5bZOxI-dr1e6WbRopM/setWebhook" \
-H "Content-Type: application/json" \
-d '{"url": "YOUR_N8N_WEBHOOK_URL/webhook/jira-commands"}'
```

### Step 4: Activate Workflows
1. Open `Subin_Personal_Jira_Assistant` → Click **Active** toggle
2. Open `Subin_Jira_Command_Handler` → Click **Active** toggle

## 💬 How to Use

### Automated Reminders
You'll receive messages automatically at:
- **9:00 AM** - Morning planning
- **2:00 PM** - Afternoon check-in  
- **5:00 PM** - End of day review

Each message includes:
- Current work status
- Today's focus tasks
- Quick stats
- Interactive buttons

### Interactive Commands

#### `/today` - Detailed Daily Plan
Shows comprehensive view of your tasks:
- Currently working on
- High priority tasks (do next)
- To-do items
- Other active tasks
- Smart recommendations
- Time logging examples

#### `/log TASK-123 2h "description"` - Time Logging
Log time directly to Jira tasks:
```
/log DEV-456 1h "Fixed login bug"
/log FEAT-789 30m "Code review"
/log BUG-321 2h15m "Testing and debugging"
```

Supported time formats:
- `1h` = 1 hour
- `30m` = 30 minutes  
- `1h30m` = 1 hour 30 minutes
- `2.5h` = 2 hours 30 minutes

#### `/status` - Quick Status Check
Get instant overview:
- Current work
- Priority breakdown
- Total active tasks
- Next action recommendation

#### `/next` - Task Recommendation
Smart task suggestions based on:
- Priority level
- Current status
- Recent updates
- Your current workload

### Interactive Buttons
All messages include quick action buttons:
- **📋 Today's Plan** - Same as `/today`
- **⏰ Log Time** - Time logging help
- **📊 Status Check** - Same as `/status`  
- **➡️ Next Task** - Same as `/next`

## 🎯 Personalization Features

### Task Filtering
- Only shows tasks assigned to **you**
- Filters out completed/closed tasks
- Focuses on active work statuses:
  - In Progress
  - To Do
  - Selected for Development
  - Open

### Smart Prioritization
Tasks are sorted by:
1. **Priority level** (Highest → High → Medium → Low)
2. **Status relevance** (In Progress → To Do → Others)  
3. **Recent activity** (Recently updated first)

### Current Work Detection
Automatically identifies:
- Tasks marked "In Progress" (what you're working on now)
- High priority items that need attention
- Next logical tasks to start

### Focus Recommendations
The system suggests:
- **Single focus**: Encourages completing current work first
- **Priority-based**: Highlights high-priority items
- **Time-aware**: Considers task estimates and time spent

## 🔧 Customization Options

### Modify Schedule
To change reminder times, edit the Schedule Trigger in the main workflow:
- Current: `0 9,14,17 * * 1-5` (9 AM, 2 PM, 5 PM, weekdays)
- Example: `0 8,12,16 * * 1-5` (8 AM, noon, 4 PM, weekdays)

### Adjust Task Filters
Modify the JQL query in Jira nodes:
```sql
assignee in (currentUser()) AND status IN ('In Progress', 'To Do', 'Selected for Development', 'Open') AND status NOT IN ('Done', 'Closed', 'Resolved')
```

Add project filters:
```sql
assignee in (currentUser()) AND project = "YOUR_PROJECT" AND status IN (...)
```

### Change Message Style
Edit the JavaScript formatting functions to:
- Add/remove emoji
- Change message structure
- Include additional Jira fields
- Modify recommendation logic

## 🛠 Troubleshooting

### No Messages Received
1. Check if workflows are **Active**
2. Verify Jira credentials are working
3. Test LLM endpoint connectivity
4. Confirm Telegram bot token is valid

### Commands Not Working
1. Ensure webhook is properly set up
2. Check Telegram webhook status:
```bash
curl "https://api.telegram.org/bot8483914760:AAEEp8Tccbc5blGme5bZOxI-dr1e6WbRopM/getWebhookInfo"
```
3. Verify command handler workflow is active

### Time Logging Fails
1. Check task key format (should be PROJECT-123)
2. Verify you have permission to log time to the task
3. Ensure task exists and is accessible

### Wrong Tasks Showing
1. Verify Jira credentials are for correct account
2. Check JQL query matches your requirements
3. Test JQL directly in Jira to verify results

## 📈 Advanced Features

### Time Tracking Integration
- Logs work directly to Jira time tracking
- Maintains work descriptions
- Supports flexible time formats
- Provides confirmation feedback

### LLM-Powered Insights
- Generates personalized motivational messages
- Provides context-aware recommendations
- Adapts tone based on workload and priorities

### Multi-Project Support
Can be extended to handle multiple projects by:
- Adding project-specific filters
- Creating separate workflows per project
- Using project-based message routing

## 🔒 Security & Privacy

### Access Control
- Only responds to your Telegram user ID (589824303)
- Unauthorized users receive denial message
- Credentials are stored securely in n8n

### Data Privacy
- No sensitive data is logged
- Messages are sent directly to your chat
- Jira access uses secure API tokens

## 📞 Support

If you need help:
1. Check n8n execution logs for errors
2. Test individual workflow nodes
3. Verify all credentials and tokens
4. Review JQL queries in Jira interface

---

**Created for Subin's personal productivity**  
*Last updated: January 2025*