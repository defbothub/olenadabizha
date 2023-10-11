from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.config import Config

contacts_keyboard = InlineKeyboardMarkup(row_width=2,
                                         inline_keyboard=[
                                             [
                                                 InlineKeyboardButton(text="Геолокація офісу",
                                                                      callback_data="contacts_office_location"),
                                                 InlineKeyboardButton(text="Телефон",
                                                                      callback_data="contacts_phone_number")
                                             ],
                                             [
                                                 InlineKeyboardButton(text="Фейсбук",
                                                                      url=Config.CONTACTS_FACEBOOK_URL,
                                                                      callback_data="contacts_facebook"),
                                                 InlineKeyboardButton(text="Інстаграм",
                                                                      url=Config.CONTACTS_INSTAGRAM_URL,
                                                                      callback_data="contacts_instagram")
                                             ]
                                         ])
