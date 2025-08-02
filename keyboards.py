from telegram import ReplyKeyboardMarkup


def build_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    """Keyboard with buttons"""
    return ReplyKeyboardMarkup(
        [[btn] for btn in buttons],
        one_time_keyboard=True,
        resize_keyboard=True)
