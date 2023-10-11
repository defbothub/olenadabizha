from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tg_bot.config import Config


def start_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="Записатися")
            ],
            [
                KeyboardButton(text="Контакти"),
                KeyboardButton(text="Поширені питання"),
                KeyboardButton(text="Мої записи")
            ]
        ]
    )

    if user_id in Config.ADMINS:
        button = KeyboardButton("Адмін панель")
        markup.row(button)

    return markup
