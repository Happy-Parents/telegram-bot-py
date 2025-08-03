from telegram import ReplyKeyboardMarkup
from messages import FEEDBACK_OPTS, QUESTION_BUTTON_TEXT


def build_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    """Keyboard with buttons"""
    return ReplyKeyboardMarkup(
        [[btn] for btn in buttons],
        one_time_keyboard=True,
        resize_keyboard=True)

FEEDBACK_OPTS_KEYBOARD = build_keyboard(FEEDBACK_OPTS)

BOT_FEATURES_KEYBOARD = build_keyboard([QUESTION_BUTTON_TEXT])
