from aiogram.dispatcher.filters.state import StatesGroup, State


class ProvideContacts(StatesGroup):
    Number = State()
    Name = State()


class FindData(StatesGroup):
    UserId = State()
