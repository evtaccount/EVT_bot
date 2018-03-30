from telebot import types
import config

main_menu = {'name': 'main_menu', 'buttons': ['Правила', 'Ивенты', 'Музыка', 'Как добраться']}
ivents = {'name': 'ivents', 'buttons': ['Ближайший ивент', 'День кино', '"Рисовач"', 'Каллиграфия', 'Главное меню']}
cinema = {'name': 'cinema', 'buttons': ['Предложить фильм', 'Голосование', 'История', 'Главное меню']}
paint = {'name': 'paint', 'buttons': ['О Рисоваче', 'Главное меню']}
kalli = {'name': 'kalli', 'buttons': ['О Каллиграфии', 'Записаться на занятие', 'Главное меню']}


# Меню голосования за фильмы
markup_crate = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
btn_crate_rerate = types.KeyboardButton('Переголосовать')
btn_crate_back = types.KeyboardButton('Главное меню')
markup_crate.add(btn_crate_rerate, btn_crate_back)




