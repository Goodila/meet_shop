from aiogram.dispatcher.filters.state import StatesGroup, State


class Order(StatesGroup):
    Name = State()
    Number = State()
    Address= State()
    Products = State()
    Time = State()


class Change(StatesGroup):
    Photo = State()
    Photo_download = State()
    Text = State()
    Text_download = State()
