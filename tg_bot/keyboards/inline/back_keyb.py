from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

back_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back_state")
        ]
    ]
)
