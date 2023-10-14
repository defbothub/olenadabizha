import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, Text, Command
from aiogram.utils.markdown import hcode

from tg_bot.config import Config
from tg_bot.keyboards.default.start_keyb import title_contacts
from tg_bot.keyboards.inline.contacts_keyb import contacts_keyboard

logger = logging.getLogger(__name__)


async def show_contacts(message: types.Message):
    logger.info(f"Handler called. {show_contacts.__name__}. user_id={message.from_user.id}")

    await message.answer(text="<b>Відвідайте сторінки в соцмережах ⬇️</b>", reply_markup=contacts_keyboard)


async def show_phone_number(callback: types.CallbackQuery):
    logger.info(f"Handler called. {show_phone_number.__name__}. user_id={callback.from_user.id}")
    await callback.answer()

    await callback.message.answer_contact(phone_number=Config.CONTACTS_PHONE_NUMBER,
                                          first_name=Config.CONTACTS_FIRST_NAME)


async def show_office_location(callback: types.CallbackQuery):
    logger.info(f"Handler called. {show_office_location.__name__}. user_id={callback.from_user.id}")
    await callback.answer()

    text = [
        "<b>Адреса офісу:</b>\n",
        hcode("м. Одеса, просп. Гагаріна 12 А, БЦ Шевченківський 11 пов., оф. 1105")
    ]

    message = callback.message
    await message.answer(text='\n'.join(text))
    await message.answer_location(latitude=Config.CONTACTS_OFFICE_LATITUDE, longitude=Config.CONTACTS_OFFICE_LONGITUDE)


def register_contacts(dp: Dispatcher):
    dp.register_message_handler(show_contacts, ChatTypeFilter(types.ChatType.PRIVATE),
                                Text(title_contacts) | Command('contacts'))
    dp.register_callback_query_handler(show_phone_number, text="contacts_phone_number")
    dp.register_callback_query_handler(show_office_location, text="contacts_office_location")
