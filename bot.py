from requests import get
from bs4 import BeautifulSoup
from random import choice
import telebot
from telebot import types
from config import *


token = "864062625:AAHt_xciZildH4u6VkGM8veN_GPzxBh6fjc"
bot = telebot.TeleBot(token)


def difficulty_rank(cur_difficulty):
    if cur_difficulty == '1':
        return 'Easy'
    elif cur_difficulty == '2':
        return 'Medium'
    elif cur_difficulty == '3':
        return 'High'


def parsing(user_url):
    global score
    request = get(user_url)
    scraping = BeautifulSoup(request.text, 'lxml')
    txt = []
    for i in scraping.findAll('div', attrs={'id': "incorrect"}):
        txt.append(i.text)
    for i in scraping.findAll('div', attrs={'id': "correct"}):
        txt.append(i.text)
        score += 1
    for i in scraping.findAll('div', attrs={'id': "hint"}):
        txt.append(i.text)
    return txt[0]


# easy_score = 0
# medium_score = 0
# hard_score = 0
# failed_answers = 0
attempts = 0
score = 0
# quiz_over = False


def quiz():
    user_quiz = choice([i for i in range(1, 251) if i not in numbers])
    input_url = url.format(str(user_quiz))
    req = get(input_url)
    result = []
    input_difficulty = 0
    soup = BeautifulSoup(req.text, 'lxml')
    for i in soup.findAll('div', attrs={'id': "main_col"}):
        result.append(i.text)
        input_difficulty = i.find('img')['alt']

    return result, input_url, input_difficulty


res, current_url, difficulty = quiz()


answer_1 = 0
answer_2 = 0
answer_3 = 0
answer_4 = 0


def answ(result):
    global answer_1, answer_2, answer_3, answer_4
    # question = result[0][29: 99]
    result = result[0][104: len(result[0]) - 119]

    answer_4 = result[len(result) - 24:]
    result = result[:len(result) - 24]

    answer_3 = result[len(result) - 52:len(result) - 1]
    result = result[:len(result) - 52]

    answer_2 = result[len(result) - 36: len(result) - 1]
    result = result[:len(result) - 36]

    answer_1 = result[len(result) - 37: len(result) - 1]
    result = result[:len(result) - 37]

    # answer = result[len(result) - 9: len(result) - 2]
    result = result[:len(result) - 13]

    return result


res = answ(res)

answer_5 = 'View a hint'
answer_6 = 'Try another question'
answer_7 = 'Score'

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_2 = types.KeyboardButton(answer_2)
btn_3 = types.KeyboardButton(answer_3)
btn_4 = types.KeyboardButton(answer_4)
btn_5 = types.KeyboardButton(answer_5)
btn_6 = types.KeyboardButton(answer_6)
btn_7 = types.KeyboardButton(answer_7)
markup_menu.add(btn_2, btn_3, btn_4, btn_5, btn_6, btn_7)


# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.send_message(message.chat.id, "Difficulty: {}\n\n".format(difficulty_rank(difficulty)) + res,
#                      reply_markup=markup_menu)
#     bot.send_message(message.chat.id, 'Text your answer if the program is guaranteed to output smth, '
#                                       'otherwise choose the correct answer in the menu', reply_markup=markup_menu)


@bot.message_handler(func=lambda message: True)
def quiz_play(message):
    global current_url, attempts
    attempts += 1

    if message.text == '/start':
        bot.send_message(message.chat.id, "Difficulty: {}\n\n".format(difficulty_rank(difficulty)) + res,
                         reply_markup=markup_menu)
        bot.send_message(message.chat.id, 'Text your answer if the program is guaranteed to output smth, '
                         'otherwise choose the correct answer in the menu', reply_markup=markup_menu)

    elif message.text == answer_2:
        new_url = current_url + CE
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

    elif message.text == answer_3:
        new_url = current_url + US
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

    elif message.text == answer_4:
        new_url = current_url + UD
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

    elif message.text == answer_5:
        new_url = current_url + HINT
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

    elif message.text == answer_6:
        next_question, next_url, next_difficulty = quiz()
        current_url = next_url
        next_question = answ(next_question)
        bot.reply_to(message, "Difficulty: {}\n\n".format(difficulty_rank(next_difficulty)) + next_question,
                     reply_markup=markup_menu)

    elif message.text == answer_7:
        bot.send_message(message.chat.id, 'Your score: {} / {}'.format(score, attempts), reply_markup=markup_menu)

    else:
        new_url = current_url + OK.format(message.text)
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)


if __name__ == '__main__':
    bot.polling(none_stop=True)
# счёт поправить, т.к увеличивает на два
