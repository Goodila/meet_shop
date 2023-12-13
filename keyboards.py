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
        i = i.split('/')[-1].split('.')[0]
        button = InlineKeyboardButton(text=i, callback_data=f'{i}')
        markup.add(button)
    button = InlineKeyboardButton(text="Назад", callback_data='start')
    markup.add(button)
    return markup


async def back_keyboard(start=False, text='Отменить регистрацию') -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=f'Назад', callback_data='menu'),
    ]
    if start:
        buttons = [
            InlineKeyboardButton(text=f'{text}', callback_data='start'),
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






