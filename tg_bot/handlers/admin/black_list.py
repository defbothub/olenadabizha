from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.utils.markdown import hcode

from tg_bot.filters.isAdmin import IsAdmin
from tg_bot.handlers.admin.panel import cmd_panel
from tg_bot.keyboards.inline.admin_keyb import back_inline
from tg_bot.misc.data_handling import black_list


async def show_black_list(callback: types.CallbackQuery):
    await callback.answer()

    text = ["<b>Список заблокованих користувачів</b>\n"]
    for uid in black_list:
        date = black_list[uid].split('_')
        time = date[1].split('-')
        temp = f"ID: {hcode(uid)} | Дата блокування: {date[0]}  {time[0]}:{time[1]}"
        text.append(temp)

    await callback.message.edit_text('\n'.join(text), reply_markup=back_inline("back_from_black_list"))


async def back_from_black_list(callback: types.CallbackQuery):
    await callback.answer()

    await cmd_panel(callback)


def register_black_list(dp: Dispatcher):
    dp.register_callback_query_handler(show_black_list, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                       text="black_list")
    dp.register_callback_query_handler(back_from_black_list, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                       text="back_from_black_list")
