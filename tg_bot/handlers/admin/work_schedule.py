import logging
from datetime import datetime, timedelta

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter

from tg_bot.config import Config
from tg_bot.filters.isAdmin import IsAdmin
from tg_bot.handlers.admin.panel import cmd_panel
from tg_bot.keyboards.inline.admin_keyb import work_schedule_calendar, work_schedule_time, back_inline, confirm_weekend, \
    back_to_time_selection
from tg_bot.keyboards.inline.callback_data import calendar_callback as cc, time_callback as tcb, temp_callback as tc
from tg_bot.misc.data_handling import all_records, timeline, amount_time_per_service
from tg_bot.misc.utils import form_completion, add_msg_to_delete

t_year, t_month, t_day = {}, {}, {}
temp_calldata = {}

logger = logging.getLogger(__name__)


async def show_calendar(callback: types.CallbackQuery):
    await callback.answer()

    uid = callback.from_user.id
    if uid in t_year:
        try:
            t_year.pop(uid)
            t_month.pop(uid)
            t_day.pop(uid)
        except KeyError:
            pass

    today = datetime.now(Config.TIMEZONE)
    msg = await callback.message.edit_text(text="<b>Графік роботи</b>",
                                           reply_markup=work_schedule_calendar(today.year, today.month, today.day))
    add_msg_to_delete(user_id=uid, msg_id=msg.message_id)


async def selected_date(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()

    global t_year
    global t_month
    global t_day

    arg1, arg2, arg3 = callback_data.get('arg1'), callback_data.get('arg2'), callback_data.get('arg3')
    arg4 = callback_data.get('arg4')
    today = datetime.now(Config.TIMEZONE)
    uid = callback.from_user.id

    if arg1 == "back":
        await cmd_panel(callback)
        return
    elif arg2 == "unclick":
        return
    elif arg1 == "day":
        temp_calldata[uid] = callback_data
        await callback.message.edit_text(text="<b>Виберіть час для взаємодії</b>",
                                         reply_markup=work_schedule_time(int(arg4), int(arg3), int(arg2)))
        return
    elif arg1 == "move":
        if uid not in t_year:
            t_year[uid] = today.year
            t_month[uid] = today.month

        if arg2 == "left":
            if t_year[uid] == today.year:
                if t_month[uid] == today.month:
                    t_day[uid] = today.day
                    return
                else:
                    if (today.month + 1) == t_month[uid]:
                        t_day[uid] = today.day
                    if t_month[uid] == 1:
                        t_year[uid] -= 1
                        t_month[uid] = 12
                    else:
                        t_month[uid] -= 1
            else:
                if t_month[uid] == 1:
                    t_year[uid] -= 1
                    t_month[uid] = 12
                else:
                    t_month[uid] -= 1
        elif arg2 == "right":
            t_day[uid] = 1
            if t_month[uid] == 12:
                t_year[uid] += 1
                t_month[uid] = 1
            else:
                t_month[uid] += 1

    await callback.message.edit_reply_markup(reply_markup=work_schedule_calendar(t_year[uid], t_month[uid], t_day[uid]))


async def selected_time(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()

    hour, minute = callback_data.get("hour"), callback_data.get("minute")
    if hour == "back":
        await show_calendar(callback)
        return

    if hour == "show_record":
        userdata = minute.split("_")
        uid, record_number = userdata[0], userdata[1]

        current_record = all_records[uid][record_number]
        temp_record = {
            "service": current_record.get("service"),
            "date": current_record.get("date"),
            "time": current_record.get("time"),
            "number": current_record.get("number"),
            "name": current_record.get("name")
        }

        text = form_completion(f"Запис {record_number} користувача з \nID: {uid}", record_data=temp_record)
        await callback.message.edit_text(text=text, reply_markup=back_inline("back_from_record"))
        return

    if hour == "all_day":
        await callback.message.edit_text("<b>Ви дійсно хочете зайняти повний день?</b>",
                                         reply_markup=confirm_weekend("all_day"))
        return

    await callback.message.edit_text("<b>Ви дійсно хочете зайняти цей час для інших справ?</b>",
                                     reply_markup=confirm_weekend(f"{hour}_{minute}"))


async def make_weekend(callback: types.CallbackQuery, callback_data: dict):
    await callback.answer()

    name = callback_data.get("name")
    uid = callback.from_user.id
    day, month, year = temp_calldata[uid].get('arg2'), temp_calldata[uid].get('arg3'), temp_calldata[uid].get('arg4')
    if name == "back":
        await selected_date(callback, temp_calldata[uid])
        return

    if name == "all_day":
        for tm in timeline:
            record = {"service": "Вихідний", "date": f"{day}.{month}.{year}",
                      "time": tm, "number": "admin", "name": "admin"}
            if "weekend" not in all_records:
                all_records["weekend"] = {"1": record}
            else:
                all_records["weekend"].update({str(len(all_records["weekend"]) + 1): record})

            if year in timeline[tm]:
                if month in timeline[tm][year]:
                    timeline[tm][year][month][day] = "weekend"
                else:
                    timeline[tm][year].update({month: {day: "weekend"}})
            else:
                timeline[tm].update({year: {month: {day: "weekend"}}})
        temp_text = "день"
    else:
        time = name.split('_')
        record = {
            "service": "Вихідний",
            "date": f"{day}.{month}.{year}",
            "time": f"{time[0]}:{time[1]}",
            "number": "admin",
            "name": "admin"
        }

        if "weekend" not in all_records:
            all_records["weekend"] = {"1": record}
        else:
            all_records["weekend"].update({str(len(all_records["weekend"])): record})

        time_start = timedelta(hours=int(time[0]), minutes=int(time[1]))
        amount_time = amount_time_per_service["Вихідний"].split(':')
        will_take_time_ = timedelta(hours=int(amount_time[0]), minutes=int(amount_time[1]))
        time_end = time_start + will_take_time_
        while time_start != time_end:
            time_list = str(time_start).split(':')
            time_str = f"{time_list[0]}:{time_list[1]}"
            if time_start > timedelta(hours=19):
                break

            if year in timeline[time_str]:
                if month in timeline[time_str][year]:
                    timeline[time_str][year][month][day] = "weekend"
                else:
                    timeline[time_str][year].update({month: {day: "weekend"}})
            else:
                timeline[time_str].update({year: {month: {day: "weekend"}}})

            time_start += timedelta(minutes=30)
        temp_text = "час"

    await callback.message.edit_text(f"<b>Ви успішно зайняли цей {temp_text}</b>", reply_markup=back_to_time_selection)


async def back_from_schedule(callback: types.CallbackQuery):
    await callback.answer()
    await selected_date(callback, temp_calldata[callback.from_user.id])


async def back_to_time_select(callback: types.CallbackQuery):
    await callback.answer()
    await selected_date(callback, temp_calldata[callback.from_user.id])


def register_work_schedule(dp: Dispatcher):
    dp.register_callback_query_handler(show_calendar, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                       text="work_schedule")
    dp.register_callback_query_handler(selected_date, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                       cc.filter(title="adm_calendar"))
    dp.register_callback_query_handler(selected_time, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                       tcb.filter(title="adm_time"))
    dp.register_callback_query_handler(make_weekend, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                       tc.filter(title="make_weekend"))
    dp.register_callback_query_handler(back_from_schedule, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                       text="back_from_record")
    dp.register_callback_query_handler(back_to_time_select, ChatTypeFilter(types.ChatType.PRIVATE), IsAdmin(),
                                       text="back_to_time_selection")
