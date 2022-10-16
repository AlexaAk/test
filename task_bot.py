#!/usr/bin/python3
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from enum import Enum
import json
import os
import platform
if platform.system() == "Linux":
    os.chdir("/home/alexaak/python/Buh_bots/")
else:
    os.chdir("../../")
import keyboards as kb
import buh


class Stage(Enum):
    NONE = 0
    EMPLOYEE_NAME = 1
    TASK_NUM = 2
    PRICE = 3
    TASK_NAME = 4
    ALREADY_EXISTS = 5
    IF_EXISTS = 6
    PROJECT_NAME = 7
    # IS_PAID = 6
    TASK_LINK = 8
    PROJECT_LINK = 9


jsonConfig = open("config.json", "r", encoding="utf-8")
json_file = json.load(jsonConfig)

bot = Bot(token=json_file["token_task_bot"])
jsonConfig.close()

dp = Dispatcher(bot)
users = {}


class User:
    def __init__(self):
        # self.user_id = id
        self.task = buh.task()
        self.stage = Stage.NONE
        self.tasks_in_total = 0
        self.qur_task = 0


def create_user_session(message):
    user_id = message.chat.id
    users[user_id] = User()
    users[user_id].task = buh.task()
    users[user_id].stage = Stage.NONE

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    user_id = message.chat.id
    create_user_session(message)
    await bot.send_message(user_id,
                           "Здравствуйте, давайте соберем задание по переводу.\n\nВведите первую букву фамилии "
                           "сотрудника, которому необходимо отправить оплату, или нажмите на кнопку, чтобы "
                           "ввести данные о новом сотруднике", reply_markup=kb.inline_btn_empl)
    users[user_id].stage = Stage.EMPLOYEE_NAME


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    user_id = message.chat.id
    await bot.send_message(user_id, "Это бот для составления задач по переводу сотрудникам компании Эффективные сайты. "
                                    "Составьте сообщение по команде /start и перешлите его в чат с бухгалтером, нажав "
                                    "на кнопку после составления сообщения.")



@dp.message_handler()
async def stuff_by_letter(message: types.Message):
    if len(users) == 0:
        create_user_session(message)
    user_id = message.chat.id
    m_t = message.text
    if users[user_id].stage == Stage.NONE:
        await bot.send_message(user_id,
                               'Введите /start чтобы начать сставлять задание по переводу\nВведите /help для вывода '
                               'информации о боте')
    elif users[user_id].stage == Stage.EMPLOYEE_NAME:
        if len(message.text) != 1:
            await bot.send_message(user_id, 'Введите первую букву фамилии сотрудника, которому необходимо '
                                            'отправить оплату')
            return
        char = m_t
        list_c = []
        list_1 = []
        list_2 = []
        list_c.append(list_1)
        list_c.append(list_2)
        for i in range(len(buh.employee)):
            if len(buh.employee[i]) != 0:
                if buh.employee[i][0] == char.upper():
                    list_c[0].append(buh.employee[i])
                    list_c[1].append(i)
        if len(list_c[0]) == 0:
            await bot.send_message(user_id, 'Таких сотрудников нет')
        else:
            kb.clean_stuff_kb()
            kb.fill_stuff_kb(list_c)
            await bot.send_message(user_id, 'Выберите сотрудника: ', reply_markup=kb.stuff_kb_list[0])
    elif users[user_id].stage == Stage.TASK_NUM:
        if m_t.isdigit():
            users[user_id].task.set_task_num(int(m_t))
            users[user_id].tasks_in_total = m_t
            users[user_id].qur_task = 1
            users[user_id].stage = Stage.PRICE
            await bot.send_message(user_id, 'Введите сумму оплаты для задачи ' + str(users[user_id].qur_task))
        else:
            await bot.send_message(user_id, 'Некорректный ввод!\n\nВведите количество задач для данного '
                                            'сотрудника')
    elif users[user_id].stage == Stage.PRICE:
        if m_t.isdigit():
            users[user_id].task.set_price(int(m_t))
            users[user_id].stage = Stage.TASK_NAME
            await bot.send_message(user_id, 'Введите название задачи ' + str(users[user_id].qur_task))
        else:
            await bot.send_message(user_id,
                                   'Некорректный ввод!\n\nВведите сумму оплаты для задачи' + str(
                                       users[user_id].qur_task))
    elif users[user_id].stage == Stage.TASK_NAME:
        users[user_id].task.set_task_name(m_t)
        users[user_id].stage = Stage.ALREADY_EXISTS
        await bot.send_message(user_id, 'Перевод по данной задаче:', reply_markup=kb.inline_kb_exists)
    elif users[user_id].stage == Stage.ALREADY_EXISTS:
        await bot.send_message(user_id, 'Перевод по данной задаче:', reply_markup=kb.inline_kb_exists)

    elif users[user_id].stage == Stage.IF_EXISTS:
        if m_t.isdigit():
            users[user_id].task.set_if_exists_price(int(m_t))
            users[user_id].stage = Stage.PROJECT_NAME
            await bot.send_message(user_id, 'Введите название проекта ' + str(users[user_id].qur_task))
        else:
            await bot.send_message(user_id, 'Вы ввели не число!\nВведите полную сумму будущей оплаты: ')

    elif users[user_id].stage == Stage.PROJECT_NAME:
        users[user_id].task.set_project_name(m_t)
        # users[user_id].stage = Stage.IS_PAID
        # await bot.send_message(user_id,
        #                        'Оплачена ли клиентом эта задача?\n(Если не знаете, выбирайте вариант не оплачено)',
        #                        reply_markup=kb.inline_kb_payment)
        users[user_id].stage = Stage.TASK_LINK
        await bot.send_message(user_id, 'Введите ссылку на задачу. Если у вас нет ссылки, '
                                        'нажмите на кнопку', reply_markup=kb.inline_kb_links2)
    # elif users[user_id].stage == Stage.IS_PAID:
    #     await bot.send_message(user_id,
    #                            'Оплачена ли клиентом эта задача?\n(Если не знаете, выбирайте вариант не оплачено)',
    #                            reply_markup=kb.inline_kb_payment)
    elif users[user_id].stage == Stage.TASK_LINK:
        users[user_id].task.set_task_link(m_t)
        users[user_id].stage = Stage.PROJECT_LINK
        await bot.send_message(user_id, 'Введите ссылку на проект. Если у вас нет ссылки, '
                                        'нажмите на кнопку', reply_markup=kb.inline_kb_links1)
    elif users[user_id].stage == Stage.PROJECT_LINK:
        users[user_id].task.set_project_link(m_t)
        if int(users[user_id].qur_task) == int(users[user_id].tasks_in_total):
            await bot.send_message(user_id, 'Все поля заполнены, высылаю готовое сообщение...')
            await bot.send_message(user_id, users[user_id].task.compose_a_message(), reply_markup=kb.inline_kb_send_msg)
            users[user_id].stage = Stage.NONE
        else:
            users[user_id].stage = Stage.PRICE
            users[user_id].qur_task += 1
            await bot.send_message(user_id, 'Введите сумму оплаты для задачи ' + str(users[user_id].qur_task))
    else:
        print (users[user_id].stage)
        await bot.send_message(user_id,
                               'Введите /start чтобы начать сставлять задание по переводу\nВведите /help для вывода '
                               'информации о боте')

# buttons
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('b_s'))
async def process_callback_stuff_kb_list(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data[3:]
    if code.isdigit():
        code = int(code)
        users[user_id].task.set_employee_name(buh.employee[code])
        users[user_id].stage = Stage.TASK_NUM
        await bot.send_message(callback_query.from_user.id, 'Введите количество задач для данного сотрудника')
    else:
        print('ERROR 1')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('exists'))
async def process_callback_stuff_kb_list(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data
    if code == 'exists_new_full':
        users[user_id].task.set_already_exists(buh.Already_exists.NEW_FULL)
        users[user_id].task.set_skip_exists_price()
        users[user_id].stage = Stage.PROJECT_NAME
        await bot.send_message(callback_query.from_user.id, 'Введите название проекта ' + str(users[user_id].qur_task))
    elif code == 'exists_new_part':
        users[user_id].task.set_already_exists(buh.Already_exists.NEW_PARTIALLY)
        users[user_id].stage = Stage.IF_EXISTS
        await bot.send_message(callback_query.from_user.id, 'Введите полную сумму будущей оплаты: ')
    else:
        users[user_id].task.set_already_exists(buh.Already_exists.OLD_PARTIALLY)
        users[user_id].task.set_skip_exists_price()
        users[user_id].stage = Stage.PROJECT_NAME
        await bot.send_message(callback_query.from_user.id, 'Введите название проекта ' + str(users[user_id].qur_task))

    # if code.isdigit():
    #     code = int(code)
    #     users[user_id].task.set_employee_name(buh.employee[code])
    #     users[user_id].stage = Stage.TASK_NUM
    #     await bot.send_message(callback_query.from_user.id, 'Введите количество задач для данного сотрудника')
    # else:
    #     print('ERROR 1')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('b_p'))
async def process_callback_stuff_kb_list(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data
    if code == 'b_p_p':
        users[user_id].task.set_is_paid(buh.Payment.PAID)
    elif code == 'b_p_pp':
        users[user_id].task.set_is_paid(buh.Payment.PARTIALLY_PAID)
    else:
        users[user_id].task.set_is_paid(buh.Payment.UNPAID)
    users[user_id].stage = Stage.TASK_LINK
    await bot.send_message(callback_query.from_user.id, 'Введите ссылку на задачу. \nЕсли задачу нужно создать, '
                                                        'или она есть, но у вас нет ссылки, нажмите на кнопку.',
                           reply_markup=kb.inline_kb_links2)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('butt'))
async def process_callback_stuff_kb_list(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    code = callback_query.data
    if users[user_id].stage == Stage.TASK_LINK:
        if code == 'butt2':
            users[user_id].task.set_task_link('Добавить новую')
        else:
            users[user_id].task.set_task_link('нет ссылки')
        users[user_id].stage = Stage.PROJECT_LINK
        await bot.send_message(callback_query.from_user.id, 'Введите ссылку на проект. Если у вас нет ссылки, '
                                                            'нажмите на кнопку', reply_markup=kb.inline_kb_links1)
    else:
        users[user_id].task.set_project_link('нет ссылки')
        if int(users[user_id].qur_task) == int(users[user_id].tasks_in_total):
            await bot.send_message(callback_query.from_user.id, 'Все поля заполнены, высылаю готовое сообщение...')
            await bot.send_message(callback_query.from_user.id, users[user_id].task.compose_a_message(),
                                   reply_markup=kb.inline_kb_send_msg)
            users[user_id].stage = Stage.NONE
        else:
            users[user_id].stage = Stage.PRICE
            users[user_id].qur_task += 1
            await bot.send_message(callback_query.from_user.id,
                                   'Введите сумму оплаты для задачи ' + str(users[user_id].qur_task))


@dp.callback_query_handler(lambda c: c.data == 'bsend')
async def process_callback_button1(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.send_message(-761980818, users[user_id].task.message)


if __name__ == '__main__':
    executor.start_polling(dp)

# @dp.message_handler(commands=['start'])
# async def process_start_command(message: types.Message):
#     await message.reply("Привет!", reply_markup=kb.greet_kb)

# @dp.message_handler(commands=['1'])
# async def process_command_1(message: types.Message):
#     await message.reply("Первая инлайн кнопка", reply_markup=kb.inline_kb1)
#
# @dp.message_handler(commands=['2'])
# async def process_command_2(message: types.Message):
#     await message.reply("Отправляю все возможные кнопки", reply_markup=kb.inline_kb_full)

# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


# @dp.callback_query_handler(lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')
#
# @dp.callback_query_handler(lambda c: c.data == 'button2')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата вторая кнопка!')
