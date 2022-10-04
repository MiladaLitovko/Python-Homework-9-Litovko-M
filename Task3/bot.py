import telebot
import os

script_dir = os.path.dirname(__file__)
# script_dir = script_dir + '/Task3'

bot = telebot.TeleBot('5524079314:AAGU7huAXLx5EBRtjvr17ph2KFmP0U2rIW4')

del_buttons = telebot.types.ReplyKeyboardRemove()
 
buttons1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1.row(telebot.types.KeyboardButton('экспорт данных'),
             telebot.types.KeyboardButton('импорт данных'))
buttons1.row(telebot.types.KeyboardButton('Ещё не определился'))


@bot.message_handler(commands=['log'])
def hello(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id,
                     text='Лог программы\newcoiywgecowegcouwefoyewfov',
                     reply_markup=del_buttons)

@bot.message_handler()
def hello(msg: telebot.types.Message):
    bot.send_message(chat_id=msg.from_user.id,
                     text='Здравствуйте.\nВведите действие, которое хотите совершить.',
                     reply_markup=buttons1)
    bot.register_next_step_handler(msg, answer)
 
 
def answer(msg: telebot.types.Message):
    if msg.text == 'экспорт данных':
        bot.register_next_step_handler(msg, export_info)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Выберите формат показа данных: \n1: Фамилия, Имя, Телефон, Описание \n2: \nФамилия \nИмя \nТелефон \nОписание \nВведите номер формата: ',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif msg.text == 'импорт данных':
        bot.register_next_step_handler(msg, import_info)
        bot.send_message(chat_id=msg.from_user.id,
                         text='Пришлите файл, который хотите импортировать в справочник.',
                         reply_markup=del_buttons)
    elif msg.text == 'Ещё не определился':
        bot.register_next_step_handler(msg, answer)
        bot.send_message(chat_id=msg.from_user.id, text='Возвращайтесь, когда определитесь.')
    else:
        bot.register_next_step_handler(msg, answer)
        bot.send_message(chat_id=msg.from_user.id, text='Пожалуйста, используйте кнопки.')
 
        bot.send_message(chat_id=msg.from_user.id, text='Введите действие, которое хотите совершить.', reply_markup=buttons1)


def export_info(msg: telebot.types.Message):
    chat_id=msg.from_user.id
    file = open(script_dir + '/guide.txt', 'r', encoding="utf-8") #изменить адрес файла
    new_file = open('Task3/export_file.txt', 'w', encoding="utf-8") 
    if msg.text == '1':
        for line in file:
            new_file.write(line) 
    elif msg.text == '2':
       for line in file:
            info = line.split(', ')
            for i in info:
                new_file.write(i + '\n')     
    else:
        file.close()
        new_file.close()
        print('Неверно введенная цифра - экспорт данных прерван')
        return
    file.close()
    new_file.close()
    doc = open('Task3/export_file.txt', 'rb')
    bot.send_document(chat_id, doc)
    # bot.send_document(chat_id, "FILEID")


@bot.message_handler(content_types=['document'])
def import_info(msg: telebot.types.Message):
    file_info = bot.get_file(msg.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = script_dir + "/" + msg.document.file_name
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    new_file.close()
    file = open('Task3/guide.txt', 'a', encoding="utf-8")  
    new_file = open(script_dir + "/" + msg.document.file_name, 'r', encoding="utf-8")
    line = new_file.readline()
    if len(line.split(', ')) == 4:
        file.write(line)
        for line in new_file:
            file.write(line + '\n')   
    else:
        user_info = line[:-1] + ', '
        for line in new_file:
            if line != '\n':
                user_info += line[:-1] + ', '
            else:
                file.write(user_info[:-2] + '\n')  
                user_info = ''
    file.close()
    new_file.close()
    bot.send_message(chat_id=msg.from_user.id, text='Спасибо за файл - добавим его в справочник!')


bot.polling()    