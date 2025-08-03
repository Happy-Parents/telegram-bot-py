from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import WEBHOOK_URL, BOT_TOKEN, ENV
from handlers.user import start, handle_message
from log_config import console_logger

def main() -> None:
    console_logger.info("🤖 Happy Bot has been launched...")

    if not WEBHOOK_URL and ENV == 'production':
        console_logger.critical('WEBHOOK not found')
        raise ValueError('WEBHOOK not found')

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    if ENV == 'production':
        app.run_webhook(
            listen="0.0.0.0",
            port=8080,
            webhook_url=WEBHOOK_URL,
        )
    else:
        app.run_polling()


if __name__ == "__main__":
    main()
