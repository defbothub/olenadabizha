from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.inline.callback_data import temp_callback as tc
from tg_bot.misc.data_handling import questions


def questions_keyboard() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    for category in questions:
        button = InlineKeyboardButton(text=category, callback_data=tc.new(title="question", name=category))
        markup.row(button)

    return markup


back_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data=tc.new(title="question", name="back"))
        ]
    ]
)
