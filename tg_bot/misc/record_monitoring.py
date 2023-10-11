import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot, types

from tg_bot.config import Config
from tg_bot.misc.data_handling import timeline, all_records, reminder
from tg_bot.misc.utils import remove_record, form_completion

logger = logging.getLogger(__name__)


async def record_monitor(first_start: bool = False):
    if first_start:
        logger.info(f"Monitoring has been started!")

    bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    while True:
        await asyncio.sleep(7)
        for time in timeline:
            for year in timeline[time]:
                for month in timeline[time][year]:
                    for day in timeline[time][year][month]:
                        time_ = time.split(':')
                        current_time = datetime.now()
                        record_time = datetime(int(year), int(month), int(day), int(time_[0]), int(time_[1]))
                        flag = False
                        if current_time >= record_time:
                            user_id = timeline[time][year][month][day]
                            for i in all_records[user_id]:
                                if all_records[user_id][i]["time"] == time:
                                    if "Вихідний" not in all_records[user_id][i].get("service"):
                                        current_record = all_records[user_id][i]
                                        temp_record = {
                                            "service": current_record.get("service"),
                                            "date": current_record.get("date"),
                                            "time": current_record.get("time"),
                                            "number": current_record.get("number"),
                                            "name": current_record.get("name")
                                        }
                                        text = form_completion(
                                            "Підійшов час, на який ви записувась\nЗапис буде видалено автоматично",
                                            record_data=temp_record
                                        )

                                        await bot.send_message(chat_id=int(user_id), text=text)

                                    remove_record(user_id, record_index=i)

                                    await record_monitor()

                        if current_time.date() == record_time.date():
                            user_id = timeline[time][year][month][day]
                            if user_id not in reminder:
                                continue
                            else:
                                flag = True
                                for n in reminder[user_id]:
                                    if reminder[user_id][n] == time:
                                        flag = False
                                        break
                                if flag:
                                    continue

                            current_time_delta = timedelta(hours=current_time.hour, minutes=current_time.minute)
                            record_time_delta = timedelta(hours=record_time.hour, minutes=record_time.minute)
                            min_time_delta = record_time_delta - timedelta(hours=2)
                            if min_time_delta < current_time_delta < record_time_delta:
                                for i in all_records[user_id]:
                                    if all_records[user_id][i]["time"] == time:
                                        current_record = all_records[user_id][i]
                                        temp_record = {
                                            "service": current_record.get("service"),
                                            "date": current_record.get("date"),
                                            "time": current_record.get("time"),
                                            "number": current_record.get("number"),
                                            "name": current_record.get("name")
                                        }

                                        temp = str(record_time_delta - current_time_delta).split(':')
                                        text = form_completion(
                                            f"Через {temp[0]}:{temp[1]} вам потрібно прийти по запису",
                                            record_data=temp_record
                                        )

                                        await bot.send_message(chat_id=int(user_id), text=text)

                                        reminder[user_id].pop(str(i))
                                        if len(reminder[user_id]) == 0:
                                            reminder.pop(user_id)

                                        break