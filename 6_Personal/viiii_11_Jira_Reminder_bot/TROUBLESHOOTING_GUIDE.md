# 🔧 Fixing Webhook and User Issues - Step by Step

## 🚨 Current Issues
1. **Webhook Error**: Using test endpoint instead of production webhook
2. **Wrong User Tasks**: Getting Akhila's tasks instead of Subin's tasks

## 🛠 Fix Instructions

### Step 1: Fix Webhook URL Issue

**Problem**: You're accessing `http://localhost:5678/webhook-test/jira-commands`
**Solution**: Use the production webhook URL

1. **Import the debug workflow** `Debug_Jira_Issue.json` first
2. **Get the correct webhook URL** from n8n:
   - Go to your workflow → Click on the webhook node
   - Copy the **Production URL** (not the test URL)
   - It should look like: `http://localhost:5678/webhook/debug-jira`

3. **Set up Telegram webhook** with correct URL:
```bash
curl -X POST "https://api.telegram.org/bot8483914760:AAEEp8Tccbc5blGme5bZOxI-dr1e6WbRopM/setWebhook" \
-H "Content-Type: application/json" \
-d '{"url": "http://YOUR_ACTUAL_IP:5678/webhook/debug-jira"}'
```

### Step 2: Test and Debug the User Issue

1. **Activate the debug workflow** `Debug_Jira_Issue.json`
2. **Send any message to your Telegram bot** (this will trigger the debug)
3. **Check the debug results** - you'll get a detailed analysis showing:
   - What `currentUser()` returns
   - What `subin@aramisimaging.com` returns  
   - What `akhila@aramisimaging.com` returns
   - Analysis of which credential/email is actually working

### Step 3: Fix Based on Debug Results

**Scenario A**: If debug shows `currentUser()` = Akhila
```
🔧 Solution: The Jira credential is linked to Akhila's account
✅ Action: Create new Jira credentials with Subin's account
```

**Scenario B**: If debug shows `subin@aramisimaging.com` = No results
```
🔧 Solution: Email format might be wrong
✅ Action: Try different email formats (username vs full email)
```

**Scenario C**: If debug shows credential authentication issues
```
🔧 Solution: Token or permissions issue
✅ Action: Regenerate Jira API token with Subin's account
```

## 🎯 Quick Debug Steps

### Step 1: Import Debug Workflow
```
1. Go to n8n
2. Import "Debug_Jira_Issue.json"  
3. Activate the workflow
```

### Step 2: Test with Telegram
```
1. Send any message to your Telegram bot
2. Check the response for detailed debug info
```

### Step 3: Identify the Issue
The debug message will tell you exactly what's wrong:
- ❌ Credential linked to wrong user
- ❌ Wrong email format
- ❌ No permissions 
- ✅ Or if everything is working correctly

## 🔍 Manual Jira Check

If you want to verify manually:

1. **Log into Jira Web Interface** with Subin's account
2. **Run this JQL query**: `assignee = currentUser()`
3. **Check if you see your tasks** (not Akhila's)
4. **Try**: `assignee = 'subin@aramisimaging.com'`
5. **Compare results**

## 🚀 After Debugging

Once you identify the issue:

1. **Fix the Jira credentials** (if needed)
2. **Update the main workflows** with correct email/query
3. **Set up proper webhook URL** (production, not test)
4. **Test `/today` command**

## 🆘 Common Solutions

### If Credential = Akhila's Account:
```
1. Go to n8n Settings → Credentials
2. Create NEW "Jira Software Cloud API" credential
3. Use Subin's Jira email and API token
4. Update all workflows to use new credential ID
```

### If Email Format Wrong:
```
Try these in order:
- assignee = 'subin@aramisimaging.com'
- assignee = 'subin'  
- assignee = 'Subin Vidhu'
- assignee in (currentUser())  # if credential is correct
```

### If No Tasks Found:
```
1. Check if Subin has any Jira tasks assigned
2. Verify Jira project access permissions
3. Test with broader JQL: assignee = 'subin@aramisimaging.com' (no status filter)
```

---

**Next Action**: Import the debug workflow and run it to get precise diagnosis! 🔍