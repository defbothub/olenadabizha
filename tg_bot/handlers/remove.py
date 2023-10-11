from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter

from tg_bot.keyboards.inline.callback_data import temp_callback as tc
from tg_bot.keyboards.inline.remove_confirm_keyb import remove_confirm
from tg_bot.misc.data_handling import black_list
from tg_bot.misc.utils import remove_record


async def remove_confirmation(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()

    name = callback_data.get("name")
    text = callback.message.text
    await callback.message.edit_text(text=text, reply_markup=remove_confirm(name))


async def remove_data(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()

    name = callback_data.get("name")
    if name == "disagree":
        await callback.message.edit_text("<b>Ви відмовились від дії</b>")
        return

    name_ = name.split('_')
    user_id = name_[1]
    data_number = name_[2]
    temp = None

    if name_[0] == "banuser":
        black_list[user_id] = f"{name_[2]}_{name_[3]}"
        temp = "блокування користувача"
    elif name_[0] == "unbanuser":
        black_list.pop(user_id)
        temp = "розблокування користувача"

    if name_[0] == "record":
        remove_record(user_id, data_number)
        temp = "видалення запису"

    await callback.message.edit_text(f"<b>Ви підтвердили {temp}</b>")


def register_remove_data(dp: Dispatcher):
    dp.register_callback_query_handler(remove_confirmation, ChatTypeFilter(types.ChatType.PRIVATE),
                                       tc.filter(title="remove"))
    dp.register_callback_query_handler(remove_data, ChatTypeFilter(types.ChatType.PRIVATE),
                                       tc.filter(title="agreement"))
