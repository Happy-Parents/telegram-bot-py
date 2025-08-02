from telegram import Message
from telegram.ext import ContextTypes
from state import user_states, message_to_user_map
from keyboards import build_keyboard
from messages import *

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
