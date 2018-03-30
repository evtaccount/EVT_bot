import telebot
from telebot import types

import menus
import functions
import config
import time
import sys


bot = telebot.TeleBot(config.API_TOKEN_EVT)
filmRates = config.vote_films
knownUsers = []


# # error handling if user isn't known yet
# # (obsolete once known users are saved to file, because all users
# #   had to use the /start command and are therefore known to the bot)
# def get_user_step(uid):
#     if uid in userStep:
#         return userStep[uid]
#     else:
#         knownUsers.append(uid)
#         userStep[uid] = 0
#         print "New user detected, who hasn't used \"/start\" yet"
#         return 0


# Хэндлер обрабатывающий команды "/start и "/ask_bot""
@bot.message_handler(commands=['start', 'ask_bot'])
def send_welcome(message):
    known_users = functions.read_known_users()
    current_user = functions.take_user(message)

    if current_user not in known_users:
        functions.write_new_user(current_user)
        bot.send_message(message.chat.id, "Привет, я бот клоповника \n Рекомендуем ознакомиться в нашими правилами /about",
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
        bot.send_message(message.chat.id, 'Меню кино:', reply_markup=keyboard_generator(menus.cinema, True, False, 1))

    elif message.text == '"Рисовач"':
        bot.send_message(message.chat.id, 'Рисовач:', reply_markup=keyboard_generator(menus.paint, True, True, 1))

    elif message.text == 'Каллиграфия':
        bot.send_message(message.chat.id, 'Киллиграфия:', reply_markup=keyboard_generator(menus.kalli, True, True, 1))

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
    used_ids = functions.read_film_rates_with_id(0)

    if message.text == 'Предложить фильм':
        pass

    elif message.text == 'Посмотреть результаты':
        bot.send_message(message.chat.id, 'Результаты голосования:', reply_markup=menus.markup_cinema)
        # for key, film in enumerate(filmRates):
        #     key += 1
        #     bot.send_message(message.chat.id, str(key) + '. ' + film['film'] + ' - ' + str(film['vote_film']))

    elif message.text == 'Голосовать':

        if message.chat.id in used_ids:
            bot.send_message(message.chat.id, 'Вы уже проголосовали')
            # bot.send_message(message.chat.id, 'Результаты голосования:', reply_markup=menus.markup_crate)
            # for key, film in enumerate(filmRates):
            #     key += 1
            #     bot.send_message(message.chat.id, str(key) + '. ' + film['film'] + ' - ' + str(film['vote_film']))

        else:
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
    markup_gen = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard, row_width=row_width)
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
        ''', reply_markup=menus.markup_main)

    elif message.text == 'Ивенты':
        bot.send_message(message.chat.id, 'Ближайшие мероприятия:', reply_markup=keyboard_generator(menus.ivents, True, True, 1))

    elif message.text == 'Музыка':
        pass

    elif message.text == 'Как добраться':
        pass

    elif message.text == 'О КЛП':
        pass

    elif message.text == 'Главное меню':
        bot.send_message(message.chat.id, "Главное меню", reply_markup=keyboard_generator(menus.main_menu, True, True, 1))

    else:
        pass
        # markup_ivents(message)

# --------------------------------------------- Кронец блока меню ------------------------------------------------------


def choose_film_markup(buttons=config.vote_films):

    markup_choosefilm = types.InlineKeyboardMarkup(row_width=3)
    btn_in_film1 = types.InlineKeyboardButton(text=(buttons[0]['film_name'] + ' - ' + str(buttons[0]['rate'])),
                                              callback_data='film1')
    btn_in_film2 = types.InlineKeyboardButton(text=(buttons[1]['film_name'] + ' - ' + str(buttons[1]['rate'])),
                                              callback_data='film2')
    btn_in_film3 = types.InlineKeyboardButton(text=(buttons[2]['film_name'] + ' - ' + str(buttons[2]['rate'])),
                                              callback_data='film3')
    markup_choosefilm.add(btn_in_film1, btn_in_film2, btn_in_film3)

    return markup_choosefilm


# Обработчик меню голосования за кино
@bot.callback_query_handler(func=lambda c: c.data)
def choose_film(c):
    print(c)
    film_rates = functions.read_film_rates()
    if c.data == 'film1':
        film_rates[0]['vote_film'] += 1

    elif c.data == 'film2':
        film_rates[1]['vote_film'] += 1

    elif c.data == 'film3':
        film_rates[2]['vote_film'] += 1

    if functions.write_film_rates(film_rates):
        bot.edit_message_text(chat_id=c.message.chat.id,
                              text='Ваш выбор?',
                              message_id=c.message.message_id,
                              reply_markup=choose_film_markup(film_rates))
    # bot.send_message(c.from_user.id, 'Результаты голосования:', reply_markup=menus.markup_crate)
    # for key, film in enumerate(film_rates):
    #     key += 1
    #     bot.send_message(c.from_user.id, str(key) + '. ' + film['film'] + ' - ' + str(film['vote_film']))


bot.polling()