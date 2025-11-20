from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN
from handlers.user import start, handle_message
from log_config import file_logger, clean_log_file, console_logger
from error_handler import error_handler

def main() -> None:
    clean_log_file()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    console_logger.info("🤖 Happy Bot has been launched...")
    file_logger.info("🤖 Happy Bot has been launched...")
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
