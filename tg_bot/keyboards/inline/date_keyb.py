import calendar
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.inline.callback_data import calendar_callback as cc
from tg_bot.misc.data_handling import timeline


def calendar_keyboard(year: int, month: int, day_: int):
    keyboard = InlineKeyboardMarkup(row_width=7,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="Пн",
                                                                 callback_data=cc.new(title="calendar", arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Вт",
                                                                 callback_data=cc.new(title="calendar", arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Ср",
                                                                 callback_data=cc.new(title="calendar", arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Чт",
                                                                 callback_data=cc.new(title="calendar", arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Пт",
                                                                 callback_data=cc.new(title="calendar", arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Сб",
                                                                 callback_data=cc.new(title="calendar", arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Нд",
                                                                 callback_data=cc.new(title="calendar", arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none"))
                                        ]
                                    ])

    month_days = calendar.Calendar().itermonthdays(year, month)
    for day in month_days:
        temp = day
        if day_ > day:
            day = " "
            temp = "unclick"

        if temp != "unclick":
            counter = 0
            for time in timeline:
                if (str(year) in timeline[time]) and (str(month) in timeline[time][str(year)]) and \
                        (str(day) in timeline[time][str(year)][str(month)]):
                    counter += 1

            if counter >= 21:
                day = "❌"
                temp = "unclick"

        button = InlineKeyboardButton(text=str(day),
                                      callback_data=cc.new(title="calendar", arg1="day", arg2=temp, arg3=month,
                                                           arg4=year))
        keyboard.insert(button)

    all_months = {1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень", 5: "Травень", 6: "Червень", 7: "Липень",
                  8: "Серпень", 9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"}

    left = InlineKeyboardButton(text="<", callback_data=cc.new(title="calendar", arg1="move", arg2="left", arg3="none",
                                                               arg4="none"))
    current_month = InlineKeyboardButton(text=f"{all_months[month]} {year}",
                                         callback_data=cc.new(title="calendar", arg1="cur_month", arg2="unclick",
                                                              arg3="none",
                                                              arg4="none"))
    right = InlineKeyboardButton(text=">",
                                 callback_data=cc.new(title="calendar", arg1="move", arg2="right", arg3="none",
                                                      arg4="none"))
    keyboard.insert(left)
    keyboard.insert(current_month)
    keyboard.insert(right)

    back = InlineKeyboardButton(text="Назад",
                                callback_data=cc.new(title="calendar", arg1="back", arg2="back", arg3="back",
                                                     arg4="back"))
    keyboard.row(back)

    return keyboard
