from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.inline.callback_data import temp_callback as tc


def remove_inline(name: str, title: str):
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [InlineKeyboardButton(text=title, callback_data=tc.new(title="remove", name=name))]])
