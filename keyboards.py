from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#buttons
inline_btn_1 = InlineKeyboardButton('Без ссылки', callback_data='butt1')
inline_btn_2 = InlineKeyboardButton('Добавить задачу', callback_data='butt2')

inline_btn_exists_1 = InlineKeyboardButton('Это новый полный перевод', callback_data='exists_new_full')
inline_btn_exists_2 = InlineKeyboardButton('Это новый частичный перевод', callback_data='exists_new_part')
inline_btn_exists_3 = InlineKeyboardButton('Это дополнение к старому переводу', callback_data='exists_old_part')

inline_btn_empl = InlineKeyboardButton('Новый сотрудник', callback_data='new_employee')

inline_btn_p = InlineKeyboardButton('Оплачено', callback_data='b_p_p')
inline_btn_pp = InlineKeyboardButton('Частично оплачено', callback_data='b_p_pp')
inline_btn_up = InlineKeyboardButton('Не оплачено', callback_data='b_p_up')

inline_btn_send_msg = InlineKeyboardButton('Отправить в чат с Бухгалтером', callback_data='bsend')

#keyboards
inline_kb_exists = InlineKeyboardMarkup(row_width=2).add(inline_btn_exists_1)
inline_kb_exists.add(inline_btn_exists_2)
inline_kb_exists.add(inline_btn_exists_3)

inline_kb_payment = InlineKeyboardMarkup(row_width=2).add(inline_btn_p)
inline_kb_payment.add(inline_btn_pp)
inline_kb_payment.add(inline_btn_up)

inline_kb_links1 = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_links2 = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_links2.add(inline_btn_2)

inline_kb_empl = InlineKeyboardMarkup(row_width=2).add(inline_btn_empl)

inline_kb_send_msg = InlineKeyboardMarkup(row_width=2).add(inline_btn_send_msg)
stuff_kb_list = []

#functions
def fill_stuff_kb (stuff):
    stuff_kb = InlineKeyboardMarkup(row_width=2)
    for i in range (len(stuff[0])):
        stuff_kb.add(InlineKeyboardButton(stuff[0][i], callback_data='b_s' + str(stuff[1][i])))
        # print(buh.employee[stuff[1][i]] + '     ' + 'b_s' + str(stuff[1][i]))
    stuff_kb_list.append(stuff_kb)

def clean_stuff_kb ():
    stuff_kb_list.clear()




# greet_kb = ReplyKeyboardMarkup()
# inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
# inline_kb_full.add(inline_btn_2)

