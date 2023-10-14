from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tg_bot.config import Config

title_start_recording = "Записатися на консультацію"
title_contacts = "Контакти"
title_common_questions = "Часті питання"
title_records = "Мої записи"


def start_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text=title_start_recording)
            ],
            [
                KeyboardButton(text=title_contacts),
                KeyboardButton(text=title_common_questions),
                KeyboardButton(text=title_records)
            ]
        ]
    )

    if user_id in Config.ADMINS:
        button = KeyboardButton("Адмін панель")
        markup.row(button)

    return markup
