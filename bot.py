import os
from decouple import config
from telegram import Update, ReplyKeyboardMarkup, Message
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = config("BOT_TOKEN")
ADMIN_GROUP_ID = int(config("ADMIN_GROUP_ID"))
WEBHOOK_URL = config("WEBHOOK_URL")

from messages import (WELCOME_MESSAGE, ASK_MESSAGE, CONFIRM_MESSAGE, THANKS_FEEDBACK_MESSAGE,
                      CLOSE_CONVERSATION_MESSAGE, CHOOSE_ACTION_MESSAGE, FEEDBACK_REQUEST_MESSAGE,
                      FEEDBACK_SENT_MESSAGE, USER_NOT_FOUND_FEEDBACK_MESSAGE, ANSWER_SENT_MESSAGE,
                      USER_NOT_FOUND_ANSWER_MESSAGE, QUESTION_BUTTON_TEXT, FEEDBACK_QUESTION, FEEDBACK_OPTIONS)

user_states: dict[int, str] = {}
message_to_user_map: dict[int, int] = {}



def build_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    """Створення клавіатури з кнопками"""
    return ReplyKeyboardMarkup([[btn] for btn in buttons], one_time_keyboard=True, resize_keyboard=True)


async def handle_admin_reply(message: Message, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """Обробка відповіді адміністратора в групі"""
    original_msg_id = message.reply_to_message.message_id
    recipient_id = message_to_user_map.get(original_msg_id)

    if text == FEEDBACK_QUESTION:
        if recipient_id:
            markup = build_keyboard(FEEDBACK_OPTIONS)
            await context.bot.send_message(
                chat_id=recipient_id,
                text=FEEDBACK_REQUEST_MESSAGE,
                reply_markup=markup
            )
            user_states[recipient_id] = "awaiting_feedback"
            await message.reply_text(FEEDBACK_SENT_MESSAGE)
        else:
            await message.reply_text(USER_NOT_FOUND_FEEDBACK_MESSAGE)
        return

    if recipient_id:
        await context.bot.send_message(
            chat_id=recipient_id,
            text=f"💬 Відповідь адміністратора:\n\n{text}"
        )
        await message.reply_text(ANSWER_SENT_MESSAGE)
    else:
        await message.reply_text(USER_NOT_FOUND_ANSWER_MESSAGE)


async def handle_user_feedback(message: Message, context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str) -> None:
    """Обробка оцінки від користувача"""
    if text in FEEDBACK_OPTIONS:
        await context.bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=f"📊 Користувач id:{user_id} оцінив розмову як {text}"
        )
        await message.reply_text(THANKS_FEEDBACK_MESSAGE)
    else:
        await message.reply_text(CLOSE_CONVERSATION_MESSAGE)

    user_states.pop(user_id, None)


async def handle_user_question(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """Обробка повідомлення користувача в активному діалозі"""
    user_id = update.effective_user.id
    username = update.effective_user.username or f"id:{user_id}"
    sent = await context.bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"📩 Повідомлення від @{username} ({user_id}):\n\n{text}"
    )
    message_to_user_map[sent.message_id] = user_id
    await update.message.reply_text(CONFIRM_MESSAGE)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    markup = build_keyboard([QUESTION_BUTTON_TEXT])
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=markup, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None or message.text is None:
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = message.text.strip()

    # Відповідь адміністратора
    if chat_id == ADMIN_GROUP_ID and message.reply_to_message:
        await handle_admin_reply(message, context, text)
        return

    # Відповідь користувача (оцінка)
    if user_states.get(user_id) == "awaiting_feedback":
        await handle_user_feedback(message, context, user_id, text)
        return

    # Початок діалогу
    if text == QUESTION_BUTTON_TEXT:
        user_states[user_id] = "active_chat"
        await message.reply_text(ASK_MESSAGE)
        return

    # Повідомлення в активному чаті
    if user_states.get(user_id) == "active_chat":
        await handle_user_question(update, context, text)
        return

    # Випадок, коли команда не розпізнана
    await message.reply_text(CHOOSE_ACTION_MESSAGE)


def main() -> None:
    print("🤖 Happy Bot has been launched...")

    if not WEBHOOK_URL:
        raise ValueError('WEBHOOK not found')

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url=WEBHOOK_URL,
    )


if __name__ == "__main__":
    main()
