from datetime import datetime
from typing import Union

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import MessageToDeleteNotFound

from tg_bot.config import Config
from tg_bot.handlers.admin.panel import cmd_panel
from tg_bot.handlers.common_questions import show_questions
from tg_bot.handlers.form_filling import start_filling
from tg_bot.handlers.start import cmd_start
from tg_bot.handlers.records import show_records
from tg_bot.keyboards.inline.callback_data import temp_callback as tc
from tg_bot.keyboards.inline.remove_keyb import remove_inline
from tg_bot.misc.data_handling import all_records, black_list
from tg_bot.misc.utils import form_completion, add_msg_to_delete
from tg_bot.misc.states import FindData

temp_calldata, temp_msgid_state = {}, {}

markup = InlineKeyboardMarkup(row_width=1,
                              inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]])


async def write_user_id(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()

    uid = callback.from_user.id

    msg = await callback.message.edit_text("<b>Введіть ID користувача</b>", reply_markup=markup)
    temp_calldata[callback.from_user.id] = callback_data
    temp_msgid_state[uid] = msg.message_id
    add_msg_to_delete(user_id=uid, msg_id=msg.message_id)

    await FindData.UserId.set()


async def show_userdata(message: Union[types.Message, types.CallbackQuery], state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        await message.answer()

        await state.reset_state()
        return await cmd_panel(message.message)

    msg_text = message.text
    uid = message.from_user.id

    try:
        await message.chat.delete_message(temp_msgid_state[uid])
    except MessageToDeleteNotFound:
        pass

    if msg_text.startswith('/'):
        if msg_text == "/start":
            await state.reset_state()
            return await cmd_start(message)
        elif msg_text == "/records":
            await state.reset_state()
            return await show_records(message)
        elif msg_text == "/apanel":
            if uid in Config.ADMINS:
                await state.reset_state()
                return await cmd_panel(message)
        elif msg_text == "/filling":
            await state.reset_state()
            return await start_filling(message)
        elif msg_text == "common_questions":
            await state.reset_state()
            return await show_questions(message)

    await message.delete()

    if ("weekend" not in msg_text) and (not msg_text.isdigit()):
        msg_wrong_format = await message.answer("<b>ID може містити тільки цифри</b>", reply_markup=markup)
        temp_msgid_state[uid] = msg_wrong_format.message_id
        add_msg_to_delete(user_id=uid, msg_id=msg_wrong_format.message_id)
        return

    name = temp_calldata[uid].get("name")
    if name == "record":
        if msg_text not in all_records:
            msg_wrong_id = await message.answer(
                "<b>Користувача з таким ID не існує або у нього немає активних записів</b>", reply_markup=markup)
            temp_msgid_state[uid] = msg_wrong_id.message_id
            add_msg_to_delete(user_id=uid, msg_id=msg_wrong_id.message_id)
            return

        for i in all_records[str(msg_text)]:
            current_record = all_records[str(msg_text)][i]
            temp_record = {
                "service": current_record.get("service"),
                "date": current_record.get("date"),
                "time": current_record.get("time"),
                "number": current_record.get("time"),
                "name": current_record.get("name")
            }

            text = form_completion(f"Запис {i}", record_data=temp_record)
            msg = await message.answer(text=text, reply_markup=remove_inline(f"record_{msg_text}_{i}", "Видалити"))
            add_msg_to_delete(user_id=uid, msg_id=msg.message_id)
    elif name == "ban_user":
        if msg_text in black_list:
            msg_wrong_id = await message.answer("<b>Даний користувач вже заблокований</b>", reply_markup=markup)
            temp_msgid_state[uid] = msg_wrong_id.message_id
            add_msg_to_delete(user_id=uid, msg_id=msg_wrong_id.message_id)
            return

        dt = datetime.now()
        msg = await message.answer(f"<b>Ви дійсно хочете заблокувати користувача з \nID: {msg_text}?</b>",
                                   reply_markup=remove_inline(
                                       f"banuser_{msg_text}_{dt.date()}_{dt.hour}-{dt.minute}", "Заблокувати"))
        add_msg_to_delete(user_id=uid, msg_id=msg.message_id)
    elif name == "unban_user":
        if msg_text not in black_list:
            msg_wrong_id = await message.answer("<b>Даний користувач не заблокований</b>", reply_markup=markup)
            temp_msgid_state[uid] = msg_wrong_id.message_id
            add_msg_to_delete(user_id=uid, msg_id=msg_wrong_id.message_id)
            return

        msg = await message.answer(f"<b>Ви дійсно хочете розблокувати користувача з \nID: {msg_text}?</b>",
                                   reply_markup=remove_inline(f"unbanuser_{msg_text}_none", "Розблокувати"))
        add_msg_to_delete(user_id=uid, msg_id=msg.message_id)

    await state.finish()


def register_act_on_users(dp: Dispatcher):
    dp.register_callback_query_handler(write_user_id, ChatTypeFilter(types.ChatType.PRIVATE),
                                       tc.filter(title="act_on_users"))
    dp.register_message_handler(show_userdata, state=FindData.UserId)
    dp.register_callback_query_handler(show_userdata, state=FindData.UserId, text="back")
