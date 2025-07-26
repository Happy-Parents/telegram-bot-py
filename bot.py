from telegram import Update, ReplyKeyboardMarkup, Message
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8108504859:AAFwonWfT6VVV2LlOHf4rtE010x9lmpNlGY"
ADMIN_GROUP_ID = -1002710807138  # ID групи, куди надсилаються повідомлення

user_states = {}
message_to_user_map = {}

WELCOME_MESSAGE = "👋 Вітаємо у боті *Happy Parents*!\nОбери опцію нижче:"
ASK_MESSAGE = "✍️ Напишіть ваше питання. Ми якнайшвидше відповімо."
CONFIRM_MESSAGE = "✅ Дякуємо! Ваше питання надіслано адміністратору."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["❓ Питання адміністратору"]]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message: Message = update.message
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = message.text

    # 👨‍💻 Якщо це повідомлення в групі та reply
    if chat_id == ADMIN_GROUP_ID and message.reply_to_message:
        original_message_id = message.reply_to_message.message_id
        recipient_id = message_to_user_map.get(original_message_id)

        if recipient_id:
            await context.bot.send_message(
                chat_id=recipient_id,
                text=f"💬 Відповідь від адміністратора:\n\n{text}"
            )
            await message.reply_text("📤 Відповідь надіслано користувачу.")
        else:
            await message.reply_text("⚠️ Не вдалося знайти користувача для відповіді.")
        return

    # 🤖 Користувач обирає "Питання адміністратору"
    if text == "❓ Питання адміністратору":
        user_states[user_id] = "awaiting_question"
        await message.reply_text(ASK_MESSAGE)
        return

    # 🧾 Користувач у стані "очікує питання"
    if user_states.get(user_id) == "awaiting_question":
        user_states.pop(user_id)
        username = update.effective_user.username or f"id:{user_id}"
        forwarded_message = await context.bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=f"📩 Нове питання від @{username} ({user_id}):\n\n{text}"
        )

        # Зберегти зв'язок між повідомленням у групі та користувачем
        message_to_user_map[forwarded_message.message_id] = user_id

        await message.reply_text(CONFIRM_MESSAGE)
        return

    await message.reply_text("🔄 Оберіть дію з меню або натисніть /start.")

# Запуск бота
def main():
    print("🤖 Бот запускається...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
