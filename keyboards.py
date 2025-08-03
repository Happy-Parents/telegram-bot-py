from telegram import ReplyKeyboardMarkup
from messages import FEEDBACK_OPTS


def build_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    """Keyboard with buttons"""
    return ReplyKeyboardMarkup(
        [[btn] for btn in buttons],
        one_time_keyboard=True,
        resize_keyboard=True)

FEEDBACK_OPTS_KEYBOARD = build_keyboard(FEEDBACK_OPTS)
