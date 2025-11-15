from telegram import Message
from telegram.ext import ContextTypes
from state import user_states, message_to_user_map
from keyboards import FEEDBACK_OPTS_KEYBOARD
from log_config import console_logger
from messages import *

async def handle_admin_reply(message: Message, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    original_msg_id = message.reply_to_message.message_id
    recipient_id = message_to_user_map.get(original_msg_id)

    # Replying to user question
    if recipient_id:
        match text.lower():
            case txt if txt == FEEDBACK_QUESTION.lower():
                console_logger.info('Admin asked to rate support.')
                await context.bot.send_message(
                    chat_id=recipient_id,
                    text=FEEDBACK_REQUEST_MESSAGE,
                    reply_markup=FEEDBACK_OPTS_KEYBOARD
                )
                console_logger.info(f'User with id {recipient_id} was asked to rate support.')
                user_states[recipient_id] = "awaiting_feedback"
                await message.reply_text(FEEDBACK_SENT_MESSAGE)
            case _:
                await context.bot.send_message(
                    chat_id=recipient_id,
                    text=f"{ADMIN_REPLY_LABEL}\n\n{text}"
                )
                console_logger.info(f'Admin unswer to user id {recipient_id} was sent.')
                await message.reply_text(ANSWER_SENT_MESSAGE)
    else:
        console_logger.error('Unable to unswer. User not found.')
        await message.reply_text(USER_NOT_FOUND_ANSWER_MESSAGE)
