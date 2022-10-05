from cmath import log
from email.message import Message
from fractions import Fraction
import telebot
import os

first=""
second=""
script_dir = os.path.dirname(__file__)
history_for_bot = open(script_dir + '/history_for_bot .txt','r+', encoding='utf-8')

bot = telebot.TeleBot('5460917203:AAFcw5YBaPs57Q9f6elHGP1HRVkjbaus1No')

del_buttons = telebot.types.ReplyKeyboardRemove()
 
buttons1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1.row(telebot.types.KeyboardButton('Комплексные'),
             telebot.types.KeyboardButton('Рациональные'),)
buttons1.row(telebot.types.KeyboardButton('Ещё не определился'))
 
buttons2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons2.row(telebot.types.KeyboardButton('+'),
             telebot.types.KeyboardButton('-'))
buttons2.row(telebot.types.KeyboardButton('*'),
             telebot.types.KeyboardButton('/'))
 
def message(chat_id, text, reply_markup = None):
    bot.send_message(chat_id=chat_id,
                text=text,
                reply_markup=reply_markup)
    history_for_bot.write("БОТ:" + str(text) + '\n')


@bot.message_handler(commands=['log'])
def hello(msg: telebot.types.Message):
    logProgr = ""
    for mess in history_for_bot:
        logProgr += mess + "\n" 
    message(chat_id=msg.from_user.id,
                     text='Лог программы: \n' + logProgr,
                     reply_markup=del_buttons)

 
@bot.message_handler()
def hello(msg: telebot.types.Message):
    message(chat_id=msg.from_user.id,
                     text='Здравствуйте.\nВыберите режим работы калькулятора.',
                     reply_markup=buttons1)
    bot.register_next_step_handler(msg, answer)
 
 
def answer(msg: telebot.types.Message):
    history_for_bot.write("USER:" + msg.text + '\n')
    if msg.text == 'Комплексные':
        bot.register_next_step_handler(msg, second_msg)
        message(chat_id=msg.from_user.id,
                         text='Введите первое число',
                         reply_markup=del_buttons)
    elif msg.text == 'Рациональные':
        bot.register_next_step_handler(msg, second_msg)
        message(chat_id=msg.from_user.id,
                         text='Введите первое число.',
                         reply_markup=del_buttons)
    elif msg.text == 'Ещё не определился':
        bot.register_next_step_handler(msg, answer)
        message(chat_id=msg.from_user.id, text='Возвращайтесь, когда определитесь.')
    else:
        bot.register_next_step_handler(msg, answer)
        message(chat_id=msg.from_user.id, text='Пожалуйста, используйте кнопки.')
        message(chat_id=msg.from_user.id, text='Выберите режим работы калькулятора.', reply_markup=buttons1)
 

def second_msg(msg: telebot.types.Message):
    history_for_bot.write("USER:" + msg.text + '\n')
    global first
    if 'j' in msg.text or 'i' in msg.text:
        first=complex("".join(msg.text.split()).replace('i','j'))
    else:
        first=Fraction(int(msg.text.split('/')[0]), int(msg.text.split('/')[1]))
    bot.register_next_step_handler(msg,sign)
    message(chat_id=msg.from_user.id,
                         text='Введите второе число.',
                         reply_markup=del_buttons)


def sign(msg: telebot.types.Message):
    history_for_bot.write("USER:" + msg.text + '\n')
    global second
    if 'j' in msg.text or 'i' in msg.text:
        second=complex("".join(msg.text.split()).replace('i','j'))
    else:
        second=Fraction(int(msg.text.split('/')[0]), int(msg.text.split('/')[1]))
    bot.register_next_step_handler(msg,counter)
    message(chat_id=msg.from_user.id,text='Введите знак', reply_markup=buttons2)


def counter(msg: telebot.types.Message):
    history_for_bot.write("USER:" + msg.text + '\n')
    message(chat_id=msg.from_user.id, text='Ответ: ', reply_markup=del_buttons)
    if msg.text == "+":
        message(chat_id=msg.from_user.id, text=second + first)
    if msg.text == "-":
        message(chat_id=msg.from_user.id, text=first - second)
    if msg.text == "*":
        message(chat_id=msg.from_user.id, text=first * second)
    if msg.text == "/":
        message(chat_id=msg.from_user.id, text=first / second)
    
bot.polling()    
history_for_bot.close()
