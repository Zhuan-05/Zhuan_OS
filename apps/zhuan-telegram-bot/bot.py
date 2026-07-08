from __future__ import annotations

import html
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from event_adapter import DEFAULT_EVENT_BUS_CONFIG, record_capture_event, record_flow_event


APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parents[1]
INBOX_DIR = ROOT_DIR / "08_Logs" / "telegram_inbox"
MEDIA_DIR = ROOT_DIR / "08_Logs" / "telegram_media"

BUTTON_BEFORE_AI = "Think Before AI"
BUTTON_QUICK_CAPTURE = "Quick Capture"
BUTTON_STUDY_LOG = "Study Log"
BUTTON_ASSIGNMENT_PROJECT = "Assignment / Project"
BUTTON_DECISION = "⚖️ Decision Log"
BUTTON_CONVERSATION_LOG = "Conversation Log"
BUTTON_MISTAKE = "❌ Mistake Log"
BUTTON_PRINCIPLE = "Principle Log"
BUTTON_NIGHT_REVIEW = "Night Review"
BUTTON_TODAY = "Today Summary"
BUTTON_EXPORT = "Export Today"
BUTTON_HELP = "❓ Help"
BUTTON_BACK = "⬅️ Back"

MAIN_MENU_BUTTONS = [
    [BUTTON_BEFORE_AI, BUTTON_QUICK_CAPTURE],
    [BUTTON_STUDY_LOG, BUTTON_ASSIGNMENT_PROJECT],
    [BUTTON_DECISION, BUTTON_CONVERSATION_LOG],
    [BUTTON_MISTAKE, BUTTON_PRINCIPLE],
    [BUTTON_NIGHT_REVIEW, BUTTON_TODAY],
    [BUTTON_EXPORT, BUTTON_HELP],
]
MAIN_MENU_BUTTON_SET = {button for row in MAIN_MENU_BUTTONS for button in row}
CANCEL_TEXTS = {"/cancel", "cancel", "back", "取消", "返回", BUTTON_BACK}
FLOW_BUTTONS = [
    [BUTTON_BACK],
    [BUTTON_QUICK_CAPTURE, BUTTON_TODAY],
]

MENU_BUTTON_TO_FLOW = {
    BUTTON_BEFORE_AI: "before_ai",
    BUTTON_QUICK_CAPTURE: "quick_capture",
    BUTTON_STUDY_LOG: "study_log",
    BUTTON_ASSIGNMENT_PROJECT: "assignment_project",
    BUTTON_DECISION: "decision",
    BUTTON_CONVERSATION_LOG: "conversation_log",
    BUTTON_MISTAKE: "mistake",
    BUTTON_PRINCIPLE: "principle",
    BUTTON_NIGHT_REVIEW: "review",
}

QUICK_CAPTURE_BUTTONS = [
    ["Study", "Spend", "Exercise"],
    ["Assignment", "Conversation"],
    ["Video", "Book", "Cook"],
    ["Idea", BUTTON_BACK],
]

QUICK_CAPTURE_CATEGORIES = {
    "Study": "study",
    "Spend": "spend",
    "Exercise": "exercise",
    "Assignment": "assignment",
    "Conversation": "conversation",
    "Video": "video",
    "Book": "book",
    "Cook": "cook",
    "Idea": "idea",
}

MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(MAIN_MENU_BUTTONS, resize_keyboard=True)
QUICK_CAPTURE_KEYBOARD = ReplyKeyboardMarkup(QUICK_CAPTURE_BUTTONS, resize_keyboard=True)
FLOW_KEYBOARD = ReplyKeyboardMarkup(FLOW_BUTTONS, resize_keyboard=True)

CATEGORY_PREFIXES = {
    "spend": "spend",
    "expense": "spend",
    "exercise": "exercise",
    "study": "study",
    "assignment": "assignment",
    "idea": "idea",
    "conversation": "conversation",
    "video": "video",
    "book": "book",
    "cook": "cook",
    "mistake": "mistake",
    "principle": "principle",
    "review": "review",
}

REVIEW_TEMPLATE = """## Daily Judgment Review

1. 今天最重要的事情是什么？
2. 你原本怎么判断？
3. 哪个假设错了？
4. 现实结果是什么？
5. 今天最大错误是什么？
6. 今天学到什么？
7. 明天要改变什么？
8. 提炼一句下次规则。"""

BEFORE_AI_TEMPLATE = """## Before AI

你现在要问 AI / 解决什么问题？
你的初步判断是什么？
你现在有哪些假设？
你担心哪里错？
你希望 AI 挑战你哪里？
哪个决定必须由你自己判断？"""

DECISION_TEMPLATE = """## Decision Log

Decision:
Options:
Why I choose this:
Biggest risk:
What would change my mind:
Expected result:
Review date:"""

WEEKLY_TEMPLATE = """## Weekly Judgment Scorecard

Score 1-5:
- Thought before AI:
- Verified AI output:
- Avoided passive copy-paste:
- Converted mistakes into principles:
- Took real-world action:
- Improved social judgment:
- Improved execution:

Questions:
1. What mistake repeated this week?
2. What decision improved?
3. Which AI/tool helped most?
4. Where did AI make me passive?
5. What workflow should I improve next week?"""

WELCOME_MESSAGE = """━━━━━━━━━━━━━━
Zhuan Growth System
AI Judgment Training Companion
━━━━━━━━━━━━━━

欢迎回来，Zhuan。

这个 Bot 不是生活流水账。
它是你的 AI 判断训练入口。

今天目标：
1. 先思考
2. 再行动
3. 记录错误
4. 提炼原则
5. 晚上复盘

Choose an action below:"""

HELP_TEXT = """Think Before AI
问 AI 前先写自己的判断，避免被 AI 带着走。

Quick Capture
随手记录一件事，不需要整理。

Study Log
记录今天学了什么、哪里不懂、下一步怎么学。

Assignment / Project
记录作业或项目进度、卡点和下一步。

⚖️ Decision Log
记录重要选择、理由、风险和回看日期。

Conversation Log
训练社会化能力：记录沟通对象、对方关心什么、下次如何表达更好。

❌ Mistake Log
把错误转化成可复用经验。

Principle Log
把经验提炼成以后还能用的原则。

Night Review
晚上复盘今天的判断、错误和下一步。

Today Summary
查看今天保存了什么。

Export Today
导出今天 Markdown。"""

SAVE_CONFIRMATION = "已保存。这个记录会帮助你训练判断力。"
QUICK_CAPTURE_FALLBACK_MESSAGE = "已保存为 Quick Capture。你也可以直接按按钮进入更具体的记录。"
VOICE_NOTE_MESSAGE = "目前请使用手机键盘的语音转文字输入。真正 voice note transcription 下一阶段再做。"

COMMAND_EXAMPLES = f"""{HELP_TEXT}

Backup commands:
/menu - show button menu
/cancel - cancel current flow
/today - category summary for today
/export - clean Markdown for daily judgment review
/review - daily judgment review template
/beforeai - think before asking AI
/decision - decision log template
/mistake text - save a structured mistake
/principle text - save a structured principle
/weekly - weekly judgment scorecard
/whoami - show your Telegram user ID

Text prefix backup:
study:
spend:
exercise:
assignment:
conversation:
video:
book:
cook:
idea:
mistake:
principle:
review:"""

FLOW_DEFINITIONS = {
    "before_ai": {
        "section": "## Before AI",
        "questions": [
            "你现在要问 AI / 解决什么问题？",
            "你的初步判断是什么？",
            "你现在有哪些假设？",
            "你担心哪里错？",
            "你希望 AI 挑战你哪里？",
            "哪个决定必须由你自己判断？",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
    "quick_capture": {
        "section": "## Captures",
        "questions": [
            "发生了什么？随便写一句。",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
    "study_log": {
        "section": "## Study Log",
        "questions": [
            "今天学了什么？",
            "哪里还不懂？",
            "下一步怎么学？",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
    "assignment_project": {
        "section": "## Assignment / Project",
        "questions": [
            "今天推进了什么 assignment / project？",
            "当前进度是多少？",
            "最大卡点是什么？",
            "下一步是什么？",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
    "decision": {
        "section": "## Decisions",
        "questions": [
            "你做了什么决定？",
            "有哪些选择？",
            "为什么这样选？",
            "最大风险是什么？",
            "什么情况会让你改变判断？",
            "什么时候回看这个决定？",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
    "conversation_log": {
        "section": "## Conversation Log",
        "questions": [
            "今天和谁有重要沟通？",
            "对方真正关心什么？",
            "你表达得好不好？",
            "下次如何更好？",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
    "review": {
        "section": "## Daily Judgment Review",
        "questions": [
            "今天最重要的事情是什么？",
            "你原本怎么判断？",
            "现实结果是什么？",
            "哪个假设错了？",
            "今天最大错误是什么？",
            "今天学到什么？",
            "明天要改变什么？",
            "提炼一句下次规则。",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
    "mistake": {
        "section": "## Mistakes",
        "questions": [
            "今天犯了什么错误？",
            "原因是什么？",
            "下次如何避免？",
            "可以形成什么原则？",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
    "principle": {
        "section": "## Principles",
        "questions": [
            "你今天学到什么以后还能用的规则？",
            "什么时候使用？",
            "使用时要小心什么？",
            "举一个例子。",
        ],
        "confirmation": SAVE_CONFIRMATION,
    },
}

ALLOWED_USER_ID_ERROR = (
    "ALLOWED_USER_ID must be your numeric Telegram user ID, not bot username. "
    "Leave it empty first, run /whoami, then paste the number."
)


def today_file(now: datetime | None = None) -> Path:
    current = now or datetime.now()
    return INBOX_DIR / f"{current:%Y-%m-%d}.md"



def record_telegram_capture(
    text: str,
    *,
    category: str = "capture",
    metadata: dict[str, object] | None = None,
    occurred_at: str | None = None,
) -> dict[str, object]:
    return record_capture_event(
        text,
        category=category,
        config=DEFAULT_EVENT_BUS_CONFIG,
        occurred_at=occurred_at,
        metadata=metadata,
    )


def record_telegram_flow(
    flow_name: str,
    answers: list[str],
    *,
    metadata: dict[str, object] | None = None,
) -> dict[str, object]:
    return record_flow_event(
        flow_name,
        answers,
        config=DEFAULT_EVENT_BUS_CONFIG,
        metadata=metadata,
    )
def is_cancel_text(text: str) -> bool:
    stripped = text.strip()
    return stripped in CANCEL_TEXTS or stripped.lower() in CANCEL_TEXTS


def is_main_menu_button(text: str) -> bool:
    return text in MAIN_MENU_BUTTON_SET


def build_photo_paths(now: datetime, message_id: int) -> tuple[Path, str]:
    date_label = f"{now:%Y-%m-%d}"
    file_name = f"{now:%H%M%S}_photo_{message_id}.jpg"
    media_path = MEDIA_DIR / date_label / file_name
    markdown_link = f"../telegram_media/{date_label}/{file_name}"
    return media_path, markdown_link


def build_photo_item(now: datetime, markdown_link: str, caption: str) -> str:
    return (
        f"### {now:%H:%M}\n"
        f"- File: {markdown_link}\n"
        f"- Caption: {caption.strip()}\n"
        "- Note: Photo saved from Telegram.\n"
    )


def build_photo_entry(now: datetime, markdown_link: str, caption: str) -> str:
    return "## Photo Capture / 图片记录\n\n" + build_photo_item(now, markdown_link, caption)


def build_quick_capture_item(text: str, now: datetime) -> str:
    return (
        f"### {now:%H:%M}\n"
        f"- Text: {text.strip()}\n"
        "- Source: Telegram text\n"
    )


def build_quick_capture_entry(text: str, now: datetime) -> str:
    return "## Quick Capture / 随手记录\n\n" + build_quick_capture_item(text, now)


def ensure_today_file(path: Path, now: datetime | None = None) -> None:
    if path.exists():
        return

    current = now or datetime.now()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"# Telegram Inbox - {current:%Y-%m-%d}\n\n"
        "## Captures\n\n"
        "## Quick Capture / 随手记录\n\n"
        "## Before AI\n\n"
        "## Decisions\n\n"
        "## Daily Judgment Review\n\n"
        "## Photo Capture / 图片记录\n\n"
        "## Review Queue\n\n"
        "## Mistakes\n\n"
        "## Principles\n",
        encoding="utf-8",
    )


def parse_capture(text: str) -> dict[str, object]:
    stripped = text.strip()
    lower = stripped.lower()

    category = "capture"
    body = stripped

    for prefix, mapped_category in CATEGORY_PREFIXES.items():
        marker = f"{prefix}:"
        if lower.startswith(marker):
            category = mapped_category
            body = stripped[len(marker) :].strip()
            break

    tags = [category]
    worth_review = category in {"mistake", "principle", "review", "idea", "assignment"}

    return {
        "category": category,
        "body": body,
        "tags": tags,
        "worth_review": worth_review,
    }


def build_capture_block(text: str, now: datetime | None = None) -> str:
    current = now or datetime.now()
    parsed = parse_capture(text)
    tags = ", ".join(f"#{tag}" for tag in parsed["tags"])
    worth_review = "yes" if parsed["worth_review"] else "no"

    return (
        f"### {current:%H:%M} - {parsed['category']}\n"
        "Original:\n"
        f"{text.strip()}\n\n"
        "Interpreted:\n"
        f"- Category: {parsed['category']}\n"
        f"- Tags: {tags}\n"
        f"- Worth review: {worth_review}\n\n"
    )


def insert_capture(path: Path, block: str) -> None:
    ensure_today_file(path)
    content = path.read_text(encoding="utf-8")
    marker = "## Review Queue"

    if marker not in content:
        content = content.rstrip() + "\n\n## Review Queue\n\n## Principles\n"

    content = content.replace(marker, f"{block}{marker}", 1)
    path.write_text(content, encoding="utf-8")


def build_mistake_entry(text: str) -> str:
    return (
        f"- Mistake: {text.strip()}\n"
        "- Cause:\n"
        "- Prevention:\n"
        "- Principle:\n"
    )


def build_principle_entry(text: str) -> str:
    return (
        f"- Principle: {text.strip()}\n"
        "- When to use:\n"
        "- Warning:\n"
        "- Example:\n"
    )


def build_guided_entry(heading: str, labels: list[str], answers: list[str]) -> str:
    lines = [heading, ""]
    for label, answer in zip(labels, answers):
        clean_label = label.rstrip(":")
        lines.append(f"- {clean_label}: {answer.strip()}")
    return "\n".join(lines).strip() + "\n"


def build_mistake_entry_from_answers(answers: list[str]) -> str:
    mistake = answers[0] if len(answers) > 0 else ""
    cause = answers[1] if len(answers) > 1 else ""
    prevention = answers[2] if len(answers) > 2 else ""
    principle = answers[3] if len(answers) > 3 else ""
    return (
        f"- Mistake: {mistake.strip()}\n"
        f"- Cause: {cause.strip()}\n"
        f"- Prevention: {prevention.strip()}\n"
        f"- Principle: {principle.strip()}\n"
    )


def build_principle_entry_from_answers(answers: list[str]) -> str:
    principle = answers[0] if len(answers) > 0 else ""
    when_to_use = answers[1] if len(answers) > 1 else ""
    warning = answers[2] if len(answers) > 2 else ""
    example = answers[3] if len(answers) > 3 else ""
    return (
        f"- Principle: {principle.strip()}\n"
        f"- When to use: {when_to_use.strip()}\n"
        f"- Warning: {warning.strip()}\n"
        f"- Example: {example.strip()}\n"
    )


def append_section_entry(content: str, heading: str, entry: str) -> str:
    clean_entry = entry.strip() + "\n"

    if heading not in content:
        section = f"{heading}\n\n{clean_entry}\n"
        if heading == "## Mistakes" and "## Principles" in content:
            return content.replace("## Principles", f"{section}## Principles", 1)
        return content.rstrip() + f"\n\n{section}"

    start = content.index(heading)
    search_from = start + len(heading)
    next_heading = content.find("\n## ", search_from)

    if next_heading == -1:
        return content.rstrip() + f"\n\n{clean_entry}"

    before = content[:next_heading].rstrip()
    after = content[next_heading:]
    return f"{before}\n\n{clean_entry}{after}"


def append_entry_to_today(section_heading: str, entry: str) -> Path:
    path = today_file()
    ensure_today_file(path)
    content = path.read_text(encoding="utf-8")
    updated = append_section_entry(content, section_heading, entry)
    path.write_text(updated, encoding="utf-8")
    return path


def append_photo_entry_to_today(markdown_link: str, caption: str, now: datetime) -> Path:
    return append_entry_to_today(
        "## Photo Capture / 图片记录",
        build_photo_item(now, markdown_link, caption),
    )


def append_quick_capture_to_today(text: str, now: datetime | None = None) -> Path:
    current = now or datetime.now()
    return append_entry_to_today(
        "## Quick Capture / 随手记录",
        build_quick_capture_item(text, current),
    )


def build_flow_entry(flow_name: str, answers: list[str]) -> tuple[str, str]:
    flow = FLOW_DEFINITIONS[flow_name]
    section = str(flow["section"])
    questions = list(flow["questions"])

    if flow_name == "mistake":
        return section, build_mistake_entry_from_answers(answers)
    if flow_name == "principle":
        return section, build_principle_entry_from_answers(answers)

    entry = build_guided_entry("", questions, answers)
    return section, entry


def build_categorized_capture_text(category: str, text: str) -> str:
    return f"{category}: {text.strip()}"


def extract_captures(content: str) -> list[dict[str, str]]:
    lines = content.splitlines()
    captures: list[dict[str, str]] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.startswith("### "):
            index += 1
            continue

        header = line.removeprefix("### ").strip()
        captured_at, separator, category = header.partition(" - ")
        if not separator:
            captured_at = "unknown"
            category = "capture"

        original_lines: list[str] = []
        index += 1

        while index < len(lines) and lines[index] != "Original:":
            index += 1

        if index < len(lines) and lines[index] == "Original:":
            index += 1
            while index < len(lines) and lines[index].strip():
                original_lines.append(lines[index])
                index += 1

        captures.append(
            {
                "time": captured_at.strip(),
                "category": category.strip(),
                "original": "\n".join(original_lines).strip(),
            }
        )

    return captures


def build_today_summary(content: str) -> str:
    captures = extract_captures(content)
    if not captures:
        return "No captures for today yet."

    counts: dict[str, int] = {}
    for capture in captures:
        category = capture["category"]
        counts[category] = counts.get(category, 0) + 1

    lines = [f"Total captures: {len(captures)}", "", "By category:"]
    for category in sorted(counts):
        lines.append(f"- {category}: {counts[category]}")

    return "\n".join(lines)


def build_clean_export(content: str, date_label: str) -> str:
    captures = extract_captures(content)

    lines = [
        f"# Daily Capture - {date_label}",
        "",
        "## Daily Capture",
    ]

    if captures:
        for capture in captures:
            original = capture["original"] or "(empty)"
            lines.append(f"- {capture['time']} [{capture['category']}] {original}")
    else:
        lines.append("- No captures yet.")

    lines.extend(
        [
            "",
            "## Before AI",
            "- What did I notice before asking AI?",
            "",
            "## Judgment",
            "- My initial judgment:",
            "- What I assumed:",
            "- What evidence I had:",
            "",
            "## Review",
            "- What reality taught me:",
            "- What changed after review:",
            "",
            "## Mistake",
            "- Biggest mistake:",
            "- Why it happened:",
            "",
            "## Principle",
            "- Principle extracted:",
            "- Where to apply it next:",
            "",
            "## Next Action",
            "- Next action:",
        ]
    )

    return "\n".join(lines)


def read_allowed_user_id() -> int | None:
    raw_value = os.getenv("ALLOWED_USER_ID", "").strip()
    if not raw_value:
        return None
    if not raw_value.isdecimal():
        print(ALLOWED_USER_ID_ERROR, file=sys.stderr)
        raise SystemExit(1)
    return int(raw_value)


def is_allowed(update: Update) -> bool:
    allowed_user_id = read_allowed_user_id()
    if allowed_user_id is None:
        return True

    user = update.effective_user
    return user is not None and user.id == allowed_user_id


async def reject_if_not_allowed(update: Update) -> bool:
    if is_allowed(update):
        return False
    if update.effective_message:
        await update.effective_message.reply_text("This bot is not configured for your Telegram user ID.")
    return True


async def reply_with_main_menu(update: Update, text: str) -> None:
    await update.message.reply_text(text, reply_markup=MAIN_MENU_KEYBOARD)


def clear_active_flow(context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("flow", None)
    context.user_data.pop("quick_capture_category", None)


def cancel_active_flow(context: ContextTypes.DEFAULT_TYPE) -> str:
    clear_active_flow(context)
    return "已返回主菜单。"


def start_guided_flow(context: ContextTypes.DEFAULT_TYPE, flow_name: str) -> str:
    flow = FLOW_DEFINITIONS[flow_name]
    context.user_data["flow"] = {
        "name": flow_name,
        "answers": [],
    }
    return str(flow["questions"][0])


def start_main_menu_button_flow(context: ContextTypes.DEFAULT_TYPE, text: str) -> str | None:
    clear_active_flow(context)
    flow_name = MENU_BUTTON_TO_FLOW.get(text)
    if flow_name is None:
        return None
    return start_guided_flow(context, flow_name)


async def show_today_summary(update: Update) -> None:
    path = today_file()
    if not path.exists():
        await update.message.reply_text("No captures for today yet.")
        return

    content = path.read_text(encoding="utf-8")
    summary = build_today_summary(content)
    await update.message.reply_text(f"{summary}\n\nSaved at:\n{path}")


async def show_export(update: Update) -> None:
    path = today_file()
    if not path.exists():
        await update.message.reply_text("No Markdown export for today yet.")
        return

    content = path.read_text(encoding="utf-8")
    export_content = build_clean_export(content, path.stem)
    escaped = html.escape(export_content)
    await update.message.reply_text(f"<pre>{escaped}</pre>", parse_mode=ParseMode.HTML)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    clear_active_flow(context)
    await reply_with_main_menu(
        update,
        WELCOME_MESSAGE
    )


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    clear_active_flow(context)
    await reply_with_main_menu(update, "Choose an action below:")


async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    user = update.effective_user
    if user is None:
        return
    await update.message.reply_text(f"Your Telegram user ID is: {user.id}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    clear_active_flow(context)
    await update.message.reply_text(COMMAND_EXAMPLES, reply_markup=MAIN_MENU_KEYBOARD)


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    await update.message.reply_text(COMMAND_EXAMPLES)


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    await show_today_summary(update)


async def export(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    await show_export(update)


async def review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    await update.message.reply_text(REVIEW_TEMPLATE)


async def beforeai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    await update.message.reply_text(BEFORE_AI_TEMPLATE)


async def decision(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    await update.message.reply_text(DECISION_TEMPLATE)


async def mistake(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Use: /mistake text")
        return

    record_telegram_capture(text, category="mistake", metadata={"entrypoint": "command"})
    path = append_entry_to_today("## Mistakes", build_mistake_entry(text))
    await update.message.reply_text(f"Mistake saved.\nSaved to:\n{path}")


async def principle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    text = " ".join(context.args).strip()
    if not text:
        await update.message.reply_text("Use: /principle text")
        return

    record_telegram_capture(text, category="principle", metadata={"entrypoint": "command"})
    path = append_entry_to_today("## Principles", build_principle_entry(text))
    await update.message.reply_text(f"Principle saved.\nSaved to:\n{path}")


async def weekly(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    await update.message.reply_text(WEEKLY_TEMPLATE)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    await reply_with_main_menu(update, cancel_active_flow(context))


async def handle_button_or_flow(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> bool:
    if is_cancel_text(text):
        await reply_with_main_menu(update, cancel_active_flow(context))
        return True

    if is_main_menu_button(text):
        question = start_main_menu_button_flow(context, text)
        if question is not None:
            await update.message.reply_text(question, reply_markup=FLOW_KEYBOARD)
            return True
        if text == BUTTON_TODAY:
            await show_today_summary(update)
            return True
        if text == BUTTON_EXPORT:
            await show_export(update)
            return True
        if text == BUTTON_HELP:
            await update.message.reply_text(COMMAND_EXAMPLES, reply_markup=MAIN_MENU_KEYBOARD)
            return True
        return True

    quick_category = context.user_data.get("quick_capture_category")
    if quick_category:
        categorized_text = build_categorized_capture_text(str(quick_category), text)
        record_telegram_capture(categorized_text, category=str(quick_category), metadata={"entrypoint": "quick_category"})
        path = today_file()
        block = build_capture_block(categorized_text)
        insert_capture(path, block)
        clear_active_flow(context)
        await reply_with_main_menu(update, SAVE_CONFIRMATION)
        return True

    active_flow = context.user_data.get("flow")
    if active_flow:
        flow_name = str(active_flow["name"])
        flow = FLOW_DEFINITIONS[flow_name]
        answers = list(active_flow["answers"])
        answers.append(text.strip())
        active_flow["answers"] = answers
        questions = list(flow["questions"])

        if len(answers) < len(questions):
            context.user_data["flow"] = active_flow
            await update.message.reply_text(str(questions[len(answers)]), reply_markup=FLOW_KEYBOARD)
            return True

        record_telegram_flow(flow_name, answers, metadata={"entrypoint": "guided_flow"})
        if flow_name == "quick_capture":
            append_quick_capture_to_today(answers[0])
        else:
            section, entry = build_flow_entry(flow_name, answers)
            append_entry_to_today(section, entry)
        clear_active_flow(context)
        await reply_with_main_menu(update, str(flow["confirmation"]))
        return True

    if text in QUICK_CAPTURE_CATEGORIES:
        category = QUICK_CAPTURE_CATEGORIES[text]
        context.user_data["quick_capture_category"] = category
        await update.message.reply_text(f"Record your {category} in one sentence.")
        return True

    return False


async def capture_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    if not update.message or not update.message.text:
        return

    text = update.message.text
    if await handle_button_or_flow(update, context, text):
        return

    category = parse_capture(text)["category"]
    if category == "capture":
        record_telegram_capture(text, category="capture", metadata={"entrypoint": "text"})
        append_quick_capture_to_today(text)
        await reply_with_main_menu(update, QUICK_CAPTURE_FALLBACK_MESSAGE)
        return

    record_telegram_capture(text, category=str(category), metadata={"entrypoint": "prefix_text"})
    path = today_file()
    block = build_capture_block(text)
    insert_capture(path, block)
    await reply_with_main_menu(update, SAVE_CONFIRMATION)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    reply_markup = FLOW_KEYBOARD if context.user_data.get("flow") or context.user_data.get("quick_capture_category") else MAIN_MENU_KEYBOARD
    await update.message.reply_text(
        VOICE_NOTE_MESSAGE,
        reply_markup=reply_markup,
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if await reject_if_not_allowed(update):
        return

    if not update.message or not update.message.photo:
        return

    now = datetime.now()
    message_id = update.message.message_id
    media_path, markdown_link = build_photo_paths(now, message_id)
    caption = update.message.caption or ""

    try:
        media_path.parent.mkdir(parents=True, exist_ok=True)
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive(custom_path=str(media_path))
        append_photo_entry_to_today(markdown_link, caption, now)
    except Exception:
        await update.message.reply_text("图片保存失败，请稍后再试。")
        return

    if context.user_data.get("flow") or context.user_data.get("quick_capture_category"):
        await update.message.reply_text(
            "图片已保存。当前流程仍在继续；如果要切换功能，请直接按菜单按钮或发送 /cancel。",
            reply_markup=FLOW_KEYBOARD,
        )
        return

    await reply_with_main_menu(update, "图片已保存。")


def main() -> None:
    load_dotenv(APP_DIR / ".env")

    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN is missing. Create .env from .env.example and add your BotFather token.")

    read_allowed_user_id()

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("whoami", whoami))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("commands", commands))
    application.add_handler(CommandHandler("today", today))
    application.add_handler(CommandHandler("export", export))
    application.add_handler(CommandHandler("review", review))
    application.add_handler(CommandHandler("beforeai", beforeai))
    application.add_handler(CommandHandler("decision", decision))
    application.add_handler(CommandHandler("mistake", mistake))
    application.add_handler(CommandHandler("principle", principle))
    application.add_handler(CommandHandler("weekly", weekly))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, capture_text))

    application.run_polling()


if __name__ == "__main__":
    main()
