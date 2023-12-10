import os
from aiogram import types, Dispatcher, types
from keyboards import start_keyboard, menu_keyboard, back_keyboard, admin_keyboard, name_keyboard, content_keyboard
from aiogram.dispatcher import FSMContext
from states import Order, Change
from funcs import get_config, Client
from asyncio import sleep
# 6500743193:AAEv7C1MescqsmCa979OptxW3qOMPRs9i2s

async def start(message: types.Message, state: FSMContext=None):
    if state:
        await state.finish()
    with open('content/menu/время доставки.txt', 'r', encoding='utf-8') as f:
        time = f.read()
    text = f'''
Приветствую! На связи бот магазина Мясницкий Ряд (Путилково) ✌🏻

С моей помощью Вы можете: 
✏️ Ознакомиться с ассортиментом товара
✏️ Оформить заказ с доставкой

{time}

Приятного аппетита!

'''
    markup = await start_keyboard()
    photo = types.InputFile('content/photo/приветствие.jpg')
    await message.bot.send_photo(message.from_user.id, photo, caption=text, reply_markup=markup)
    

async def back_start(message: types.Message):
    ''' старт после отмены регистрации'''
    await message.bot.delete_message(message.message.chat.id, message.message.message_id)
    await start(message)


async def admin(message: types.Message, state: FSMContext):
    admins = get_config().admins
    if str(message.chat.id) in admins:
        markup = await admin_keyboard()
        await message.answer('Вы админ', reply_markup=markup)


async def contacts(message: types.Message):
    markup = await back_keyboard(start=True, text='Назад')
    text = """Для связи с нами:
Татьяна: (TG, WhatsApp) +7 966 072 7281 
Андрей: (TG, WhatsApp) +7 963 643-39-48 """
    await message.message.answer(text=text, reply_markup=markup)


async def change_photo(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Change.Photo.state)
    markup = await content_keyboard('jpg')
    await call.message.answer('Выберите фото, которое хотите изменить', reply_markup=markup)


async def change_photo_2(call: types.CallbackQuery, state: FSMContext):
    markup = await back_keyboard(start=True)
    await state.update_data(file=call.data)
    await call.message.answer('Пришлите новое фото', reply_markup=markup)
    await state.set_state(Change.Photo_download.state)


async def change_photo_3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file = data['file']
    await message.photo[-1].download(f'content/photo/{file}.jpg')
    await message.answer('фото заменено')
    await state.finish()
    await start(message, state=state)


async def change_menu(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Change.Text.state)
    markup = await content_keyboard('txt')
    await call.message.answer('Выберите текст, который хотите изменить', reply_markup=markup)


async def change_text_2(call: types.CallbackQuery, state: FSMContext):
    markup = await back_keyboard(start=True)
    await state.update_data(file=call.data)
    await call.message.answer('Пришлите новый текст', reply_markup=markup)
    await state.set_state(Change.Text_download.state)


async def change_text_3(message: types.Message, state: FSMContext):
    data = await state.get_data()
    file = data['file']
    with open(f"content/menu/{file}.txt", "w", encoding='utf-8') as f:
        f.write(f"{message.text}")
    await message.answer('текст заменен')
    await state.finish()
    await start(message)


async def menu(message: types.Message):
    ''' старт меню '''
    await message.bot.delete_message(message.message.chat.id, message.message.message_id)
    with open('content/menu/меню.txt', 'r', encoding='utf-8') as f:
        menu = f.read()
        lst = menu.split('\n')
        markup = await menu_keyboard(lst)
        photo = types.InputFile('content/photo/меню.jpg')
        text = '''В этом разделе Вы ожете ознакомиться с продукцией, и ценами на нее'''
        await message.bot.send_photo(message.from_user.id, photo, caption=text, reply_markup=markup)


async def categories(call: types.CallbackQuery):
    ''' выбор любой категории '''
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    with open('content/menu/меню.txt', 'r', encoding='utf-8') as f:
        menu = f.read()
        lst = menu.split('\n')
    if call.data in lst:
        with open(f'content/menu/{call.data}.txt', 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = 'не найдена категория((('
    photo = types.InputFile(f'content/photo/{call.data}.jpg')
    markup = await back_keyboard()
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    try:
        await call.bot.send_photo(call.from_user.id, photo, caption=text, reply_markup=markup)
    except:
        photo = types.InputFile(f'content/photo/{call.data}.jpg')
        await call.bot.send_photo(call.from_user.id, photo, caption='')
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        await call.bot.send_message(call.from_user.id, text=text, reply_markup=markup)


async def start_delivery(call: types.CallbackQuery, state: FSMContext):
    ''' старт опроса по доставке'''
    await state.set_state(Order.Name.state)
    id=str(call.from_user.id)
    await state.update_data(id=id)
    await state.update_data(username=call.from_user.username)
    text = '''Для оставления заказа ответьте на следующие вопросы:\n
*Укажите имя, на которое будет осуществлена доставка*'''
    markup = await back_keyboard(start=True)
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(text=text, reply_markup=markup)
    await state.set_state(Order.Name.state)
#     if Client(id).check():
#         name = Client(id).get_stuff('name')
#         text = f'''Заказ на имя - {name}?'''
#         markup = await name_keyboard('name')
#         await call.message.answer(text=text, reply_markup=markup)
#         await call.bot.delete_message(call.message.chat.id, call.message.message_id)
#         return
#     else:
#         Client(id).record({})
#         text = '''Для оставления заказа ответьте на следующие вопросы:\n
#         *Укажите имя, на которое будет осуществлена доставка*'''
#         markup = await back_keyboard(start=True)
#         await call.bot.delete_message(call.message.chat.id, call.message.message_id)
#         await call.message.answer(text=text, reply_markup=markup)


async def order_name(call: types.CallbackQuery, state: FSMContext):
    ''' обработка клавиатуры name '''
    await state.update_data(name=call.text)
    text = '''Укажите номер для связи'''
    markup = await back_keyboard(start=True)
    await call.answer(text, reply_markup=markup)
    await state.set_state(Order.Number.state)


async def order_number(call: types.CallbackQuery, state: FSMContext):
    ''' запоминает номер, спрашивает адрес '''
    await state.update_data(number=call.text)
    text = '''Укажите адрес для доставки
    (Улица, дом, корпус, подъезд, этаж, квартира)'''
    await state.set_state(Order.Address.state)
    markup = await back_keyboard(start=True)
    await call.answer(text, reply_markup=markup)


async def order_address(call: types.CallbackQuery, state: FSMContext):
    ''' запоминает address, спрашивает продукты '''
    await state.update_data(address=call.text)
    text = '''Укажите продукты, которые хотите заказать одним сообщением.
    не забудьте указать количество вес в граммах.'''
    await state.set_state(Order.Products.state)
    markup = await back_keyboard(start=True)
    await call.answer(text, reply_markup=markup)


async def order_products(call: types.CallbackQuery, state: FSMContext):
    ''' запоминает products, спрашивает время '''
    await state.update_data(products=call.text)
    with open('content/menu/время доставки.txt', 'r', encoding='utf-8') as f:
        time = f.read()
    text = f'''Укажите дату и время доставки.\n{time}'''
    await state.set_state(Order.Time.state)
    markup = await back_keyboard(start=True)
    await call.answer(text, reply_markup=markup)


async def order_time(call: types.CallbackQuery, state: FSMContext):
    ''' запоминает time, посылает заказ '''
    await state.update_data(time=call.text)
    text = f'''Заказ отправлен менеджеру. Спсибо за заказ. С Вами свяжуться в ближайшее время.'''
    await call.answer(text)
    order = await state.get_data()
    order_text = f'''Поступил заказ!
@{order['username']} {order['name']}
{order['number']}
{order['address']}
{order['products']}
{order['time']}'''
    admins = get_config().admins
    for i in admins:
        await call.bot.send_message(int(i), order_text)
    await sleep(4)
    await state.finish()
    await start(call)


#РЕГИСТРАЦИЯ ХЕНДЛЕРОВ
def registration_handlers(dp: Dispatcher):
    #Commands
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(admin, commands=['admin'])

    #Callbacks
    dp.register_callback_query_handler(menu, text='menu')
    dp.register_callback_query_handler(start, text='start')
    dp.register_callback_query_handler(start, state='*', text='start')
    dp.register_callback_query_handler(back_start, text='back_start')
    dp.register_callback_query_handler(start_delivery, text='delivery')
    dp.register_callback_query_handler(change_photo, text='change_photo')
    dp.register_callback_query_handler(change_menu, text='change_menu')
    dp.register_callback_query_handler(contacts, text='contacts')
    dp.register_callback_query_handler(categories)
#     #States
        #Name
    dp.register_callback_query_handler(order_name, state=Order.Name)
    dp.register_message_handler(order_name, state=Order.Name)
    dp.register_message_handler(order_number, state=Order.Number)
    dp.register_message_handler(order_address, state=Order.Address)
    dp.register_message_handler(order_products, state=Order.Products)
    dp.register_message_handler(order_time, state=Order.Time)
        #Admin
    dp.register_callback_query_handler(change_photo_2, state=Change.Photo)
    dp.register_message_handler(change_photo_3, content_types='photo' ,state=Change.Photo_download)
    dp.register_callback_query_handler(change_text_2, state=Change.Text)
    dp.register_message_handler(change_text_3, state=Change.Text_download)
