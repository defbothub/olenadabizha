from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hcode

from tg_bot.misc.utils import add_msg_to_delete


async def show_price(callback: types.CallbackQuery):
    await callback.answer()

    text = [
        "<b>Прайс</b>",
        f"\nПослуга - <b>Онлайн консультація</b>",
        f"Вартість: {hcode('1000')} грн. Час: 30 хв.",
        f"\nПослуга - <b>Консультація в офісі</b>",
        f"Вартість: {hcode('1500')} грн. Час: 30 хв.",
        "\n<b>Реквізити:</b>",
        f"Найменування отримувача: {hcode('ФОП Дабіжа Олена Анатоліївна')}",
        f"Код отримувача: {hcode(3361604228)}",
        f"Рахунок отримувача: {hcode('UA303052990000026218004900452')}",
        "Назва банку: " + hcode('АТ КБ "ПРИВАТБАНК"')
    ]
    markup = InlineKeyboardMarkup(row_width=1,
                                  inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back_price")]])
    msg = await callback.message.edit_text('\n'.join(text), reply_markup=markup)
    add_msg_to_delete(user_id=callback.from_user.id, msg_id=msg.message_id)


def register_menu_price(dp: Dispatcher):
    dp.register_callback_query_handler(show_price, ChatTypeFilter(types.ChatType.PRIVATE), text="price")
