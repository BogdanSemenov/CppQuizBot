from requests import get
from bs4 import BeautifulSoup
from random import choice
from config import *


@add_method(bot)
def difficulty_rank(input_difficulty):
    """
    transform task's difficulty

    :param input_difficulty: str
    """
    if input_difficulty == '1':
        bot.difficulty = 'Easy'
    elif input_difficulty == '2':
        bot.difficulty = 'Medium'
    elif input_difficulty == '3':
        bot.difficulty = 'High'


@add_method(bot)
def check_users_answer(user_url):
    """
    check correctness of user's answers
    and increase his score

    :param user_url: str
    :return: str
    """
    request = get(user_url)
    scraping = BeautifulSoup(request.text, 'html.parser')
    txt = []
    for i in scraping.findAll('div', attrs={'id': "incorrect"}):
        txt.append(i.text)
        bot.attempts += 1
    for i in scraping.findAll('div', attrs={'id': "correct"}):
        txt.append(i.text)
        bot.score += 1
        bot.attempts += 1
    for i in scraping.findAll('div', attrs={'id': "hint"}):
        txt.append(i.text)
    return txt[0]


@add_method(bot)
def quiz_parsing():
    """
    Do parsing random C++ questions,
    difficulty of current  questions
    and its url from the web-page

    """
    user_number_quiz = choice([i for i in range(1, 251) if i not in numbers])
    bot.main_url = url.format(str(user_number_quiz))
    req = get(bot.main_url)
    result = []
    cur_difficulty = str()
    soup = BeautifulSoup(req.text, 'html.parser')
    for i in soup.findAll('div', attrs={'id': "main_col"}):
        result.append(i.text)
        cur_difficulty = i.find('img')['alt']

    difficulty_rank(cur_difficulty)
    bot.main_question = result[0]


@add_method(bot)
def extract_question_info():
    """
    Extract all types of answers
    and the main part of
    current question
    """

    result = bot.main_question[104: len(bot.main_question) - 119]

    bot.answer_3 = result[len(result) - 24:]
    result = result[:len(result) - 24]

    bot.answer_2 = result[len(result) - 52:len(result) - 1]
    result = result[:len(result) - 52]

    bot.answer_1 = result[len(result) - 36: len(result) - 1]
    result = result[:len(result) - 36]

    result = result[:len(result) - 50]

    bot.main_question = result


@add_method(bot)
def reply_on_answer(cur_message, cur_type):
    """
    reply on user's message

    :param cur_message: str
    :param cur_type: str
    :return: answer
    """
    new_url = bot.main_url + cur_type
    output = check_users_answer(new_url)
    bot.send_message(cur_message.chat.id, output, reply_markup=bot.markup_menu)


@add_method(bot)
def is_url_empty(message):
    if not bot.main_url:
        bot.send_message(message.chat.id, "You didn't choose any questions yet. Please, "
                                          "press button 'Try next question' or /start ")
        return True

    return False


@add_method(bot)
def make_button():
    bot.markup_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    bot.button_1 = telebot.types.KeyboardButton(bot.answer_1)
    bot.button_2 = telebot.types.KeyboardButton(bot.answer_2)
    bot.button_3 = telebot.types.KeyboardButton(bot.answer_3)
    bot.button_4 = telebot.types.KeyboardButton(bot.answer_4)
    bot.button_5 = telebot.types.KeyboardButton(bot.answer_5)
    bot.button_6 = telebot.types.KeyboardButton(bot.answer_6)
    bot.markup_menu.add(bot.button_1, bot.button_2, bot.button_3, bot.button_4, bot.button_5, bot.button_6)


@bot.message_handler(func=lambda message: True)
def quiz_play(message):
    """
    process of quiz

    :param message: text
    :return: text
    """

    if message.text == '/start':
        bot.quiz_parsing()
        bot.extract_question_info()
        bot.make_button()
        bot.send_message(message.chat.id, "Difficulty: {}\n\n".format(bot.difficulty) +
                         bot.main_question, reply_markup=bot.markup_menu)
        bot.send_message(message.chat.id, 'Text your answer if the program is guaranteed to output smth, '
                         'otherwise choose the correct answer in the menu', reply_markup=bot.markup_menu)

    elif message.text == bot.answer_1:
        if not bot.is_url_empty(message):
            bot.attempts += 1
            reply_on_answer(message, CE)

    elif message.text == bot.answer_2:
        if not bot.is_url_empty(message):
            reply_on_answer(message, US)

    elif message.text == bot.answer_3:
        if not bot.is_url_empty(message):
            reply_on_answer(message, UD)

    elif message.text == bot.answer_4:
        if not bot.is_url_empty(message):
            reply_on_answer(message, HINT)

    elif message.text == bot.answer_5:
        bot.quiz_parsing()
        bot.extract_question_info()
        bot.make_button()
        bot.send_message(message.chat.id, "Difficulty: {}\n\n".format(bot.difficulty) + bot.main_question,
                         reply_markup=bot.markup_menu)

    elif message.text == bot.answer_6:
        bot.send_message(message.chat.id, 'Your score: {} / {}'.format(bot.score, bot.attempts),
                         reply_markup=bot.markup_menu)

    else:
        if not bot.is_url_empty(message):
            new_url = bot.main_url + OK.format(message.text)
            output = check_users_answer(new_url)
            bot.send_message(message.chat.id, output, reply_markup=bot.markup_menu)
