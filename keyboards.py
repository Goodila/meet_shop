from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from glob import glob
# EventsCallback = CallbackData('event', 'action', 'id')


async def start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Ассортимент', callback_data='menu'),
        InlineKeyboardButton(text='Заказать доставку', callback_data='delivery'),
        InlineKeyboardButton(text='Контакты', callback_data='contacts')
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def menu_keyboard(lst) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    for i in lst:
        button = InlineKeyboardButton(text=i, callback_data=f'{i}')
        markup.add(button)
    button = InlineKeyboardButton(text="Назад", callback_data='back_start')
    markup.add(button)
    return markup


async def content_keyboard(string) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    s = 'photo' if string is 'jpg' else 'menu'
    lst = glob(f'content/{s}/*.{string}')
    print(lst)
    for i in lst:
        i = i.split('\\')[-1].split('.')[0]
        print(i)
        button = InlineKeyboardButton(text=i, callback_data=f'{i}')
        markup.add(button)
    button = InlineKeyboardButton(text="Назад", callback_data='start')
    markup.add(button)
    return markup


async def back_keyboard(start=False) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=f'Назад', callback_data='menu'),
    ]
    if start:
        buttons = [
            InlineKeyboardButton(text=f'Отменить регистрацию', callback_data='start'),
        ]

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Изменить фото', callback_data='change_photo'),
        InlineKeyboardButton(text='Изменить ассортимент', callback_data='change_menu'),
        InlineKeyboardButton(text='Назад', callback_data='start')
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def name_keyboard(string) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=f'Да✅', callback_data=f'{string}_да'),
        InlineKeyboardButton(text='нет, ввести другой', callback_data=f'{string}_нет')
    ]
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*buttons)
    return markup


#ARCHIVE
async def colab_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Бартер', callback_data='barter'),
        InlineKeyboardButton(text='Я мнеджер блогеров, хочу сотрудничать с ЕРА', callback_data='manager'),
        InlineKeyboardButton(text='Сотрудничетсво с ЕРА', callback_data='colab_start'),
        InlineKeyboardButton(text='Назад', callback_data='start')
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def manager_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text='Да✅'),
        KeyboardButton(text='Нет❌')
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*buttons)
    return markup


async def bloger_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Instagram', callback_data='Instagram'),
        InlineKeyboardButton(text='YouTube', callback_data='YT'),
        InlineKeyboardButton(text='VK', callback_data='VK'),
        InlineKeyboardButton(text='Telegram', callback_data='TG'),
        InlineKeyboardButton(text='Дзен', callback_data='Дзен'),
        InlineKeyboardButton(text='Назад', callback_data='start')
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup






async def topic_keyboard_2() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Выбрать еще категорию', callback_data='topic_start'),
        InlineKeyboardButton(text='✅Закончить выбор', callback_data='topic_end'),
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup




