import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, CommandStart

from tg_bot.keyboards.default.start_keyb import start_keyboard

logger = logging.getLogger(__name__)


async def cmd_start(message: types.Message):
    logger.info(f"Handler called. {cmd_start.__name__}. user_id={message.from_user.id}")

    text = "\n<b>В меню ви можете ознайомитися з відповідями на часті питання та записатися на консультацію користуючись клавіатурою   ⬇️</b>"
    await message.answer(text=text, reply_markup=start_keyboard(message.from_user.id))


def register_start(dp: Dispatcher):
    dp.register_message_handler(cmd_start, ChatTypeFilter(types.ChatType.PRIVATE), CommandStart())
