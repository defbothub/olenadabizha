from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, Text, Command

from tg_bot.keyboards.inline.callback_data import temp_callback as tc
from tg_bot.keyboards.inline.questions_keyb import questions_keyboard, back_keyboard
from tg_bot.misc.data_handling import questions


async def show_questions(message: types.Message, edit_text: bool = False):
    if edit_text:
        await message.edit_text(text="<b>Часті питання</b>", reply_markup=questions_keyboard())
    else:
        await message.answer(text="<b>Часті питання</b>", reply_markup=questions_keyboard())


async def show_category_body(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()

    category = callback_data.get("name")
    if category == "back":
        return await show_questions(callback.message, edit_text=True)

    body = questions.get(category)
    body.insert(0, f"<b>{category}</b>\n")

    await callback.message.edit_text(text='\n'.join(body), reply_markup=back_keyboard)


def register_common_questions(dp: Dispatcher):
    dp.register_message_handler(show_questions, ChatTypeFilter(types.ChatType.PRIVATE),
                                Text("Поширені питання") | Command("common_questions"))
    dp.register_callback_query_handler(show_category_body, ChatTypeFilter(types.ChatType.PRIVATE),
                                       tc.filter(title="question"))
