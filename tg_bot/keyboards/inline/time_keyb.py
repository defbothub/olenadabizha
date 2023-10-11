from datetime import datetime, time, date, timedelta

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from tg_bot.misc.data_handling import amount_time_per_service, timeline
from tg_bot.keyboards.inline.callback_data import time_callback as tcb


def time_keyboard(year: int, month: int, day: int, service: str):
    keyboard = InlineKeyboardMarkup(row_width=3, inline_keyboard=[])
    input_date = date(int(year), int(month), int(day))
    current_datetime = datetime.now()
    for i in timeline:
        temp = i.split(':')
        if input_date == current_datetime.date():
            hour, minute = current_datetime.hour, current_datetime.minute
            current_time = time(hour, minute)
            job_time = time(int(temp[0]), int(temp[1]))
            if current_time > job_time:
                continue

        if (str(year) in timeline[i]) and (str(month) in timeline[i][str(year)]) and \
                (str(day) in timeline[i][str(year)][str(month)]):
            continue

        time_splited = amount_time_per_service.get(service).split(":")
        will_take_time_ = timedelta(hours=int(time_splited[0]), minutes=int(time_splited[1]))
        tm_start = timedelta(hours=int(temp[0]), minutes=int(temp[1]))
        tm_end = tm_start + will_take_time_

        flag = True
        for tm in timeline:
            tm_list = tm.split(':')
            tm_delta = timedelta(hours=int(tm_list[0]), minutes=int(tm_list[1]))
            if tm_delta <= tm_start or tm_delta > tm_end:
                continue
            else:
                year, month, day = str(year), str(month), str(day)
                if (year in timeline[tm]) and (month in timeline[tm][year]) and (day in timeline[tm][year][month]):
                    flag = False
                    break

        if not flag:
            continue

        button = InlineKeyboardButton(text=f"{temp[0]}:{temp[1]}",
                                      callback_data=tcb.new(title="time", hour=int(temp[0]), minute=int(temp[1])))
        keyboard.insert(button)

    back = InlineKeyboardButton(text="Назад", callback_data=tcb.new("time", hour="back", minute="back"))
    keyboard.row(back)

    return keyboard
