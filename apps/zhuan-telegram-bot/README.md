# Zhuan Telegram Capture Bot MVP

This is a beginner-friendly Telegram bot for quick daily capture into Zhuan_OS.

It runs locally on your laptop, uses Telegram polling, writes captures to the Event Bus JSONL source of truth, rebuilds the SQLite query index, and can optionally keep legacy Markdown fallback files.

## What It Does

- Saves normal Telegram text messages as V1 Event Bus events.
- Supports simple prefixes like `spend:`, `study:`, `assignment:`, `mistake:`, and `principle:`.
- Appends source-of-truth events to `D:\Zhuan_OS\data\events\events-YYYY-MM.jsonl`.
- Rebuilds the SQLite query index at `D:\Zhuan_OS\data\zhuan_os.db`.
- Keeps optional legacy Markdown fallback writes under `agent_workspace/inbox/telegram_inbox/YYYY-MM-DD.md` by default.
- Lets you check your Telegram user ID with `/whoami`.
- Summarizes today's captures by category with `/today`.
- Exports a clean judgment-training Markdown template with `/export`.
- Gives judgment-training templates for before-AI thinking, decisions, mistakes, principles, and weekly review.
- Shows a persistent button menu so you do not need to remember commands.
- Lets any main menu button interrupt the current guided flow and start the new one.
- Saves Telegram photos locally and links them from the daily Markdown inbox.
- Does not use an AI API, webhook, cloud deployment, Bot Assistant, or MCP. SQLite is only a local rebuildable query index.

## How To Create A Bot With BotFather

1. Open Telegram on your phone.
2. Search for `@BotFather`.
3. Send:

```text
/newbot
```

4. Follow BotFather's prompts:
   - Choose a display name, for example `Zhuan Capture Bot`.
   - Choose a username ending in `bot`, for example `zhuan_capture_bot`.
5. BotFather will give you a bot token. Put this value in `BOT_TOKEN`.

Do not paste the token into Git, chat logs, screenshots, or public notes.

## How To Copy Token Into .env

From this folder:

```bat
copy .env.example .env
```

Open `.env` in a text editor and replace:

```text
BOT_TOKEN=replace_with_your_botfather_token
```

with:

```text
BOT_TOKEN=your_real_token_from_botfather
```

`ALLOWED_USER_ID` is Zhuan's numeric Telegram user ID. It is not the bot username.

Leave `ALLOWED_USER_ID` empty on the first run:

```text
ALLOWED_USER_ID=
```

You will fill it after running `/whoami`.

Do not put values like `@zhuan_capture_bot` or `zhuan_capture_bot` into `ALLOWED_USER_ID`.

## Event Bus And Legacy Markdown

Event Bus JSONL is the primary source of truth. Legacy Markdown under `agent_workspace/inbox/telegram_inbox/` is still enabled by default as a local fallback during V1 stabilization.

Set this in `.env` to control legacy Markdown writes:

```text
LEGACY_MARKDOWN_FALLBACK=true
```

Use `false`, `0`, `no`, or `off` to disable legacy Markdown writes after Event Bus confidence is high:

```text
LEGACY_MARKDOWN_FALLBACK=false
```

If Event Bus writing fails, the bot logs the failure without message body content. When legacy fallback is enabled, it attempts to save the capture to Markdown and replies with a clear warning. When fallback is disabled, it replies that the capture was not saved as source of truth.

Safe logs include `event_id`, event `type`, and `source`; logs must not include message bodies, bot tokens, or `.env` values.

## How To Run Locally

Open Command Prompt or PowerShell and run:

```bat
cd /d D:\Zhuan_OS\apps\zhuan-telegram-bot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

Keep this terminal window open while using the bot.

## Button-First Workflow

Use buttons on your phone first. Commands are backup.

You do not need to type `/cancel` during normal use.

Start or reopen the menu with:

```text
/start
/menu
/help
```

Main buttons:

```text
Capture | Today
Decision | Review
Search | More
```

Capture buttons:

```text
Quick Capture | Study Log
Mistake Log | Principle Log
Food / Life | Photo
Back
```

Review buttons:

```text
Night Review | Weekly Review
Mistake Review | Principle Extract
Back
```

More buttons:

```text
Recent | Dashboard Link
Export Today | Health Check
Help | Settings
Back
```
When you are inside a guided flow, the bot shows a smaller keyboard:

```text
⬅️ Back
Quick Capture | Today
```

Tap `Back` to cancel the current flow and return to the main menu.

Any main menu button can interrupt the current flow. For example, if you started a guided flow and then tap another flow button, the bot discards the incomplete answers and starts the new flow.

Cancel options:

```text
/cancel
cancel
取消
back
返回
⬅️ Back
```

Voice typing works because your phone converts speech into normal text before sending it to Telegram.

Real Telegram voice note transcription is not supported yet. If you send a voice note, the bot will ask you to use phone keyboard voice-to-text for now.

## How To Get Your Telegram User ID

1. Keep `ALLOWED_USER_ID` empty in `.env`.
2. Start the bot locally with `python bot.py`.
3. Open your bot in Telegram.
4. Send:

```text
/whoami
```

5. Copy the number returned by the bot.
6. Put that number into `.env`:

```text
ALLOWED_USER_ID=123456789
```

Do not put the bot username here. `ALLOWED_USER_ID` must be the numeric ID returned by `/whoami`.

7. Stop the bot with `Ctrl+C`.
8. Start it again:

```bat
python bot.py
```

After this, other Telegram users will be rejected.

## Why Phone And Laptop Do Not Need Same Wi-Fi

This bot uses Telegram polling.

Your laptop connects outward to Telegram's servers and asks for new messages. Your phone also sends messages to Telegram's servers. Because both devices talk to Telegram over the internet, they do not need to be on the same Wi-Fi network.

## Phone Usage Examples

Use the main menu for the fastest actions:

```text
Capture: open capture actions
Today: show today's SQLite events
Decision: start a decision log
Review: open review actions
Search: shows Use /search keyword
More: open lower-frequency actions
```

Use Capture for event-writing actions:

```text
Quick Capture
Study Log
Mistake Log
Principle Log
Food / Life
Photo
Back
```

Use Review for reflection actions:

```text
Night Review
Weekly Review
Mistake Review
Principle Extract
Back
```

Use More for lower-frequency actions:

```text
Recent
Dashboard Link
Export Today
Health Check
Help
Settings
Back
```

Quick Capture asks one question:

```text
发生了什么？随便写一句。
```

Text prefixes still work as backup:

```text
spend: RM12 lunch
study: Fluid Mechanics pipe loss 1 hour
assignment: Project management Q2 60%
mistake: spent too much time optimizing system
principle: capture first, organize later
```

Useful commands:

```text
/start
/menu
/help
/commands
/cancel
/whoami
/today
/recent
/search keyword
/dashboard
/export
/review
/beforeai
/decision
/mistake text
/principle text
/weekly
```

## Daily Judgment Commands

Buttons are recommended. Commands below are backup when typing is faster.

`/today` shows how many captures you made today and groups them by category.

`/export` returns clean Markdown with these sections:

```text
Daily Capture
Before AI
Judgment
Review
Mistake
Principle
Next Action
```

`/review` gives the daily judgment review template:

```text
## Daily Judgment Review

1. 今天最重要的事情是什么？
2. 你原本怎么判断？
3. 哪个假设错了？
4. 现实结果是什么？
5. 今天最大错误是什么？
6. 今天学到什么？
7. 明天要改变什么？
8. 提炼一句下次规则。
```

`/commands` shows capture examples for:

```text
study:
spend:
exercise:
assignment:
conversation:
mistake:
principle:
review:
```

`/beforeai` helps you think before asking AI:

```text
## Before AI

你现在要问 AI / 解决什么问题？
你的初步判断是什么？
你现在有哪些假设？
你担心哪里错？
你希望 AI 挑战你哪里？
哪个决定必须由你自己判断？
```

`/decision` gives a decision log:

```text
## Decision Log

Decision:
Options:
Why I choose this:
Biggest risk:
What would change my mind:
Expected result:
Review date:
```

`/mistake text` saves a structured mistake under today's `## Mistakes` section:

```text
/mistake accepted AI output without verification
```

It saves:

```text
- Mistake:
- Cause:
- Prevention:
- Principle:
```

`/principle text` saves a structured principle under today's `## Principles` section:

```text
/principle verify before trusting
```

It saves:

```text
- Principle:
- When to use:
- Warning:
- Example:
```

`/weekly` gives a weekly scorecard:

```text
## Weekly Judgment Scorecard

Score 1-5:
- Thought before AI:
- Verified AI output:
- Avoided passive copy-paste:
- Converted mistakes into principles:
- Took real-world action:
- Improved social judgment:
- Improved execution:
```

## Output Format

Primary events are saved here:

```text
D:\Zhuan_OS\data\events\events-YYYY-MM.jsonl
```

The local SQLite query index is rebuilt here:

```text
D:\Zhuan_OS\data\zhuan_os.db
```

When `LEGACY_MARKDOWN_FALLBACK=true`, fallback Markdown is also saved here:

```text
D:\Zhuan_OS\agent_workspace\inbox\telegram_inbox\YYYY-MM-DD.md
```

Each daily file uses this Markdown shape:

```markdown
# Telegram Inbox - YYYY-MM-DD

## Captures

### HH:MM - category
Original:
...

Interpreted:
- Category:
- Tags:
- Worth review: yes/no

## Quick Capture / 随手记录

### HH:MM
- Text:
- Source: Telegram text

## Before AI

## Decisions

## Daily Judgment Review

## Photo Capture / 图片记录

### HH:MM
- File: ../telegram_media/YYYY-MM-DD/HHMMSS_photo_<message_id>.jpg
- Caption:
- Note: Photo saved from Telegram.

## Review Queue

## Mistakes

## Principles
```

## Safety Warning

Do not send secrets, passwords, private keys, bank details, or very private personal data to this bot yet.

This MVP stores local Event Bus JSONL, a rebuildable SQLite index, and optional local Markdown fallback files. Telegram messages still pass through Telegram's service.

Do not touch or send private vault files through the bot.

Never share `BOT_TOKEN` in chat, screenshots, Git, or notes.

Photo safety: do not send private documents, passwords, IC/passport, bank screenshots, API keys, or sensitive images.

Photos are stored locally under:

```text
D:\Zhuan_OS\agent_workspace\inbox\telegram_media\YYYY-MM-DD\
```

## Current Limitation

Your laptop must be awake, connected to the internet, and running `python bot.py`.

If the terminal is closed or the laptop sleeps, the bot will stop responding until you start it again.
