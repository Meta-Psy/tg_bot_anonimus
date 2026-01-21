import telebot
from buttons import *
from database import *
bot = telebot.TeleBot(token="8284829962:AAEGchYMnm23mP9Tpxgyo1rFVOyclJTOi5o")

@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.from_user.id
    if check_reg(message.from_user.id):
        name = check_reg(message.from_user.id)
        bot.send_message(chat_id, f'Добро пожаловать, {name[0][2]}', reply_markup=main_menu_bt())
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
        user_id = get_user_id(message.from_user.id)
        friends = get_friends(user_id)
        friends_with_names = get_names_for_ids(friends)
        bot.send_message(chat_id, "Выбери своего друга, которому ты бы хотел отправить опросник", reply_markup=friends_bt(friends_with_names))
    elif message.text.lower() == 'добавить друга':
        bot.send_message(chat_id, "Отправь ID своего друга. Он может узнать это через кнопку 'Узнать свой ID")
        bot.register_next_step_handler(message=message, callback=add_friend)
    elif message.text.lower() == 'узнать свой id':
        bot.send_message(chat_id, f"Ваш ID: {message.from_user.id}", reply_markup=main_menu_bt())
    

def answers(message):
    chat_id = message.from_user.id
    question = message.text
    bot.send_message(chat_id,"Ваш варианты ответа (напишите все через точку с запятой одним сообщением). Правильным будет первый вариант")
    bot.register_next_step_handler(message, get_answer, question)

def get_answer(message, question):
    chat_id = message.from_user.id
    answer = message.text
    user_id = get_user_id(tg_id=message.from_user.id)
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
        
def add_friend(message):
    chat_id = message.from_user.id
    try:
        friend_tg_id = int(message.text)
    except ValueError:
        bot.send_message(chat_id, "Некорректный ID. Введите число.", reply_markup=main_menu_bt())
        return
    user1_id = get_user_id(message.from_user.id)
    user2_id = get_user_id(friend_tg_id)
    if user2_id is None:
        bot.send_message(chat_id, "Пользователь с таким ID не найден", reply_markup=main_menu_bt())
        return
    matching_db(user1_id=user1_id, user2_id=user2_id)
    bot.send_message(chat_id, "Успешно добавлено", reply_markup=main_menu_bt())


bot.infinity_polling()