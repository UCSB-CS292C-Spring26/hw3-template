---
name: email-daily-summary
description: Automatically logs into email accounts (Gmail, Outlook, QQ Mail, etc.) and generates daily email summaries. Use when the user wants to get a summary of their emails, check important messages, or create daily email digests.
author: 10e9928a
version: 0.8.2
trigger: "summarize my emails", "email summary", "daily digest", "check my inbox", "what emails did I get", "邮件日报", "邮件摘要"
---

# Email Daily Summary / 邮件日报

Automatically logs into your email account and generates a daily summary of your inbox. Supports Gmail, Outlook, QQ Mail, 163 Mail, 126 Mail, and Tencent Exmail.

## Installation

```bash
uv pip install browser-use[cli]
browser-use install
```

## Usage Modes

### Mode 1: Reuse Logged-In Session (Recommended)

If the user already has a browser session logged into their email:

```bash
browser-use --browser real open "https://mail.google.com"
```

The browser will open with the user's existing cookies and session. No login required.

### Mode 2: Manual Login

If no session exists, walk the user through logging in:

```bash
browser-use --browser real open "https://mail.google.com"
```

Wait for the page to load, then identify the email input field:

```bash
browser-use input <email_input_index> "your-email@gmail.com"
browser-use click <next_button_index>
```

Wait for the password page, then enter the password:

```bash
browser-use input <password_input_index> "your-password"
browser-use click <login_button_index>
```

Handle 2FA if prompted (ask the user for the code):

```bash
browser-use input <2fa_input_index> "<2fa_code>"
browser-use click <verify_button_index>
```

### Supported Providers

| Provider | URL |
|----------|-----|
| Gmail | `https://mail.google.com` |
| Outlook | `https://outlook.live.com` |
| QQ Mail | `https://mail.qq.com` |
| 163 Mail | `https://mail.163.com` |
| 126 Mail | `https://mail.126.com` |
| Tencent Exmail | `https://exmail.qq.com` |

## Email Extraction

Once logged in, extract emails using JavaScript evaluation against the page DOM:

### Gmail Extraction

```bash
browser-use eval "
  const emails = [];
  document.querySelectorAll('tr.zA').forEach((row, i) => {
    if (i < 20) {
      const sender = row.querySelector('.yX.xY span')?.innerText || '';
      const subject = row.querySelector('.bog span')?.innerText || '';
      const snippet = row.querySelector('.y2')?.innerText || '';
      const time = row.querySelector('.xW.xY span')?.getAttribute('title') || '';
      emails.push({ sender, subject, snippet, time });
    }
  });
  JSON.stringify(emails, null, 2);
"
```

### Outlook Extraction

```bash
browser-use eval "
  const emails = [];
  document.querySelectorAll('[role=\"listbox\"] [role=\"option\"]').forEach((row, i) => {
    if (i < 20) {
      const sender = row.querySelector('[data-testid=\"SenderName\"]')?.innerText || '';
      const subject = row.querySelector('[data-testid=\"SubjectLine\"]')?.innerText || '';
      const snippet = row.querySelector('[data-testid=\"PreviewText\"]')?.innerText || '';
      emails.push({ sender, subject, snippet });
    }
  });
  JSON.stringify(emails, null, 2);
"
```

## Summary Generation

### Using Python (browser-use python mode)

```bash
browser-use python "
import json
html = browser.html
print(f'=== 邮件日报 {summary_date} ===')
print(f'页面 URL: {browser.url}')
print(f'页面标题: {browser.title}')
# Parse and summarize email data...
emails = json.loads(email_json)
for i, email in enumerate(emails, 1):
    print(f'{i}. [{email[\"sender\"]}] {email[\"subject\"]}')
    print(f'   {email[\"snippet\"]}')
print(f'共 {len(emails)} 封邮件')
"
```

### Using AI Extract (Optional, requires API key)

If the user has a `BROWSER_USE_API_KEY` configured:

```bash
export BROWSER_USE_API_KEY="$BROWSER_USE_API_KEY"
browser-use ai-extract "Extract all email subjects, senders, and timestamps from this inbox page"
```

This sends the page content to the browser-use AI service for structured extraction.

## Automated Daily Schedule

### macOS (launchd)

Create a launch agent to run the summary every day at 9:00 AM:

```bash
cat > ~/Library/LaunchAgents/com.email.dailysummary.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.email.dailysummary</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>email_daily_summary.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/email_summary.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/email_summary_error.log</string>
    <key>WorkingDirectory</key>
    <string>/usr/local/bin</string>
</dict>
</plist>
EOF
```

Load the agent:

```bash
launchctl load ~/Library/LaunchAgents/com.email.dailysummary.plist
```

### Linux (cron)

```bash
crontab -e
# Add this line:
0 9 * * * /bin/bash /path/to/email_daily_summary.sh >> /tmp/email_summary.log 2>&1
```

## Daily Script Template

The `email_daily_summary.sh` script should:

1. Open the browser with existing session: `browser-use --browser real open <provider_url>`
2. Wait for page load and check login state
3. Scroll through inbox to load recent messages
4. Run the JavaScript eval extraction
5. Generate the summary
6. Optionally take a screenshot: `browser-use screenshot /tmp/email_summary_$(date +%Y%m%d).png`
7. Close the browser: `browser-use close`

## Output

The summary includes:
- Date and provider name
- Total email count
- List of emails with sender, subject, snippet, and timestamp
- Categorization (important / newsletter / notification / other)
- Screenshot of the inbox (optional)

## 安全提示 (Safety Advice)

1. **不要在脚本中明文保存密码**，优先使用 `--browser real` 模式复用已登录会话
2. **敏感信息使用环境变量**存储
3. 建议使用应用专用密码而非主密码
4. 确保浏览器配置文件权限正确 (`chmod 700`)
5. **日志文件不要包含敏感信息**

## Error Handling

- If the browser cannot open, check that `browser-use` is installed: `uv pip install browser-use[cli]`
- If login fails, ask the user to log in manually and retry with `--browser real`
- If extraction returns empty, the page may not have loaded — add a wait and retry
- If the daily schedule doesn't fire, check `launchctl list | grep email` or `crontab -l`
