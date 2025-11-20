# error_handler.py
import traceback
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_GROUP_ID
from log_config import file_logger

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Глобальний перехоплювач помилок.
    Автоматично ловить усі exceptions у всіх handlers.
    """
    traceback_info = "".join(traceback.format_exception(context.error))

    file_logger.error("❗ GLOBAL ERROR ❗")
    file_logger.error(traceback_info)

    try:
        await context.bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=f"⚠️ *Помилка у боті!*\n\n```{traceback_info}```",
            parse_mode="Markdown"
        )
    except Exception as send_error:
        file_logger.error(
            f"Не вдалося відправити помилку адміну: {send_error}"
        )
