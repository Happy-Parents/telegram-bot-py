from telegram import Update, Message
    # Update.effective_user has has all info about user
    # Update.effective_chat has all info about user chat
from telegram.ext import ContextTypes
from state import user_states, message_to_user_map
from .admin import handle_admin_reply
from log_config import file_logger
from keyboards import BOT_FEATURES_KEYBOARD
from config import ADMIN_GROUP_ID
from messages import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_MESSAGE,
                                    reply_markup=BOT_FEATURES_KEYBOARD,
                                    parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None or message.text is None:
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    text = message.text.strip()

    # Admin reply
    if chat_id == ADMIN_GROUP_ID and message.reply_to_message:
        await handle_admin_reply(message, context, text)
        return

    # User reply (rate support)
    if user_states.get(user_id) == "awaiting_feedback":
        await handle_user_feedback(message, context, user_id, text)
        return

    # Conversation beginning
    if text == QUESTION_BUTTON_TEXT:
        # TODO: handle update.effective_user.is_bot == True
        file_logger.info(f'User with id {user_id} started chat with admin.')
        user_states[user_id] = "active_chat"
        await message.reply_text(ASK_MESSAGE)
        return

    # Messages in active chat
    if user_states.get(user_id) == "active_chat":
        await handle_user_question(update, context, text)
        return

    # Case when user command is not recognized
    await message.reply_text(CHOOSE_ACTION_MESSAGE)


async def handle_user_feedback(message: Message, context: ContextTypes.DEFAULT_TYPE, user_id: int, text: str) -> None:
    """handle user feedback abot conversation level"""

    if text in FEEDBACK_OPTS:
        await context.bot.send_message(
            chat_id=ADMIN_GROUP_ID,
            text=f"📊 Користувач id:{user_id} оцінив розмову як {text}"
        )
        file_logger.info(f'User with id {user_id} rated support in valid way: {text}')
        await message.reply_text(THANKS_FEEDBACK_MESSAGE)
    else:
        file_logger.warning(f'User with id {user_id} rated support in invalid way: {text}')
        await message.reply_text(CLOSE_CONVERSATION_MESSAGE)
        file_logger.info('Finit message to user delivered.')

    user_states.pop(user_id, None)


async def handle_user_question(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    """handle user message in active chat"""

    user = update.effective_user
    display_id = f"id:{user.id}"
    display_name = f'{user.first_name or user.username or display_id} [{user.language_code}]'

    sent = await context.bot.send_message(
        chat_id=ADMIN_GROUP_ID,
        text=f"📩 Повідомлення від {display_name} ({user.id}):\n\n{text}"
    )
    message_to_user_map[sent.message_id] = user.id
    await update.message.reply_text(CONFIRM_MESSAGE)
