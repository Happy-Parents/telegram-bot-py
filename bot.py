from telegram import Update, ReplyKeyboardMarkup, Message
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8108504859:AAFwonWfT6VVV2LlOHf4rtE010x9lmpNlGY"
ADMIN_GROUP_ID = -4940266122

user_states = {}  # user_id → "active_chat", "awaiting_feedback"
message_to_user_map = {}  # group_msg_id → user_id

# 📌 Константи повідомлень
WELCOME_MESSAGE = "👋 Вітаємо у боті *Happy Parents*!\nОбери опцію нижче:"
ASK_MESSAGE = "✍️ Напишіть ваше питання. Ми якнайшвидше відповімо."
CONFIRM_MESSAGE = "✅ Ваше повідомлення надіслано адміністратору."
THANKS_FEEDBACK_MESSAGE = "✅ Дякуємо за оцінку!"
CLOSE_CONVERSATION_MESSAGE = "✅ Дякуємо! Розмову завершено."
CHOOSE_ACTION_MESSAGE = "🔄 Оберіть дію з меню або натисніть /start."
FEEDBACK_REQUEST_MESSAGE = "🙏 Дякуємо за спілкування!\nОцініть, будь ласка, розмову:"
FEEDBACK_SENT_MESSAGE = "✅ Запит на оцінку надіслано користувачу."
USER_NOT_FOUND_FEEDBACK_MESSAGE = "⚠️ Користувача не знайдено для оцінки."
ANSWER_SENT_MESSAGE = "📤 Відповідь надіслано користувачу."
USER_NOT_FOUND_ANSWER_MESSAGE = "⚠️ Не вдалося знайти користувача для відповіді."

QUESTION_BUTTON_TEXT = "❓ Задати питання"
FEEDBACK_QUESTION = "стоп"
FEEDBACK_OPTIONS = ["😐", "🙂", "😃"]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[QUESTION_BUTTON_TEXT]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=markup, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message: Message = update.message
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = message.text.strip()

    if chat_id == ADMIN_GROUP_ID and message.reply_to_message:
        original_message_id = message.reply_to_message.message_id
        recipient_id = message_to_user_map.get(original_message_id)

        if text == FEEDBACK_QUESTION:
            if recipient_id:
                keyboard = [[emoji] for emoji in FEEDBACK_OPTIONS]
                markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

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
        return

    if user_states.get(user_id) == "awaiting_feedback":
        if text in FEEDBACK_OPTIONS:
            await context.bot.send_message(
                chat_id=ADMIN_GROUP_ID,
                text=f"📊 Користувач id:{user_id} оцінив розмову як {text}"
            )
            await message.reply_text(THANKS_FEEDBACK_MESSAGE)
        else:
            await message.reply_text(CLOSE_CONVERSATION_MESSAGE)

        user_states.pop(user_id, None)
        return

    if text == QUESTION_BUTTON_TEXT:
        user_states[user_id] = "active_chat"
        await message.reply_text(ASK_MESSAGE)
        return

    if user_states.get(user_id) == "active_chat":
        username = update.effective_user.username or f"id:{user_id}"
        sent = await context.bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=f"📩 Повідомлення від @{username} ({user_id}):\n\n{text}"
        )
        message_to_user_map[sent.message_id] = user_id
        await message.reply_text(CONFIRM_MESSAGE)
        return

    await message.reply_text(CHOOSE_ACTION_MESSAGE)


def main():
    print("🤖 Happy Bot has been launched...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()
