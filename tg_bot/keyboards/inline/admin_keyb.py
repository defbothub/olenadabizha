import calendar
from datetime import datetime, time, timedelta

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.config import Config
from tg_bot.keyboards.inline.callback_data import temp_callback as tc, calendar_callback as cc, time_callback as tcb
from tg_bot.misc.data_handling import timeline, all_records, amount_time_per_service

panel_inline = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="Графік", callback_data="work_schedule")
                                        ],
                                        [
                                            InlineKeyboardButton(text="Знайти запис",
                                                                 callback_data=tc.new(title="act_on_users",
                                                                                      name="record"))
                                        ],
                                        [
                                            InlineKeyboardButton(text="Заблокувати",
                                                                 callback_data=tc.new(title="act_on_users",
                                                                                      name="ban_user")),
                                            InlineKeyboardButton(text="Розблокувати",
                                                                 callback_data=tc.new(title="act_on_users",
                                                                                      name="unban_user"))
                                        ],
                                        [
                                            InlineKeyboardButton(text="Чорний список", callback_data="black_list")
                                        ]
                                    ])


def back_inline(name: str):
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data=name)]])


def work_schedule_calendar(year: int, month: int, day_: int):
    keyboard = InlineKeyboardMarkup(row_width=7,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="Пн",
                                                                 callback_data=cc.new(title="adm_calendar",
                                                                                      arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Вт",
                                                                 callback_data=cc.new(title="adm_calendar",
                                                                                      arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Ср",
                                                                 callback_data=cc.new(title="adm_calendar",
                                                                                      arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Чт",
                                                                 callback_data=cc.new(title="adm_calendar",
                                                                                      arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Пт",
                                                                 callback_data=cc.new(title="adm_calendar",
                                                                                      arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Сб",
                                                                 callback_data=cc.new(title="adm_calendar",
                                                                                      arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none")),
                                            InlineKeyboardButton(text="Нд",
                                                                 callback_data=cc.new(title="adm_calendar",
                                                                                      arg1="weekday",
                                                                                      arg2="unclick", arg3="none",
                                                                                      arg4="none"))
                                        ]
                                    ])

    month_days = calendar.Calendar().itermonthdays(year, month)
    for day in month_days:
        temp_symbol = ""
        temp = day
        try:
            if day_ > day:
                day = " "
                temp = "unclick"
        except TypeError:
            pass

        if temp != "unclick":
            counter = 0
            for time in timeline:
                if (str(year) in timeline[time]) and (str(month) in timeline[time][str(year)]) and \
                        (str(day) in timeline[time][str(year)][str(month)]):
                    counter += 1

                if counter >= len(timeline):
                    temp_symbol = " ❌"

        button = InlineKeyboardButton(text=(str(day) + temp_symbol),
                                      callback_data=cc.new(title="adm_calendar", arg1="day", arg2=temp, arg3=month,
                                                           arg4=year))
        keyboard.insert(button)

    all_months = {1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень", 5: "Травень", 6: "Червень", 7: "Липень",
                  8: "Серпень", 9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"}

    left = InlineKeyboardButton(text="<",
                                callback_data=cc.new(title="adm_calendar", arg1="move", arg2="left", arg3="none",
                                                     arg4="none"))
    current_month = InlineKeyboardButton(text=f"{all_months[month]} {year}",
                                         callback_data=cc.new(title="adm_calendar", arg1="cur_month", arg2="unclick",
                                                              arg3="none",
                                                              arg4="none"))
    right = InlineKeyboardButton(text=">",
                                 callback_data=cc.new(title="adm_calendar", arg1="move", arg2="right", arg3="none",
                                                      arg4="none"))
    keyboard.insert(left)
    keyboard.insert(current_month)
    keyboard.insert(right)

    back = InlineKeyboardButton(text="Назад",
                                callback_data=cc.new(title="adm_calendar", arg1="back", arg2="back", arg3="back",
                                                     arg4="back"))
    keyboard.row(back)

    return keyboard


def work_schedule_time(year: int, month: int, day: int):
    temp_time = {}
    keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=[])
    input_date = datetime(int(year), int(month), int(day))
    current_datetime = datetime.now(Config.TIMEZONE)
    counter = 0
    for i in timeline:
        if i in temp_time:
            continue

        symbol = " ✔"
        temp = i.split(':')
        calldata = tcb.new(title="adm_time", hour=temp[0], minute=temp[1])
        if input_date.date() == current_datetime.date():
            hour, minute = current_datetime.hour, current_datetime.minute
            current_time = time(hour, minute)
            job_time = time(int(temp[0]), int(temp[1]))
            if current_time > job_time:
                continue

        if (str(year) in timeline[i]) and (str(month) in timeline[i][str(year)]) and \
                (str(day) in timeline[i][str(year)][str(month)]):
            uid = timeline[i][str(year)][str(month)][str(day)]
            for n in all_records[uid]:
                date = all_records[uid][n]["date"].split('.')
                time_data = all_records[uid][n]["time"]
                if date[0] == str(day) and date[1] == str(month) and date[2] == str(year):
                    if i == time_data:
                        symbol = " ❌"
                        service = all_records[uid][n]["service"]
                        time_list = time_data.split(":")

                        amount_time_split = amount_time_per_service[service].split(':')

                        will_take_time_ = timedelta(hours=int(amount_time_split[0]), minutes=int(amount_time_split[1]))
                        time_start = timedelta(hours=int(time_list[0]), minutes=int(time_list[1]))
                        time_end = time_start + will_take_time_
                        while time_start != time_end:
                            time_start_list = str(time_start).split(':')
                            temp_time.update({f"{time_start_list[0]}:{time_start_list[1]}": uid})

                            time_start += timedelta(minutes=30)

                    calldata = tcb.new(title="adm_time", hour="show_record", minute=f"{uid}_{n}")
        else:
            counter += 1
        # Не відображається червоний хрестик на зайнятому часу
        button = InlineKeyboardButton(text=(i + symbol), callback_data=calldata)
        keyboard.insert(button)

    if counter >= len(timeline):
        take_all_day = InlineKeyboardButton(text="Зайняти весь день",
                                            callback_data=tcb.new(title="adm_time", hour="all_day", minute="all_day"))
        keyboard.row(take_all_day)

    back = InlineKeyboardButton(text="Назад", callback_data=tcb.new(title="adm_time", hour="back", minute="back"))
    keyboard.row(back)

    return keyboard


def confirm_weekend(calldata: str):
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="Підтверджую",
                                                                 callback_data=tc.new(title="make_weekend",
                                                                                      name=calldata)),
                                            InlineKeyboardButton(text="Назад",
                                                                 callback_data=tc.new(title="make_weekend",
                                                                                      name="back"))
                                        ]
                                    ])
    return keyboard


back_to_time_selection = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Повернутись до часу", callback_data="back_to_time_selection")]])
