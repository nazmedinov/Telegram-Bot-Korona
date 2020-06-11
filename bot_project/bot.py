import telebot
from telebot import types
bot = telebot.TeleBot('1240093961:AAEy7nZykUMeA74AkTvk0CEj7bSvkHRsPUs')

import sqlite3
db = sqlite3.connect('bot.db', check_same_thread=False)
cur = db.cursor()

sum = 0

def keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
    btn1 = types.KeyboardButton('Я заболел')
    btn2 = types.KeyboardButton('Я не болею')
    btn3 = types.KeyboardButton('Статистика')
    markup.add(btn1, btn2, btn3)
    return markup

def AddUser(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("INSERT INTO information (id, status) VALUES (?, ?);", (user_id, 'Заболел'))
    conn.commit()
    conn.close()

def DelUser(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('DELETE FROM information where id=(?) and 5=(?);', (user_id, 5))
    conn.commit()
    conn.close()

def Stat():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    global sum
    c.execute('SELECT COUNT(*) FROM information')
    sum = c.fetchone()
    conn.commit()
    conn.close()
    return sum[0]

@bot.message_handler(commands=["start"])
def send_buttoms(message):
    bot.send_message(message.chat.id, 'Приветствую!\nБот показывает статистику по коронавирусу онлайн!\nДля больше информации введите команду /help !', reply_markup = keyboard())

@bot.message_handler(commands=["help"])
def send_info(message):
    bot.send_message(message.chat.id, "Данный бот показывает реальную статистику заболеваемости коронавирусом:\n1. Введите 'Я заболел', если вы болеете коронавирусом.\n2. Введите 'Я не болею', если вы не болеете коронавирусом или вылечились.\n3. Введите 'Статистика', чтобы посмотреть количество зараженных людей по информации бота.", reply_markup = keyboard())


@bot.message_handler(content_types=["text"])
def send_anytext(message):
    if message.text.lower() == 'я заболел':
        try:
            AddUser(message.from_user.id)
            bot.send_message(message.chat.id, 'Вы были добавлены в список заболевших!', reply_markup=keyboard())
        except:
            bot.send_message(message.chat.id, 'Вы уже добавлены в список заболевших!', reply_markup=keyboard())
    elif message.text.lower() == 'я не болею':
        try:
            DelUser(message.from_user.id)
            bot.send_message(message.chat.id, 'Вы не числитесь в списке заболевших!', reply_markup=keyboard())
        except:
            bot.send_message(message.chat.id, 'Вы здоровы!', reply_markup=keyboard())
    elif message.text.lower() == 'статистика':
        x = Stat()
        bot.send_message(message.chat.id, f'По информации бота количество зараженных в данный момент: {x}', reply_markup=keyboard())
    else:
        bot.send_message(message.chat.id, 'Не могу выполнить ваш запрос, используйте команду /help для помощи!', reply_markup = keyboard())

if __name__ == '__main__':
    bot.polling(none_stop=True)






