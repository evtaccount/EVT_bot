import telebot
from telebot import types

import menus
import functions
import config
import os
from flask import Flask, request
import logging


bot = telebot.TeleBot(config.API_TOKEN_EVT)
filmRates = config.vote_films
knownUsers = []


# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)


    # Хэндлер обрабатывающий команды "/start и "/ask_bot""
    @bot.message_handler(commands=['start', 'ask_bot'])
    def send_welcome(message):
        known_users = functions.read_known_users()
        current_user = functions.take_user(message)

        if current_user not in known_users:
            functions.write_new_user(current_user)
            bot.send_message(message.chat.id,
                             "Привет, я бот клоповника \n Рекомендуем ознакомиться в нашими правилами /about",
                             reply_markup=keyboard_generator(menus.main_menu, True, True, 1))
        else:
            print('Есть в базе')
            bot.send_message(message.chat.id, "Мы уже знакомы ;-)",
                             reply_markup=keyboard_generator(menus.main_menu, True, True, 1))


    # Хэндлер показывающий список доступных комманд
    @bot.message_handler(commands=['help'])
    def command_help(message):
        help_text = "Доступны следующие команды: \n"
        for key in config.commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += config.commands[key] + "\n"
        bot.send_message(message.chat.id, help_text)  # send the generated help page


    # Хэндлер обеспечивающий быстрый доступ к списку правил
    @bot.message_handler(commands=['about'])
    def rules_klp(message):
        bot.send_message(message.chat.id, 'Тут будет список правил бункера')
        pass


    # ----------------------------------------- Начало блока менюшек -------------------------------------------------------


    @bot.message_handler(func=lambda message: True if message.text in menus.ivents['buttons'][:-1:] else False)
    def markup_ivents(message):
        if message.text == 'Ближайший ивент':
            pass

        elif message.text == 'День кино':
            print(functions.read_film_rates_with_id(0))
            bot.send_message(message.chat.id, 'Меню кино:',
                             reply_markup=keyboard_generator(menus.cinema, True, False, 1))

        elif message.text == '"Рисовач"':
            bot.send_message(message.chat.id, 'Рисовач:', reply_markup=keyboard_generator(menus.paint, True, True, 1))

        elif message.text == 'Каллиграфия':
            bot.send_message(message.chat.id, 'Киллиграфия:',
                             reply_markup=keyboard_generator(menus.kalli, True, True, 1))

        else:
            pass


    # Обработчик меню "День кино".
    # "Предложить фильм"
    # "Посмотреть результаты"
    # "Голосовать"
    # "История"
    @bot.message_handler(func=lambda message: True if message.text in menus.cinema['buttons'][:-1:] else False)
    def markup_cinema(message):
        filmRates = functions.read_film_rates_with_id(1)

        if message.text == 'Предложить фильм':
            pass

        elif message.text == 'Голосование':
            bot.send_message(message.chat.id, "Ваш выбор?", reply_markup=choose_film_markup(filmRates))

        elif message.text == 'История':
            pass

        else:
            markup_paint(message)


    # Обработчик меню "Рисовач"
    @bot.message_handler(func=lambda message: True if message.text in menus.paint['buttons'][:-1:] else False)
    def markup_paint(message):
        if message.text == 'О Рисоваче':
            pass

        else:
            markup_kalli(message)


    # Обработчик меню "Каллиграфия"
    @bot.message_handler(func=lambda message: True if message.text in menus.kalli['buttons'][:-1:] else False)
    def markup_kalli(message):
        if message.text == 'О Каллиграфии':
            pass

        elif message.text == 'Записаться на занятие':
            pass

        else:
            pass


    # Обработчик меню "Переголосовать"
    @bot.message_handler(func=lambda message: True if message.text in ['Переголосовать'] else False)
    def markup_crate(message):
        if message.text == 'Переголосовать':
            pass

        else:
            pass


    def keyboard_generator(markup_list, resize_keyboard, one_time_keyboard, row_width):
        btns_list = markup_list['buttons']
        markup_gen = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard,
                                               row_width=row_width)
        buttons = []
        for button in btns_list:
            buttons.append(types.KeyboardButton(button))
        markup_gen.add(*buttons)
        return markup_gen


    # Обработчик "Главного меню"
    @bot.message_handler(func=lambda message: True)
    def main_menu(message):
        if message.text == 'Правила':
            bot.send_message(message.chat.id, '''
            Наши правила довольно просты:
            1. 
            2. 
            3. 
            4. 
            5. 
            ''', reply_markup=keyboard_generator(menus.main_menu, True, True, 1))

        elif message.text == 'Ивенты':
            bot.send_message(message.chat.id, 'Ближайшие мероприятия:',
                             reply_markup=keyboard_generator(menus.ivents, True, True, 1))

        elif message.text == 'Музыка':
            pass

        elif message.text == 'Как добраться':
            pass

        elif message.text == 'Главное меню':
            bot.send_message(message.chat.id, "Главное меню",
                             reply_markup=keyboard_generator(menus.main_menu, True, True, 1))

        else:
            pass
            # markup_ivents(message)


    # --------------------------------------------- Кронец блока меню ------------------------------------------------------


    def choose_film_markup(button=config.vote_films):

        markup_choose_film = types.InlineKeyboardMarkup(row_width=1)
        btn_in_film1 = types.InlineKeyboardButton(text=(button[0]['film_name'] + ' - ' + str(button[0]['rate'])),
                                                  callback_data='film1')
        btn_in_film2 = types.InlineKeyboardButton(text=(button[1]['film_name'] + ' - ' + str(button[1]['rate'])),
                                                  callback_data='film2')
        btn_in_film3 = types.InlineKeyboardButton(text=(button[2]['film_name'] + ' - ' + str(button[2]['rate'])),
                                                  callback_data='film3')
        markup_choose_film.add(btn_in_film1, btn_in_film2, btn_in_film3)

        return markup_choose_film


    # Обработчик меню голосования за кино
    @bot.callback_query_handler(func=lambda c: c.data)
    def choose_film(c):
        film_rates = functions.read_film_rates_with_id(1)
        print(film_rates)
        print(c)

        if c.data == 'film1':
            # if c.data == 'film1' and c.from_user.id not in film_rates[1]['user_ids'] and c.from_user.id in film_rates[2]['user_ids']:
            if c.from_user.id not in film_rates[1]['user_ids'] and c.from_user.id not in film_rates[2]['user_ids']:
                if c.from_user.id in film_rates[0]['user_ids']:
                    film_rates[0]['user_ids'].remove(c.from_user.id)
                    film_rates[0]['rate'] -= 1
                    print(film_rates)
                else:
                    film_rates[0]['user_ids'].append(c.from_user.id)
                    film_rates[0]['rate'] += 1
                    print(film_rates)

        elif c.data == 'film2':
            # elif c.data == 'film2' and c.from_user.id not in film_rates[0]['user_ids'] and c.from_user.id in film_rates[2]['user_ids']:
            if c.from_user.id not in film_rates[0]['user_ids'] and c.from_user.id not in film_rates[2]['user_ids']:
                if c.from_user.id in film_rates[1]['user_ids']:
                    film_rates[1]['user_ids'].remove(c.from_user.id)
                    film_rates[1]['rate'] -= 1
                    print(film_rates)
                else:
                    film_rates[1]['user_ids'].append(c.from_user.id)
                    film_rates[1]['rate'] += 1
                    print(film_rates)

        elif c.data == 'film3':
            # elif c.data == 'film3' and c.from_user.id not in film_rates[0]['user_ids'] and c.from_user.id in film_rates[1]['user_ids']:
            if c.from_user.id not in film_rates[1]['user_ids'] and c.from_user.id not in film_rates[0]['user_ids']:
                if c.from_user.id in film_rates[2]['user_ids']:
                    film_rates[2]['user_ids'].remove(c.from_user.id)
                    film_rates[2]['rate'] -= 1
                    print(film_rates)
                else:
                    film_rates[2]['user_ids'].append(c.from_user.id)
                    film_rates[2]['rate'] += 1
                    print(film_rates)

        functions.write_film_rates_with_id(film_rates)

        try:
            bot.edit_message_text(chat_id=c.message.chat.id,
                                  text='Ваш выбор?',
                                  message_id=c.message.message_id,
                                  reply_markup=choose_film_markup(film_rates))
        except:
            pass
            # bot.send_message(c.from_user.id, 'Результаты голосования:', reply_markup=menus.markup_crate)
            # for key, film in enumerate(film_rates):
            #     key += 1
            #     bot.send_message(c.from_user.id, str(key) + '. ' + film['film'] + ' - ' + str(film['vote_film']))


    @server.route("/" + config.API_TOKEN_EVT, methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        try:
            bot.set_webhook(url='https://evt-bot.herokuapp.com/' + config.API_TOKEN_EVT)
        except:
            bot.set_webhook(url='https://evt-bot.herokuapp.com/')
        return "?", 200

    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)