import telebot

def main_menu_bt():
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = telebot.types.KeyboardButton("Создать свой Опросник")
    bt2 = telebot.types.KeyboardButton("Выбрать Опросник друга")
    kb.row(bt1)
    kb.row(bt2)
    return kb

def choose_bt():
    kb = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt1 = telebot.types.KeyboardButton("Завершить работу")
    bt2 = telebot.types.KeyboardButton("Еще один опросник")
    kb.add(bt1, bt2)
    return kb