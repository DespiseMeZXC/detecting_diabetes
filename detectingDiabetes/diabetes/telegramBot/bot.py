import telebot
import pickle
import time
import numpy as np
from telebot import types

# pip install pytelegrambotapi
with open('Model_cnn', 'rb') as f2:  # читаем побайтово
    loaded_model = pickle.load(f2)  # с помощью load загружаем

bot = telebot.TeleBot('5299383555:AAGtLP9-5t270MPfn9pNTxIrKXVRGYp1s3w')

question = ["Количество беременностей", "Глюкозы в крови", "Давление крови",
            "Толщина кожи", "Инсулина в крови", "Индекс массы тела",
            "Функция родословного диабета", "Возвраст"]
answerOnTheQuestion = []

keyboard = types.InlineKeyboardMarkup()
callback_button1 = types.InlineKeyboardButton(text="Кто я?", callback_data="whoIAm")
callback_button2 = types.InlineKeyboardButton(text="Что такое диабет?", callback_data="whatIsDiabet")
callback_button3 = types.InlineKeyboardButton(text="Информация о разработчике", callback_data="infoAboutMe")
keyboard.add(callback_button1)
keyboard.add(callback_button2)
keyboard.add(callback_button3)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Определить диагноз")
btn2 = types.KeyboardButton("Вернуться к приветствию")
markup.add(btn1)
markup.add(btn2)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Спасибо посещение)"
                     .format(message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id, text="Здравствуй, пользователь!!! Что хотите узнать?"
                     .format(message.from_user), reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def func(message):
    a = True
    global answerOnTheQuestion
    if message.text == "Определить диагноз":
        bot.send_message(message.chat.id, text="Введите " + question[len(answerOnTheQuestion)])
    if message.text[0].isdigit() == True:
        pointCount = 0
        for i in range(len(message.text)):
            if message.text[i] == '.':
                pointCount = pointCount + 1
            if not (message.text[i].isdigit()) and not (message.text[i] == '.' and pointCount > 1):
                if message.text != "Определить диагноз" or len(answerOnTheQuestion) > 0:
                    answerOnTheQuestion = []
                    bot.send_message(message.chat.id, text="Вводите пожалуйтса только числа")
                    time.sleep(1)
                    num_of_secs = 3
                    while num_of_secs:
                        bot.send_message(message.chat.id,
                                         text="Время подумать над своим поведением: " + str(num_of_secs))
                        time.sleep(1)
                        num_of_secs -= 1
                    bot.send_message(message.chat.id, text="Введите " + question[len(answerOnTheQuestion)])
                    a = False
        if len(answerOnTheQuestion) == len(question):
            X_new = np.array([answerOnTheQuestion], dtype="float")
            answerOnTheQuestion = []
            pred = loaded_model.predict(X_new)
            result = pred[0]
            some = ""
            if result == 1:
                some = "Вероятен диабет"
            else:
                some = "Диабет маловероятен"
            time.sleep(1)
            num_of_secs = 3
            while num_of_secs:
                bot.send_message(message.chat.id,
                                 text="Тест пройдет, результат обрабатывается" + str(num_of_secs))
                time.sleep(0.5)
                num_of_secs -= 1
            bot.send_message(message.chat.id, text=some)

        if a == True and len(answerOnTheQuestion) != len(question):
            answerOnTheQuestion.append(float(message.text))
            if len(answerOnTheQuestion) == len(question):
                X_new = np.array([answerOnTheQuestion], dtype="float")
                answerOnTheQuestion = []
                pred = loaded_model.predict(X_new)
                result = pred[0]
                some = ""
                if result == 1:
                    some = "Вероятен диабет"
                else:
                    some = "Диабет маловероятен"
                time.sleep(1)
                num_of_secs = 3
                while num_of_secs:
                    bot.send_message(message.chat.id,
                                     text="Тест пройден, результат обрабатывается " + str(num_of_secs))
                    time.sleep(0.5)
                    num_of_secs -= 1
                bot.send_message(message.chat.id, text=some)
            else:
                bot.send_message(message.chat.id, text="Введите " + question[len(answerOnTheQuestion)])
                print(answerOnTheQuestion)


    elif message.text == "Вернуться к приветствию":
        bot.send_message(message.chat.id, text="Здравствуй, пользователь!!! Что хотите узнать?"
                         .format(message.from_user), reply_markup=markup and keyboard)
    elif (len(answerOnTheQuestion) != 0 or message.text != "Определить диагноз"):
        answerOnTheQuestion = []
        bot.send_message(message.chat.id, text="Вводите пожалуйтса только числа")
        time.sleep(1)
        num_of_secs = 3
        while num_of_secs:
            bot.send_message(message.chat.id,
                             text="Время подумать над своим поведением: " + str(num_of_secs))
            time.sleep(1)
            num_of_secs -= 1
        bot.send_message(message.chat.id, text="Введите " + question[len(answerOnTheQuestion)])
        a = False


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        some = call.message.text
        some1 = call.message.reply_markup
        if call.data == "whoIAm":
            num_of_secs = 6
            while num_of_secs:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Я бот определяющий по анализам начнётся \
                                 ли диабет у человека в течении 5 лет.\nВернётся автоматически через:" + str(
                                          num_of_secs))
                time.sleep(1)
                num_of_secs -= 1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=some,
                                  reply_markup=some1)
        if call.data == "whatIsDiabet":
            num_of_secs = 15
            while num_of_secs:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Диабет – это хроническое заболевание,\
                                 которое возникает либо в случаях, когда\
                                  поджелудочная железа не вырабатывает \
                                  достаточное количество инсулина, либо \
                                  когда организм не может эффективно \
                                  использовать вырабатываемый инсулин. \
                                  Инсулин – это гормон, регулирующий уровень \
                                  глюкозы в крови.\n Вернётся автоматически \через:" + str(num_of_secs))
                time.sleep(1)
                num_of_secs -= 1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=some,
                                  reply_markup=some1)
        if call.data == "infoAboutMe":
            num_of_secs = 8
            while num_of_secs:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Выполнил студент БГИТУ, учащийся в "
                                           "в группе ИВТ-301, Шитый Алексей Дмитриевич."
                                           " Номер зачётной книжки: 20-2.019.\nВернётся автоматически через:" + str(
                                          num_of_secs))
                time.sleep(1)
                num_of_secs -= 1
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=some,
                                  reply_markup=some1)


bot.polling()