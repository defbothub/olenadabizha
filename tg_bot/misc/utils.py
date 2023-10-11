from datetime import timedelta
from typing import Optional

from aiogram import Bot
from aiogram.utils.exceptions import MessageToDeleteNotFound
from aiogram.utils.markdown import hcode

from tg_bot.misc.data_handling import msg_to_delete, all_records, timeline, reminder, amount_time_per_service


def form_completion(title: str, record_data: Optional[dict] = None) -> str:
    if record_data:
        service = record_data.get("service")
        date = record_data.get("date")
        time = record_data.get("time")
        number = record_data.get("number")
        name = record_data.get("name")
    else:
        service, date, time, number, name = None, None, None, None, None

    text = [
        f"<b>{title}</b>",
        f"{hcode('Послуга:')} {service if service else ''}",
        f"{hcode('Дата:')} {date if date else ''}",
        f"{hcode('Час:')} {time if time else ''}",
        f"{hcode('Телефон:')} {number if number else ''}",
        hcode('Ім\'я: ') + str(name if name else '')
    ]
    return '\n\n'.join(text)


def add_msg_to_delete(user_id: int, msg_id: int):
    if user_id not in msg_to_delete:
        msg_to_delete[user_id] = []

    msg_to_delete[user_id].append(msg_id)


async def delete_messages(user_id: Optional[int] = None):
    try:
        if not user_id:
            for uid in msg_to_delete:
                for msg_id in msg_to_delete.get(uid):
                    try:
                        await Bot.get_current().delete_message(chat_id=uid, message_id=msg_id)
                    except MessageToDeleteNotFound:
                        continue

            return

        for msg_id in msg_to_delete[user_id]:
            try:
                await Bot.get_current().delete_message(chat_id=user_id, message_id=msg_id)
            except MessageToDeleteNotFound:
                continue

        msg_to_delete[user_id].clear()
    except KeyError:
        return


def remove_record(user_id: str, record_index: str):
    date = all_records[user_id][record_index]["date"].split('.')
    time = all_records[user_id][record_index]["time"].split(':')
    day, month, year = date[0], date[1], date[2]

    time_amount_split = amount_time_per_service.get(all_records[user_id][record_index]["service"]).split(':')
    will_take_time_ = timedelta(hours=int(time_amount_split[0]), minutes=int(time_amount_split[1]))
    time_start = timedelta(hours=int(time[0]), minutes=int(time[1]))
    time_end = time_start + will_take_time_
    while time_start != time_end:
        time_start_ = str(time_start).split(':')
        time_str = f"{time_start_[0]}:{time_start_[1]}"
        if time_start > timedelta(hours=19):
            break

        timeline[time_str][year][month].pop(day)
        if len(timeline[time_str][year][month]) == 0:
            timeline[time_str][year].pop(month)
            if len(timeline[time_str][year]) == 0:
                timeline[time_str].pop(year)

        time_start += timedelta(minutes=30)

    all_records[user_id].pop(record_index)
    if len(all_records[user_id]) == 0:
        all_records.pop(user_id)
