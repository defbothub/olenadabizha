from typing import Union

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.inline.callback_data import question_callback as qc
from tg_bot.misc.data_handling import categories, subcategories


def questions_keyboard(category: Union[bool, str] = False, subcategory: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    flag = True
    if category and subcategory:
        ct_ind = categories.index(category)
        for i in subcategories[category]:
            subct_ind = subcategories[category].index(i)
            button = InlineKeyboardButton(
                text=i, callback_data=qc.new(title="question", category=ct_ind, subcategory=subct_ind))
            markup.row(button)
    elif category:
        flag = False
        for i in categories:
            ct_ind = categories.index(i)
            button = InlineKeyboardButton(
                text=i, callback_data=qc.new(title="question", category=ct_ind, subcategory="no"))
            markup.row(button)

    if flag:
        button = InlineKeyboardButton(
            text="Назад", callback_data=qc.new(title="question", category="no", subcategory="no"))
        markup.row(button)

    return markup
