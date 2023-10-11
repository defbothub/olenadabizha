from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, Command, Text
from aiogram.utils.markdown import hcode

from tg_bot.filters.isAdmin import IsAdmin
from tg_bot.keyboards.inline.admin_keyb import panel_inline
from tg_bot.misc.data_handling import all_records
from tg_bot.misc.utils import delete_messages, add_msg_to_delete


async def cmd_panel(message: types.Message | types.CallbackQuery):
    if isinstance(message, types.CallbackQuery):
        uid = message.from_user.id
        message = message.message
    else:
        uid = message.from_user.id
        await message.delete()

    await delete_messages(uid)

    records_count = 0
    for user_id in all_records:
        for record_index in all_records[user_id]:
            if all_records[user_id][record_index].get("service") == "Вихідний":
                continue

            records_count += 1

    text = [
        "<b>Ви увішли в адмін панель</b>",
        f"{hcode('На даний момент активних записів:')} {records_count}",
        "\n<b>Виберіть одну з функцій</b>"
    ]
    msg = await message.answer('\n\n'.join(text), reply_markup=panel_inline)
    add_msg_to_delete(user_id=uid, msg_id=msg.message_id)


def register_panel(dp: Dispatcher):
    dp.register_message_handler(cmd_panel, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                Text("Адмін панель") | Command('apanel'))
