from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

from tg_bot.config import Config

payment_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [
            KeyboardButton(text="Перейти до сплати",
                           web_app=WebAppInfo(url=Config.PAYMENT_URL))
        ]
    ]
)
