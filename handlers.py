import os
from aiogram import types, Dispatcher, types
from keyboards import start_keyboard, menu_keyboard, back_keyboard, admin_keyboard, name_keyboard, content_keyboard
from aiogram.dispatcher import FSMContext
from states import Order, Change
from funcs import get_config, Client
from asyncio import sleep
# 6500743193:AAEv7C1MescqsmCa979OptxW3qOMPRs9i2s

async def start(message: types.Message):
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
    await start(message)


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
    await call.bot.send_photo(call.from_user.id, photo, caption=text, reply_markup=markup)


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


# async def order_name(call: types.CallbackQuery, state: FSMContext):
#     ''' обработка клавиатуры name '''
#     if isinstance(call, types.Message):
#         await state.update_data(name=call.text)
#         text = '''*Укажите номер телефона для связи*''' 
#         Client(call.from_user.id).record_stuff("name", f'{call.text}')
#         markup = await back_keyboard(start=True)
#         await call.bot.delete_message(call.chat.id, call.message_id)
#         await call.answer(text=text, reply_markup=markup)
#         await state.set_state(Order.Number.state)
#         await call.bot.delete_message(call.chat.id, call.message_id-1)
#         return
#     if call.data == 'name_да':
#         name = Client(call.from_user.id).get_stuff('name')
#         await state.update_data(name=name)
#         text = '''*Укажите номер телефона для связи*''' 
#     elif call.data == 'name_нет':
#         text = '*Укажите имя, на которое будет осуществлена доставка*' 
#         markup = await back_keyboard(start=True)
#         await call.bot.delete_message(call.message.chat.id, call.message.message_id)
#         await call.message.answer(text=text, reply_markup=markup)
#         return
#     elif call.data == 'start':
#         await state.finish()
#         await start(call)
#         return
#     else:
#         text = 'ЧТО ТО ПОШЛО НЕ ТАК'
#         await call.message.answer(text=text)
#         await start(call)
#         await state.finish()
#     markup = await back_keyboard(start=True)
#     await call.bot.delete_message(call.message.chat.id, call.message.message_id)
#     await call.message.answer(text=text, reply_markup=markup)


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

#     dp.register_message_handler(work_name, state=Work.Name)
#     dp.register_message_handler(work_age, state=Work.Age)
#     dp.register_message_handler(work_post, state=Work.Post)
#     dp.register_message_handler(work_why, state=Work.Why)
#     dp.register_message_handler(work_know_from, state=Work.Know_from)
#     dp.register_message_handler(work_resume, state=Work.Link_resume)
#     dp.register_message_handler(work_case, state=Work.Link_case)
#     dp.register_message_handler(work_load, state=Work.Load)
#         #Бартер
#     dp.register_message_handler(barter_name, state=Barter.Name)
#     dp.register_message_handler(barter_number, state=Barter.Number)
#     dp.register_message_handler(barter_link, state=Barter.Link)
#     dp.register_message_handler(barter_subs, state=Barter.Subs)
#     dp.register_message_handler(barter_city, state=Barter.City)
#         #Менеджер
#     dp.register_message_handler(manager_number, state=Manager.Number)
#     dp.register_message_handler(manager_name, state=Manager.Name)
#     dp.register_message_handler(manager_link, state=Manager.Link)
#     dp.register_message_handler(manager_q, state=Manager.Q)
#         #Сотрудничество
#     dp.register_message_handler(colab_name, state=Colab.Name)
#     dp.register_message_handler(colab_post, state=Colab.Post)
#     dp.register_message_handler(colab_company, state=Colab.Company)
#     dp.register_message_handler(colab_reason, state=Colab.Reason)
#     dp.register_message_handler(colab_number, state=Colab.Number)
#         #Instagram
#     dp.register_message_handler(inst_number, state=Instagram.Number)
#     dp.register_message_handler(inst_number_wait, state=Instagram.Wait)
#     dp.register_message_handler(inst_link, state=Instagram.Link)
#     dp.register_callback_query_handler(inst_topic_choose, state=Instagram.Topic, text_startswith='Topic')
#     dp.register_callback_query_handler(inst_topic_choose_2, state=Instagram.Topic, text_startswith='topic')
#     dp.register_message_handler(inst_topic_another, state=Instagram.Topic_another)
#     dp.register_message_handler(inst_subs, state=Instagram.Subs)
#     dp.register_message_handler(inst_descroption, state=Instagram.Description)
#     dp.register_message_handler(inst_city, state=Instagram.City)
#     dp.register_message_handler(inst_stories, state=Instagram.Stories)
#     dp.register_message_handler(inst_stories_scope, state=Instagram.Stories_scope)
#     dp.register_message_handler(inst_reels, state=Instagram.Reels)
#     dp.register_message_handler(inst_reels_scope, state=Instagram.Reels_scope)
#     dp.register_message_handler(inst_statistic, state=Instagram.Statistic)
#         #YouTube
#     dp.register_message_handler(yt_number, state=YT.Number)
#     dp.register_message_handler(yt_number_wait, state=YT.Wait)
#     dp.register_message_handler(yt_link, state=YT.Link)
#     dp.register_callback_query_handler(yt_topic_choose, state=YT.Topic, text_startswith='Topic')
#     dp.register_callback_query_handler(yt_topic_choose_2, state=YT.Topic, text_startswith='topic')
#     dp.register_message_handler(yt_topic_another, state=YT.Topic_another)
#     dp.register_message_handler(yt_subs, state=YT.Subs)
#     dp.register_message_handler(yt_descroption, state=YT.Description)
#     dp.register_message_handler(yt_country, state=YT.Country)
#     dp.register_message_handler(yt_shorts, state=YT.Shorts)
#     dp.register_message_handler(yt_shorts_views, state=YT.Shorts_views)
#     dp.register_message_handler(yt_video, state=YT.Video)
#     dp.register_message_handler(yt_video_views, state=YT.Video_views)
#     dp.register_message_handler(yt_statistic, state=YT.Statistic)
#         #VK
#     dp.register_message_handler(vk_number, state=VK.Number)
#     dp.register_message_handler(vk_number_wait, state=VK.Wait)
#     dp.register_message_handler(vk_link, state=VK.Link)
#     dp.register_callback_query_handler(vk_topic_choose, state=VK.Topic, text_startswith='Topic')
#     dp.register_callback_query_handler(vk_topic_choose_2, state=VK.Topic, text_startswith='topic')
#     dp.register_message_handler(vk_topic_another, state=VK.Topic_another)
#     dp.register_message_handler(vk_subs, state=VK.Subs)
#     dp.register_message_handler(vk_descroption, state=VK.Description)
#     dp.register_message_handler(vk_country, state=VK.Country)
#     dp.register_message_handler(vk_post, state=VK.Post)
#     dp.register_message_handler(vk_post_views, state=VK.Post_views)
#     dp.register_message_handler(vk_clip, state=VK.Clip)
#     dp.register_message_handler(vk_clip_views, state=VK.Clip_views)
#     dp.register_message_handler(vk_statistic, state=VK.Statistic)
#         #TG
#     dp.register_message_handler(tg_number, state=TG.Number)
#     dp.register_message_handler(tg_number_wait, state=TG.Wait)
#     dp.register_message_handler(tg_link, state=TG.Link)
#     dp.register_callback_query_handler(tg_topic_choose, state=TG.Topic, text_startswith='Topic')
#     dp.register_callback_query_handler(tg_topic_choose_2, state=TG.Topic, text_startswith='topic')
#     dp.register_message_handler(tg_topic_another, state=TG.Topic_another)
#     dp.register_message_handler(tg_subs, state=TG.Subs)
#     dp.register_message_handler(tg_post_view, state=TG.Post_views)
#     dp.register_message_handler(tg_post, state=TG.Post)
#     dp.register_message_handler(tg_country, state=TG.Country)
#     dp.register_message_handler(tg_description, state=TG.Description)
#     dp.register_message_handler(tg_statistic, state=TG.Statistic)
#         #Dzen
#     dp.register_message_handler(dz_number, state=DZ.Number)
#     dp.register_message_handler(dz_number_wait, state=DZ.Wait)
#     dp.register_message_handler(dz_link, state=DZ.Link)
#     dp.register_callback_query_handler(dz_topic_choose, state=DZ.Topic, text_startswith='Topic')
#     dp.register_callback_query_handler(dz_topic_choose_2, state=DZ.Topic, text_startswith='topic')
#     dp.register_message_handler(dz_topic_another, state=DZ.Topic_another)
#     dp.register_message_handler(dz_subs, state=DZ.Subs)
#     dp.register_message_handler(dz_post_view, state=DZ.Post_views)
#     dp.register_message_handler(dz_post, state=DZ.Post)
#     dp.register_message_handler(dz_description, state=DZ.Description)
#     dp.register_message_handler(dz_statistic, state=DZ.Statistic)
        #Контакты
    # dp.register_callback_query_handler(contacts, text_startswith='contacts')

