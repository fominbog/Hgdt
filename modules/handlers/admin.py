
from datetime import timedelta
from aiogram import types
from main import dp
import datetime
from modules import sqLite
from modules.keyboards import confirm_kb, back_kb, admin_kb, admin_client_kb, admin_driver_kb, admin_ban_kb
from modules.dispatcher import bot, admin_Form


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_first_menu, text='drivers')
async def start_menu(call: types.CallbackQuery):
    sqLite.insert_info(table='admin', name='data', data='drivers', telegram_id=call.from_user.id)
    await call.message.edit_text('Здесь вы можите отправить сообщение всем ВОДИТЕЛЯМ\n'
                                 'Введите текст сообщения', reply_markup=back_kb)
    await admin_Form.admin_send_msg.set()


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_first_menu, text='clients')
async def start_menu(call: types.CallbackQuery):
    sqLite.insert_info(table='admin', name='data', data='client', telegram_id=call.from_user.id)
    await call.message.edit_text('Здесь вы можите отправить сообщение всем КЛИЕНТАМ\n'
                                 'Введите текст сообщения', reply_markup=back_kb)
    await admin_Form.admin_send_msg.set()


# Admin menu
@dp.message_handler(state=admin_Form.admin_send_msg)
async def add_person_start(message: types.Message):
    await message.answer(text="Вот ваше сообщение. Отправить?")
    await message.answer(text=message.text, reply_markup=confirm_kb)
    sqLite.insert_info(table='admin', name=f'data2', data=message.text, telegram_id=message.from_user.id)
    await admin_Form.admin_send_msg_confirm.set()


# Menu investor send msg
@dp.callback_query_handler(state=admin_Form.admin_send_msg_confirm, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    admin_data = sqLite.read_all_value_bu_name(table='admin', name='*')[0]
    table = admin_data[5]
    users_data = sqLite.read_all_value_bu_name(table=f'{table}', name='*')
    for i in users_data:
        try:
            await bot.send_message(chat_id=i[1], text=admin_data[6])
        except:
            print('Error')
    await call.message.answer('Ваше сообщение отправлено')
    await call.message.answer('Привет администратор. Чем тебе помочь', reply_markup=admin_kb)
    await admin_Form.admin_first_menu.set()


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_users, text='back')
@dp.callback_query_handler(state=admin_Form.admin_first_menu, text='find_user')
async def start_menu(call: types.CallbackQuery):
    await call.message.answer('Введите телефонный номер без пробелов и без знака +')
    await admin_Form.admin_black_list_phone.set()


# Admin menu
@dp.message_handler(state=admin_Form.admin_black_list_phone)
async def start_menu(message: types.Message):
    all_data_client = sqLite.read_all_value_bu_name(name='*', table='client')
    all_data_driver = sqLite.read_all_value_bu_name(name='*', table='drivers')
    num = 0
    for i in all_data_client:
        if i is None:
            pass
        else:
            try:
                if message.text in i[3]:
                    num = i[1]
                    sqLite.insert_info(table='admin', name='data', data=i[1], telegram_id=message.from_user.id)
                else:
                    pass
            except:
                pass
    for i in all_data_driver:
        if i is None:
            pass
        else:
            try:
                if message.text in i[3]:
                    num = i[1]
                    sqLite.insert_info(table='admin', name='data', data=i[1], telegram_id=message.from_user.id)
                else:
                    pass
            except:
                pass
    if num == 0:
        await message.answer(f'Таких людей нет')
    else:
        data = sqLite.read_all_values_in_db(table='client', telegram_id=num)
        data2 = sqLite.read_all_values_in_db(table='drivers', telegram_id=num)
        if data is None:
            pass
        else:
            await message.answer(f'Тип аккаунта <b>КЛИЕНТ</b>\n'
                                 f'Нашел пользователя <b>{data[2]}</b>,\n'
                                 f'Телефон <b>{data[3]}</b>,\n'
                                 f'Рейтинг <b>{data[4]}</b>,\n'
                                 f'Статус (блокировка до) <b>{data[5]}</b>,\n', parse_mode='html',
                                 reply_markup=admin_client_kb)
            await admin_Form.admin_users.set()
        if data2 is None:
            pass
        else:
            await message.answer(f'Тип аккаунта <b>ВОДИТЕЛЬ</b>\n'
                                 f'Нашел пользователя <b>{data2[2]}</b>,\n'
                                 f'Телефон <b>{data2[3]}</b>,\n'
                                 f'Автомобиль <b>{data2[4]}</b>,\n'
                                 f'Номер автомобиля <b>{data2[5]}</b>,\n'
                                 f'Рейтинг <b>{data2[6]}</b>,\n'
                                 f'Статус (блокировка до) <b>{data2[16]}</b>,\n'
                                 f'Тариф оплачен до <b>{data2[9]}</b>,\n', parse_mode='html',
                                 reply_markup=admin_driver_kb)
            await admin_Form.admin_users.set()


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_users)
async def start_menu(call: types.CallbackQuery):
    if str(call.data) == 'ban_client':
        sqLite.insert_info(table='admin', name='data2', data='drivers', telegram_id=call.from_user.id)
        await call.message.answer('Здесь вы можите забанить и разбанить пользователя.', reply_markup=admin_ban_kb)
        await admin_Form.admin_ban.set()
    elif str(call.data) == 'ban_client_c':
        sqLite.insert_info(table='admin', name='data2', data='client', telegram_id=call.from_user.id)
        await call.message.answer('Здесь вы можите забанить и разбанить пользователя.', reply_markup=admin_ban_kb)
        await admin_Form.admin_ban.set()

    elif str(call.data) == 'send_msg':
        await call.message.answer('Здесь вы можите отправить сообщение пользователю.\n'
                                  'Введите текст сообщения', reply_markup=back_kb)
        await admin_Form.admin_send_msg_one.set()
    elif str(call.data) == 'ban_client_c':
        await call.message.answer('Здесь вы можите отправить сообщение пользователю.\n'
                                  'Введите текст сообщения', reply_markup=back_kb)
        await admin_Form.admin_send_msg_one.set()

    elif str(call.data) == 'pay_time':
        await call.message.answer('Введите количество оплаченых дней', reply_markup=back_kb)
        await admin_Form.admin_set_pay.set()
    else:
        pass


# Admin menu
@dp.message_handler(state=admin_Form.admin_send_msg_one)
async def add_person_start(message: types.Message):
    await message.answer(text="Вот ваше сообщение. Отправить?")
    await message.answer(text=message.text, reply_markup=confirm_kb)
    sqLite.insert_info(table='admin', name=f'data2', data=message.text, telegram_id=message.from_user.id)
    await admin_Form.admin_send_msg_one_confirm.set()


# Menu investor send msg
@dp.callback_query_handler(state=admin_Form.admin_send_msg_one_confirm, text='yes_all_good')
async def add_person_start(call: types.CallbackQuery):
    user_id = sqLite.read_all_value_bu_name(table='admin', name='*')[0][5]
    text = sqLite.read_all_value_bu_name(table='admin', name='*')[0][6]
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except:
        print('Error')
    await call.message.answer('Ваше сообщение отправлено')
    await call.message.answer('Привет администратор. Чем тебе помочь', reply_markup=admin_kb)
    await admin_Form.admin_first_menu.set()


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_ban)
async def start_menu(call: types.CallbackQuery):
    if str(call.data) == 'ban_min':
        await call.message.edit_text(
            'Введите целлое число МИНУТ на которое будет забанен пользователь начиная с данного '
            'момента')
        sqLite.insert_info(table='admin', name='data3', data='минут', telegram_id=call.from_user.id)
    elif str(call.data) == 'ban_hours':
        await call.message.edit_text(
            'Введите целлое число ЧАСОВ на которое будет забанен пользователь начиная с данного '
            'момента')
        sqLite.insert_info(table='admin', name='data3', data='часов', telegram_id=call.from_user.id)
    elif str(call.data) == 'ban_days':
        await call.message.edit_text(
            'Введите целлое число ДНЕЙ на которое будет забанен пользователь начиная с данного '
            'момента')
        sqLite.insert_info(table='admin', name='data3', data='дней', telegram_id=call.from_user.id)
    elif str(call.data) == 'unban':
        await call.message.edit_text(
            'Вы уверены что хотите разбанить пользователя?', reply_markup=confirm_kb)
    await admin_Form.admin_ban_time.set()


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_ban_time, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    user_id = sqLite.read_all_values_in_db(table='admin', telegram_id=call.from_user.id)[5]
    table = sqLite.read_all_values_in_db(table='admin', telegram_id=call.from_user.id)[6]
    sqLite.insert_info(table=table, name='status', data='active', telegram_id=int(user_id))
    await call.message.answer("Пользователь разбанен")
    await call.message.answer('Привет администратор. Чем тебе помочь', reply_markup=admin_kb)
    await admin_Form.admin_first_menu.set()


# Admin menu
@dp.message_handler(state=admin_Form.admin_ban_time)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        sqLite.insert_info(table='admin', name='data4', data=message.text, telegram_id=message.from_user.id)
        b_time = sqLite.read_all_values_in_db(table='admin', telegram_id=message.from_user.id)[7]
        await message.answer(f'Вы хотите забанить пользователя на <b>{message.text} {b_time}</b>?', parse_mode='html',
                             reply_markup=confirm_kb)
        await admin_Form.admin_ban_time_confirm.set()
    else:
        await message.answer('Введите только цифры')


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_ban_time_confirm, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    user_id = sqLite.read_all_values_in_db(table='admin', telegram_id=call.from_user.id)[5]
    table = sqLite.read_all_values_in_db(table='admin', telegram_id=call.from_user.id)[6]
    time_ban = sqLite.read_all_values_in_db(table='admin', telegram_id=call.from_user.id)[7]
    time_ban_number = sqLite.read_all_values_in_db(table='admin', telegram_id=call.from_user.id)[8]
    now = datetime.datetime.now()
    ban_date = ' '
    if str(time_ban) == 'минут':
        ban_date = now + timedelta(minutes=int(time_ban_number))
    elif str(time_ban) == 'часов':
        ban_date = now + timedelta(hours=int(time_ban_number))
    elif str(time_ban) == 'дней':
        ban_date = now + timedelta(days=int(time_ban_number))
    sqLite.insert_info(table=table, name='status', data=str(ban_date), telegram_id=int(user_id))
    await call.message.answer("Пользователь разбанен")
    await call.message.answer('Привет администратор. Чем тебе помочь', reply_markup=admin_kb)
    await admin_Form.admin_first_menu.set()


# Admin menu
@dp.message_handler(state=admin_Form.admin_set_pay)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        sqLite.insert_info(table='admin', name='data3', data=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Вы хотите дать платный период на {message.text} дней?', reply_markup=confirm_kb)
        await admin_Form.admin_set_confirm.set()
    else:
        await message.answer('Введите только цифры')


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_set_confirm, text='yes_all_good')
async def start_menu(call: types.CallbackQuery):
    user_id = sqLite.read_all_values_in_db(table='admin', telegram_id=call.from_user.id)[5]
    pay_time = sqLite.read_all_values_in_db(table='admin', telegram_id=call.from_user.id)[7]
    now = datetime.datetime.now()
    ban_date = now + timedelta(days=int(pay_time))
    sqLite.insert_info(table='drivers', name='pay_line', data=str(ban_date).split(' ')[0], telegram_id=int(user_id))
    await call.message.answer('Оплаченный период заданн')
    await call.message.answer('Привет администратор. Чем тебе помочь', reply_markup=admin_kb)
    await admin_Form.admin_first_menu.set()


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_first_menu, text='dilay_time')
async def start_menu(call: types.CallbackQuery):
    time_delta = sqLite.read_all_value_bu_name(name='time_delta', table='admin')[0][0]
    await call.message.edit_text(f'Введите длительность задержки в часах\n'
                                 f'В данный момент задержка равна  <b>{time_delta}</b>\n'
                                 f'Только целые числа', parse_mode='html', reply_markup=back_kb)
    await admin_Form.dilay_time.set()


# Admin menu
@dp.message_handler(state=admin_Form.dilay_time)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        sqLite.insert_info(table='admin', name='time_delta', data=message.text, telegram_id=message.from_user.id)
        await message.answer(f'Установлена задержка <b>{message.text}</b>', parse_mode='html')
        await message.answer('Привет администратор. Чем тебе помочь', reply_markup=admin_kb)
        await admin_Form.admin_first_menu.set()
    else:
        await message.answer("Введите только число")


# Admin menu
@dp.callback_query_handler(state=admin_Form.admin_first_menu, text='pay_mod')
async def start_menu(call: types.CallbackQuery):
    await call.message.edit_text(f'Для установки платного режима отправьте <b>1</b>\n'
                                 f'Для отключения платного режима отправьте <b>0</b>',
                                 parse_mode='html', reply_markup=back_kb)
    await admin_Form.admin_pay_mod.set()


# Admin menu
@dp.message_handler(state=admin_Form.admin_pay_mod)
async def start_menu(message: types.Message):
    if message.text.isdigit():
        sqLite.insert_info(table='admin', name='pay_mod', data=message.text, telegram_id=message.from_user.id)
        if '1' in message.text:
            await message.answer(f'Платный мод <b>ВКЛЮЧЕН</b>', parse_mode='html')
        else:
            await message.answer(f'Платный мод <b>ОТКЛЮЧЕН</b>', parse_mode='html')
        await message.answer('Привет администратор. Чем тебе помочь', reply_markup=admin_kb)
        await admin_Form.admin_first_menu.set()
    else:
        await message.answer("Введите только число")
