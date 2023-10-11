from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from tg_bot.config import Config


class IsAdmin(BoundFilter):
    async def check(self, target: types.Message | types.CallbackQuery) -> bool:
        return target.from_user.id in Config.ADMINS
