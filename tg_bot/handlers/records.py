from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, Command, Text

from tg_bot.keyboards.inline.remove_keyb import remove_inline
from tg_bot.misc.data_handling import all_records
from tg_bot.misc.utils import form_completion, delete_messages, add_msg_to_delete


async def show_records(message: types.Message):
    uid = message.from_user.id

    await delete_messages(uid)

    if str(uid) not in all_records:
        await message.answer("<b>У вас немає активних записів</b>")
        return

    for i in all_records[str(uid)]:
        current_record = all_records[str(uid)][i]
        temp_record = {
            "service": current_record.get("service"),
            "date": current_record.get("date"),
            "time": current_record.get("time"),
            "number": current_record.get("number"),
            "name": current_record.get("name")
        }

        text = form_completion(f"Запис {i}", record_data=temp_record)
        msg = await message.answer(text=text, reply_markup=remove_inline(f"record_{uid}_{i}", "Видалити"))
        add_msg_to_delete(user_id=uid, msg_id=msg.message_id)


def register_records(dp: Dispatcher):
    dp.register_message_handler(show_records, ChatTypeFilter(types.ChatType.PRIVATE),
                                Text("Мої записи") | Command('records'))
