from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from config import WEBHOOK_URL, BOT_TOKEN
from handlers.user import handle_message
from messages import WELCOME_MESSAGE, QUESTION_BUTTON_TEXT
from keyboards import build_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    markup = build_keyboard([QUESTION_BUTTON_TEXT])
    await update.message.reply_text(WELCOME_MESSAGE, reply_markup=markup, parse_mode='Markdown')


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
