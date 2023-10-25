import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter, Text, Command

from tg_bot.keyboards.default.start_keyb import title_common_questions
from tg_bot.keyboards.inline.callback_data import question_callback as qc
from tg_bot.keyboards.inline.questions_keyb import questions_keyboard
from tg_bot.misc.data_handling import questions, categories, subcategories

logger = logging.getLogger(__name__)


async def show_questions(message: types.Message, edit_text: bool = False):
    text = "<b>Щоб заощадити час на консультації, ознайомтеся з відповідями на питання, які вас можуть цікавити.👇 </b>"
    if edit_text:
        await message.edit_text(text=text, reply_markup=questions_keyboard(category=True))
    else:
        await message.answer(text=text, reply_markup=questions_keyboard(category=True))


async def show_category_data(callback: types.CallbackQuery, callback_data: dict):
    category = callback_data.get("category")
    subcategory = callback_data.get("subcategory")
    if category != "no" and subcategory != "no":
        category = categories[int(category)]
        subcategory = subcategories[category][int(subcategory)]
        body = questions[category][subcategory]
        await callback.message.edit_text(text=f"<b>{category}\n{subcategory}</b>\n\n" + '\n'.join(body),
                                         reply_markup=questions_keyboard())
    elif category != "no":
        category = categories[int(category)]
        await callback.message.edit_text(text=f"<b>{category}</b>\n\n",
                                         reply_markup=questions_keyboard(category=category, subcategory=True))
    else:
        return await show_questions(message=callback.message, edit_text=True)


def register_common_questions(dp: Dispatcher):
    dp.register_message_handler(show_questions, ChatTypeFilter(types.ChatType.PRIVATE),
                                Text(title_common_questions) | Command("common_questions"))
    dp.register_callback_query_handler(show_category_data, ChatTypeFilter(types.ChatType.PRIVATE),
                                       qc.filter(title="question"))
