from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.inline.callback_data import temp_callback as tc


def remove_confirm(name: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="Підтверджую",
                                                                 callback_data=tc.new(title="agreement", name=name)),
                                            InlineKeyboardButton(text="Відмовляюсь",
                                                                 callback_data=tc.new(title="agreement",
                                                                                      name="disagree"))
                                        ]
                                    ])
    return keyboard
