import asyncio
import logging

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils import executor

from tg_bot.config import Config
from tg_bot.handlers import *
from tg_bot.filters import *
from tg_bot.middlewares import *
from tg_bot.misc.record_monitoring import record_monitor
from tg_bot.misc.data_handling import load_data, upload_data
from tg_bot.misc.utils import delete_messages

logger = logging.getLogger(__name__)


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Головне меню"),
        BotCommand(command="/filling", description="Почати запис"),
        BotCommand(command="/records", description="Ваші активні записи"),
        BotCommand(command="/common_questions", description="Поширені питання")
    ]
    await bot.set_my_commands(commands=commands)


async def on_startup(self):
    await load_data()


async def on_shutdown(self):
    await upload_data()
    await delete_messages()


def register_all_middlewares(dp: Dispatcher):
    dp.setup_middleware(AccRest())


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(IsAdmin)


def register_all_handlers(dp: Dispatcher):
    register_start(dp)
    register_form_filling(dp)
    register_contacts(dp)
    register_records(dp)
    register_common_questions(dp)
    register_remove_data(dp)
    register_menu_price(dp)

    register_panel(dp)
    register_black_list(dp)
    register_act_on_users(dp)
    register_work_schedule(dp)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')

    bot = Bot(token=Config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    register_all_handlers(dp)

    loop = asyncio.get_event_loop()
    loop.create_task(set_bot_commands(bot))
    loop.create_task(record_monitor(True))

    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
