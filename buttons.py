import telebot

def main_menu_bt():
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = telebot.types.KeyboardButton("Создать свой Опросник")
    bt2 = telebot.types.KeyboardButton("Выбрать Опросник друга")
    bt3 = telebot.types.KeyboardButton("Добавить друга")
    bt4 = telebot.types.KeyboardButton("Узнать свой ID")
    kb.row(bt1)
    kb.row(bt2, bt3)
    kb.row(bt4)
    return kb

def choose_bt():
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = telebot.types.KeyboardButton("Завершить работу")
    bt2 = telebot.types.KeyboardButton("Еще один опросник")
    kb.add(bt1, bt2)
    return kb

def friends_bt(friends_with_names):
    kb = telebot.types.InlineKeyboardMarkup(row_width=2)
    buttons = [telebot.types.InlineKeyboardButton(text=f'{friend[1]} - {friend[0]}', callback_data=f'id_{friend[0]}') for friend in friends_with_names]
    kb.add(*buttons)
    return kb

