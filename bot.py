from requests import get
from bs4 import BeautifulSoup
from random import choice
import telebot
from config import *

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
    scraping = BeautifulSoup(request.text, 'html.parser')
    txt = []
    for i in scraping.findAll('div', attrs={'id': "incorrect"}):
        txt.append(i.text)
    for i in scraping.findAll('div', attrs={'id': "correct"}):
        txt.append(i.text)
        score += 1
    for i in scraping.findAll('div', attrs={'id': "hint"}):
        txt.append(i.text)
    return txt[0]


attempts = 0
score = 0


def quiz():
    user_quiz = choice([i for i in range(1, 251) if i not in numbers])
    input_url = url.format(str(user_quiz))
    req = get(input_url)
    result = []
    input_difficulty = 0
    soup = BeautifulSoup(req.text, 'html.parser')
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
    result = result[0][104: len(result[0]) - 119]

    answer_4 = result[len(result) - 24:]
    result = result[:len(result) - 24]

    answer_3 = result[len(result) - 52:len(result) - 1]
    result = result[:len(result) - 52]

    answer_2 = result[len(result) - 36: len(result) - 1]
    result = result[:len(result) - 36]

    answer_1 = result[len(result) - 37: len(result) - 1]
    result = result[:len(result) - 37]

    result = result[:len(result) - 13]

    return result


res = answ(res)

answer_5 = 'View a hint'
answer_6 = 'Try another question'
answer_7 = 'Score'

markup_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_2 = telebot.types.KeyboardButton(answer_2)
btn_3 = telebot.types.KeyboardButton(answer_3)
btn_4 = telebot.types.KeyboardButton(answer_4)
btn_5 = telebot.types.KeyboardButton(answer_5)
btn_6 = telebot.types.KeyboardButton(answer_6)
btn_7 = telebot.types.KeyboardButton(answer_7)
markup_menu.add(btn_2, btn_3, btn_4, btn_5, btn_6, btn_7)


@bot.message_handler(func=lambda message: True)
def quiz_play(message):
    global current_url, attempts
    
    if message.text == '/start':
        attempts += 1
        bot.send_message(message.chat.id, "Difficulty: {}\n\n".format(difficulty_rank(difficulty)) + res,
                         reply_markup=markup_menu)
        bot.send_message(message.chat.id, 'Text your answer if the program is guaranteed to output smth, '
                                          'otherwise choose the correct answer in the menu', reply_markup=markup_menu)

    elif message.text == answer_2:
        attempts += 1
        new_url = current_url + CE
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

    elif message.text == answer_3:
        attempts += 1
        new_url = current_url + US
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

    elif message.text == answer_4:
        attempts += 1
        new_url = current_url + UD
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

    elif message.text == answer_5:
        new_url = current_url + HINT
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

    elif message.text == answer_6:
        attempts += 1
        next_question, next_url, next_difficulty = quiz()
        current_url = next_url
        next_question = answ(next_question)
        bot.reply_to(message, "Difficulty: {}\n\n".format(difficulty_rank(next_difficulty)) + next_question,
                     reply_markup=markup_menu)

    elif message.text == answer_7:
        bot.send_message(message.chat.id, 'Your score: {} / {}'.format(score, attempts), reply_markup=markup_menu)

    else:
        attempts += 1
        new_url = current_url + OK.format(message.text)
        output = parsing(new_url)
        bot.reply_to(message, output, reply_markup=markup_menu)

