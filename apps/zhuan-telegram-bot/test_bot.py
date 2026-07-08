import unittest
from unittest.mock import patch
from datetime import datetime

import bot


SAMPLE_INBOX = """# Telegram Inbox - 2026-07-07

## Captures

### 09:10 - study
Original:
study: Fluid Mechanics pipe loss 1 hour

Interpreted:
- Category: study
- Tags: #study
- Worth review: no

### 11:20 - mistake
Original:
mistake: spent too much time optimizing system

Interpreted:
- Category: mistake
- Tags: #mistake
- Worth review: yes

### 13:00 - principle
Original:
principle: capture first, organize later

Interpreted:
- Category: principle
- Tags: #principle
- Worth review: yes

## Review Queue

## Principles
"""


class DummyContext:
    def __init__(self):
        self.user_data = {}


class FakeMessage:
    def __init__(self):
        self.replies = []

    async def reply_text(self, text, reply_markup=None):
        self.replies.append((text, reply_markup))


class FakeUpdate:
    def __init__(self):
        self.message = FakeMessage()
        self.effective_message = self.message
        self.effective_user = None


class BotFormattingTests(unittest.TestCase):
    def test_today_summary_counts_captures_by_category(self):
        summary = bot.build_today_summary(SAMPLE_INBOX)

        self.assertIn("Total captures: 3", summary)
        self.assertIn("- study: 1", summary)
        self.assertIn("- mistake: 1", summary)
        self.assertIn("- principle: 1", summary)

    def test_clean_export_contains_judgment_training_sections(self):
        export = bot.build_clean_export(SAMPLE_INBOX, "2026-07-07")

        self.assertIn("# Daily Capture - 2026-07-07", export)
        for heading in [
            "## Daily Capture",
            "## Before AI",
            "## Judgment",
            "## Review",
            "## Mistake",
            "## Principle",
            "## Next Action",
        ]:
            self.assertIn(heading, export)
        self.assertIn("- 09:10 [study] study: Fluid Mechanics pipe loss 1 hour", export)
        self.assertIn("- 11:20 [mistake] mistake: spent too much time optimizing system", export)
        self.assertIn("- 13:00 [principle] principle: capture first, organize later", export)

    def test_review_template_is_short_and_practical(self):
        self.assertIn("## Daily Judgment Review", bot.REVIEW_TEMPLATE)
        self.assertIn("3. 哪个假设错了？", bot.REVIEW_TEMPLATE)
        self.assertIn("8. 提炼一句下次规则。", bot.REVIEW_TEMPLATE)

    def test_judgment_templates_exist(self):
        self.assertIn("## Before AI", bot.BEFORE_AI_TEMPLATE)
        self.assertIn("你希望 AI 挑战你哪里？", bot.BEFORE_AI_TEMPLATE)
        self.assertIn("## Decision Log", bot.DECISION_TEMPLATE)
        self.assertIn("What would change my mind:", bot.DECISION_TEMPLATE)
        self.assertIn("## Weekly Judgment Scorecard", bot.WEEKLY_TEMPLATE)
        self.assertIn("Where did AI make me passive?", bot.WEEKLY_TEMPLATE)

    def test_command_examples_include_core_prefixes(self):
        for prefix in [
            "study:",
            "spend:",
            "exercise:",
            "assignment:",
            "conversation:",
            "mistake:",
            "principle:",
            "review:",
        ]:
            self.assertIn(prefix, bot.COMMAND_EXAMPLES)
        for command in [
            "/beforeai",
            "/decision",
            "/mistake text",
            "/principle text",
            "/weekly",
        ]:
            self.assertIn(command, bot.COMMAND_EXAMPLES)

    def test_mistake_entry_uses_judgment_training_format(self):
        entry = bot.build_mistake_entry("accepted AI output without verification")

        self.assertIn("- Mistake: accepted AI output without verification", entry)
        self.assertIn("- Cause:", entry)
        self.assertIn("- Prevention:", entry)
        self.assertIn("- Principle:", entry)

    def test_principle_entry_uses_judgment_training_format(self):
        entry = bot.build_principle_entry("verify before trusting")

        self.assertIn("- Principle: verify before trusting", entry)
        self.assertIn("- When to use:", entry)
        self.assertIn("- Warning:", entry)
        self.assertIn("- Example:", entry)

    def test_append_section_entry_creates_missing_mistakes_section(self):
        content = bot.append_section_entry(SAMPLE_INBOX, "## Mistakes", "mistake entry\n")

        self.assertIn("## Mistakes\n\nmistake entry\n", content)
        self.assertLess(content.index("## Mistakes"), content.index("## Principles"))

    def test_main_menu_contains_button_first_actions(self):
        self.assertEqual(
            bot.MAIN_MENU_BUTTONS,
            [
                [bot.BUTTON_BEFORE_AI, bot.BUTTON_QUICK_CAPTURE],
                [bot.BUTTON_STUDY_LOG, bot.BUTTON_ASSIGNMENT_PROJECT],
                [bot.BUTTON_DECISION, bot.BUTTON_CONVERSATION_LOG],
                [bot.BUTTON_MISTAKE, bot.BUTTON_PRINCIPLE],
                [bot.BUTTON_NIGHT_REVIEW, bot.BUTTON_TODAY],
                [bot.BUTTON_EXPORT, bot.BUTTON_HELP],
            ],
        )

    def test_quick_capture_menu_contains_categories_and_back(self):
        flattened = [button for row in bot.QUICK_CAPTURE_BUTTONS for button in row]

        for button in ["Study", "Spend", "Exercise", "Assignment", "Conversation", "Video", "Book", "Cook", "Idea", bot.BUTTON_BACK]:
            self.assertIn(button, flattened)

    def test_build_guided_entry_formats_answers_under_heading(self):
        entry = bot.build_guided_entry(
            "## Before AI",
            ["Problem:", "My initial judgment:"],
            ["Need a plan", "Start small"],
        )

        self.assertIn("## Before AI", entry)
        self.assertIn("- Problem: Need a plan", entry)
        self.assertIn("- My initial judgment: Start small", entry)

    def test_build_mistake_entry_from_answers(self):
        entry = bot.build_mistake_entry_from_answers(
            ["trusted output too fast", "wanted speed", "verify before using"]
        )

        self.assertIn("- Mistake: trusted output too fast", entry)
        self.assertIn("- Cause: wanted speed", entry)
        self.assertIn("- Prevention: verify before using", entry)
        self.assertIn("- Principle:", entry)

    def test_build_principle_entry_from_answers(self):
        entry = bot.build_principle_entry_from_answers(
            ["verify before trusting", "AI answers", "do not outsource judgment"]
        )

        self.assertIn("- Principle: verify before trusting", entry)
        self.assertIn("- When to use: AI answers", entry)
        self.assertIn("- Warning: do not outsource judgment", entry)
        self.assertIn("- Example:", entry)

    def test_chinese_guided_questions(self):
        self.assertEqual(bot.FLOW_DEFINITIONS["before_ai"]["questions"][0], "你现在要问 AI / 解决什么问题？")
        self.assertEqual(bot.FLOW_DEFINITIONS["quick_capture"]["questions"], ["发生了什么？随便写一句。"])
        self.assertEqual(bot.FLOW_DEFINITIONS["study_log"]["questions"][0], "今天学了什么？")
        self.assertEqual(bot.FLOW_DEFINITIONS["assignment_project"]["questions"][0], "今天推进了什么 assignment / project？")
        self.assertEqual(bot.FLOW_DEFINITIONS["conversation_log"]["questions"][0], "今天和谁有重要沟通？")
        self.assertEqual(bot.FLOW_DEFINITIONS["review"]["questions"][-1], "提炼一句下次规则。")

    def test_chinese_help_and_confirmation_text(self):
        self.assertIn("问 AI 前先写自己的判断", bot.HELP_TEXT)
        self.assertIn("已保存。这个记录会帮助你训练判断力。", bot.SAVE_CONFIRMATION)
        self.assertIn("已保存为 Quick Capture。你也可以直接按按钮进入更具体的记录。", bot.QUICK_CAPTURE_FALLBACK_MESSAGE)

    def test_main_menu_button_switches_active_flow_without_saving_button_as_answer(self):
        context = DummyContext()
        bot.start_guided_flow(context, "before_ai")
        context.user_data["flow"]["answers"] = ["old incomplete answer"]

        question = bot.start_main_menu_button_flow(context, bot.BUTTON_QUICK_CAPTURE)

        self.assertEqual(question, bot.FLOW_DEFINITIONS["quick_capture"]["questions"][0])
        self.assertEqual(context.user_data["flow"]["name"], "quick_capture")
        self.assertEqual(context.user_data["flow"]["answers"], [])
        self.assertNotIn(bot.BUTTON_QUICK_CAPTURE, context.user_data["flow"]["answers"])

    def test_cancel_text_detection_supports_english_and_chinese(self):
        for text in ["/cancel", "cancel", "Back", "back", "取消", "返回", bot.BUTTON_BACK]:
            self.assertTrue(bot.is_cancel_text(text))

    def test_back_action_clears_active_flow(self):
        context = DummyContext()
        bot.start_guided_flow(context, "before_ai")

        message = bot.cancel_active_flow(context)

        self.assertEqual(message, "已返回主菜单。")
        self.assertNotIn("flow", context.user_data)

    def test_flow_keyboard_contains_back_quick_capture_and_today(self):
        flattened = [button for row in bot.FLOW_BUTTONS for button in row]

        self.assertEqual(bot.FLOW_BUTTONS[0], [bot.BUTTON_BACK])
        self.assertIn(bot.BUTTON_QUICK_CAPTURE, flattened)
        self.assertIn(bot.BUTTON_TODAY, flattened)

    def test_quick_capture_item_uses_required_section(self):
        entry = bot.build_quick_capture_entry("voice typed text", datetime(2026, 7, 7, 9, 8, 7))

        self.assertIn("## Quick Capture / 随手记录", entry)
        self.assertIn("### 09:08", entry)
        self.assertIn("- Text: voice typed text", entry)


class BotAsyncBehaviorTests(unittest.IsolatedAsyncioTestCase):
    async def test_voice_handler_replies_without_clearing_active_flow(self):
        context = DummyContext()
        bot.start_guided_flow(context, "before_ai")
        update = FakeUpdate()

        await bot.handle_voice(update, context)

        self.assertEqual(update.message.replies[0][0], bot.VOICE_NOTE_MESSAGE)
        self.assertEqual(update.message.replies[0][1], bot.FLOW_KEYBOARD)
        self.assertEqual(context.user_data["flow"]["name"], "before_ai")


    async def test_capture_text_records_event_for_categorized_input(self):
        context = DummyContext()
        update = FakeUpdate()
        update.message.text = "study: fake study note"

        with patch.object(bot, "record_telegram_capture") as record_capture, patch.object(bot, "insert_capture"):
            await bot.capture_text(update, context)

        record_capture.assert_called_once()
        self.assertEqual(record_capture.call_args.kwargs["category"], "study")
        self.assertEqual(record_capture.call_args.args[0], "study: fake study note")
    def test_photo_paths_use_expected_daily_media_folder_and_relative_link(self):
        now = datetime(2026, 7, 7, 9, 8, 7)

        media_path, markdown_link = bot.build_photo_paths(now, 12345)

        self.assertEqual(media_path, bot.MEDIA_DIR / "2026-07-07" / "090807_photo_12345.jpg")
        self.assertEqual(markdown_link, "../telegram_media/2026-07-07/090807_photo_12345.jpg")

    def test_photo_entry_uses_required_markdown_format(self):
        entry = bot.build_photo_entry(
            datetime(2026, 7, 7, 9, 8, 7),
            "../telegram_media/2026-07-07/090807_photo_12345.jpg",
            "pump diagram",
        )

        self.assertIn("## Photo Capture / 图片记录", entry)
        self.assertIn("### 09:08", entry)
        self.assertIn("- File: ../telegram_media/2026-07-07/090807_photo_12345.jpg", entry)
        self.assertIn("- Caption: pump diagram", entry)
        self.assertIn("- Note: Photo saved from Telegram.", entry)


if __name__ == "__main__":
    unittest.main()
