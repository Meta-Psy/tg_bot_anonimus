import telebot
from buttons import *
from database import *
bot = telebot.TeleBot(token="8284829962:AAEGchYMnm23mP9Tpxgyo1rFVOyclJTOi5o")

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.from_user.id
    if check_reg(message.from_user.id):
        name = check_reg(message.from_user.id)
        bot.send_message(chat_id, f'Добро пожаловать, {name[0][2]}')
        bot.register_next_step_handler(message, main_menu)
    else:
        bot.send_message(chat_id=message.from_user.id, text="Перед тем как начать,давайте познакомимся.Как вас зовут? ")
        bot.register_next_step_handler(message, save_name)
    
def save_name(message):
    chat_id = message.from_user.id
    name = message.text
    create_acc(message.from_user.id, name)
    bot.send_message(chat_id, 'Выберите Действие: ', reply_markup=main_menu_bt())

@bot.message_handler(content_types=['text'])
def main_menu(message):
    chat_id = message.from_user.id
    if message.text.lower() == 'создать свой опросник':
        bot.send_message(chat_id, 'Задайте Вопрос: ')
        bot.register_next_step_handler(message=message, callback=answers)
    elif message.text.lower() == 'выбрать опросник друга':
        pass

def answers(message):
    chat_id = message.from_user.id
    question = message.text
    bot.send_message(chat_id,"Ваш варианты ответа (напишите все через точку с запятой одним сообщением). Правильным будет первый вариант")
    bot.register_next_step_handler(message, get_answer, question)

def get_answer(message, question):
    chat_id = message.from_user.id
    answer = message.text
    user_id = get_user_info(tg_id=message.from_user.id)
    create_poll(question, answer, user_id)
    bot.send_message(chat_id, 'Продолжим?', reply_markup=choose_bt())
    bot.register_next_step_handler(message, choose)

    
def choose(message):
    chat_id = message.from_user.id
    if message.text == 'Завершить работу':
        bot.send_message(chat_id, "Ваш опросник успешно сохранен. Если будет желание, можете снова создать опросник или пройти его самому. Кнопки будут как всегда внизу.", reply_markup=main_menu_bt())
    elif message.text == 'Еще один опросник':
        bot.send_message(chat_id, 'Задайте Вопрос: ')
        bot.register_next_step_handler(message, answers)
bot.infinity_polling()