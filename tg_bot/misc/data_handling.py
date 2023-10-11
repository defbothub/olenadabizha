import json
import logging
from typing import Dict

all_records, reminder, black_list = {}, {}, {}
questions: Dict[str, list] = {}

services = {"online_consultation": "Онлайн консультація", "office_consultation": "Консультація в офісі"}
timeline = {"9:00": {}, "9:30": {}, "10:00": {}, "10:30": {}, "11:00": {}, "11:30": {}, "12:00": {}, "12:30": {},
            "13:00": {}, "13:30": {}, "14:00": {}, "14:30": {}, "15:00": {}, "15:30": {}, "16:00": {}, "16:30": {},
            "17:00": {}, "17:30": {}, "18:00": {}, "18:30": {}, "19:00": {}}

amount_time_per_service = {"Онлайн консультація": "00:30", "Консультація в офісі": "00:30", "Вихідний": "1:00"}
service_prices = {"Онлайн консультація": 1000, "Консультація в офісі": 1500}

msg_to_delete = {"all": [], "fill": []}

logger = logging.getLogger(__name__)


async def upload_data():
    with open("tg_bot/misc/data/all_records.json", "w", encoding="utf-8-sig") as file:
        json.dump(all_records, file, indent=4, ensure_ascii=False)

    with open("tg_bot/misc/data/timeline.json", "w", encoding="utf-8-sig") as file:
        json.dump(timeline, file, indent=4, ensure_ascii=False)

    with open("tg_bot/misc/data/reminder.json", "w", encoding="utf-8-sig") as file:
        json.dump(reminder, file, indent=4, ensure_ascii=False)

    with open("tg_bot/misc/data/black_list.json", "w", encoding="utf-8-sig") as file:
        json.dump(black_list, file, indent=4, ensure_ascii=False)

    with open("tg_bot/misc/data/questions.json", "w", encoding="utf-8-sig") as file:
        json.dump(questions, file, indent=4, ensure_ascii=False)

    logger.info("Data has been successfully uploaded!")


async def load_data():
    try:
        with open("tg_bot/misc/data/all_records.json", encoding="utf-8-sig") as file:
            all_records.update(json.load(file))

        with open("tg_bot/misc/data/timeline.json", "r", encoding="utf-8-sig") as file:
            timeline.update(json.load(file))

        with open("tg_bot/misc/data/reminder.json", "r", encoding="utf-8-sig") as file:
            reminder.update(json.load(file))

        with open("tg_bot/misc/data/black_list.json", "r", encoding="utf-8-sig") as file:
            black_list.update(json.load(file))

        with open("tg_bot/misc/data/questions.json", "r", encoding="utf-8-sig") as file:
            questions.update(json.load(file))
    except FileNotFoundError:
        pass

    logger.info("Data has been successfully loaded!")
