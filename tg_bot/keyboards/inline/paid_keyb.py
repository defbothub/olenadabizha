from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.inline.callback_data import temp_callback as tc

paid_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Я оплати(в/ла)",
                                 callback_data=tc.new(title="service_paid", name="confirm"))
        ],
        [
            InlineKeyboardButton(text="Назад",
                                 callback_data=tc.new(title="service_paid", name="back"))
        ]
    ]
)
