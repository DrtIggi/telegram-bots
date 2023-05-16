import telebot,time,sqlite3,os
import telebot.types as types
from datetime import datetime
token='654067993:AAFelWe-DhkArfO7npkEYjPeEt5MeDKWgyo'
bot=telebot.TeleBot(token)
massiv=[6]
admin_name="232673077"
number_massiv=['first','second','third','fourth','fifth']
def check(message):
    conn=sqlite3.connect("userbase.db")
    cursor=conn.cursor()
    t = (str(message.chat.id),)
    cursor.execute("SELECT chat_id FROM main WHERE chat_id = ?", t)
    if cursor.fetchone()==None:
        z=(str(message.json['from']['username']),str(message.chat.id),)
        cursor.execute("insert into main values (?,?,Null) ",z)
        conn.commit()
    conn.close()
def redaction(message,number):
    if message.json['chat']['username'] == admin_name or message.json['chat']['username'] == "dirtyiggi":
        massiv[0] = 6
        try:
            conn = sqlite3.connect("adminbase.db")  # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE main SET " + number_massiv[number - 1] + " = '" + str(message.text) + "'")
            bot.send_message(message.chat.id, "Готово")
            conn.commit()
            conn.close()
            admin(message)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(message.chat.id, "Произошла ошибка")
    else:
        pass
@bot.message_handler(commands=['start'])
def start(message):
    try:
        check(message)
    except Exception as f:
        os.system("echo " + str(f) + " >> exception")
    try:
        r=yes("first","adminbase.db")
        bot.send_message(message.chat.id,"☺️Привет бро!\nМы тут разоряем букмекеров при помощи валуйных ставок и инсайдов.\n___________\n🚨Чистая прибыль составляет более 200% к начальному банку в месяц. В нашем деле все решает математика и связи.\nИнтересно?😉")
        key = types.InlineKeyboardMarkup()
        key.add(types.InlineKeyboardButton("Да", callback_data="Yes"),
            types.InlineKeyboardButton("Нет", callback_data="No"))
        bot.send_message(message.chat.id,str(r[0][0]),reply_markup=key)
    except Exception as f:
        os.system("echo " + str(f) + " >> exception")
        bot.send_message(message.chat.id,"Произошла ошибка")
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.json['chat']['username'] == admin_name or message.json['chat']['username'] == "dirtyiggi":
        key = types.InlineKeyboardMarkup()
        key.add(types.InlineKeyboardButton("Редактировать текст", callback_data="red"))
        key.add(types.InlineKeyboardButton("Информация о пользователях", callback_data="user_info"))
        key.add(types.InlineKeyboardButton("Пробные пользователи", callback_data="suki"))
        key.add(types.InlineKeyboardButton("Очистить пробных", callback_data="delete"))
        key.add(types.InlineKeyboardButton("Очистить пользователей (yes/no)", callback_data="userdelete"))
        bot.send_message(message.chat.id, "Приветствую в админ панели", reply_markup=key)
    else:
        pass
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data=="Yes":
        try:
            bot.delete_message(call.message.chat.id,call.message.message_id)
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton("Начать зарабатывать", callback_data="begin"))
            r=yes("second","adminbase.db")
            bot.send_message(call.message.chat.id,r[0][0],reply_markup=key)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id, "Произошла ошибка")
    elif call.data=="begin":
        try:
            bot.delete_message(call.message.chat.id,call.message.message_id)
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton("Да", callback_data="yes2"),types.InlineKeyboardButton("Нет", callback_data="No2"))
            r=yes("third","adminbase.db")
            bot.send_message(call.message.chat.id,r[0][0],reply_markup=key)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id, "Произошла ошибка")
    elif call.data=="No2":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            set_info(call.message,"Нет")
            user_markup = telebot.types.ReplyKeyboardRemove()
            r=no(call.message)
            bot.send_message(call.message.chat.id, r[0][0])
            bot.send_message(call.message.chat.id, r[1][0],reply_markup=user_markup)
            set_time(call.message)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id, "Произошла ошибка")
    elif call.data=="suki":
        try:
            suki(call.message)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id, "Произошла ошибка")
    elif call.data=="No":
        try:
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton("Назад", callback_data="back2"))
            bot.delete_message(call.message.chat.id, call.message.message_id)
            r=no(call.message)
            bot.send_message(call.message.chat.id, r[0][0])
            bot.send_message(call.message.chat.id, r[1][0], reply_markup=key)
            set_time(call.message)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id,"Произошла ошибка")
    elif call.data=="user_info":
        try:
            conn = sqlite3.connect("userbase.db")  # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM main")
            r=cursor.fetchall()
            for x in r:
                bot.send_message(call.message.chat.id,"@"+str(x[0])+": "+str(x[2]))
            conn.close()
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton("Назад", callback_data="back"))
            bot.send_message(call.message.chat.id,"Вернуться в админ панель",reply_markup=key)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id, "Произошла ошибка")
    elif call.data=="back2":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            start(call.message)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id, "Произошла ошибка")
    elif call.data=="yes2":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            set_info(call.message, "Да")
            bot.send_message(call.message.chat.id, "Держи подарок! Доступ в закрытый канал бесплатно на сегодня!")
            user_markup = telebot.types.ReplyKeyboardRemove()
            r=yes("fifth","adminbase.db")
            bot.send_message(call.message.chat.id, r[0][0], reply_markup=user_markup)
            set_time(call.message)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id, "Произошла ошибка")
    elif call.data=="red":
        try:
            conn = sqlite3.connect("adminbase.db")  # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM main")
            y=1
            r=cursor.fetchall()[0]
            for x in r:
                key = types.InlineKeyboardMarkup()
                if x==None:
                    key.add(types.InlineKeyboardButton("Редактировать", callback_data="#" + str(y)))
                    bot.send_message(call.message.chat.id, "пусто", reply_markup=key)
                    y += 1
                else:
                    key.add(types.InlineKeyboardButton("Редактировать", callback_data="#" + str(y)))
                    bot.send_message(call.message.chat.id, str(x),reply_markup=key)
                    y+=1
            conn.close()
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id,"Прости, ошибка")
    elif call.data=="delete":
        try:
            bot.delete_message(call.message.chat.id,call.message.message_id)
            conn = sqlite3.connect("debtorbase.db")  # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            cursor.execute("DELETE FROM main")
            conn.commit()
            conn.close()
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton("Назад", callback_data="back"))
            bot.send_message(call.message.chat.id,"Готово",reply_markup=key)
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id, "Прости, ошибка")
    elif call.data[0]=="#":
        try:
            key = types.InlineKeyboardMarkup()
            key.add(types.InlineKeyboardButton("Назад", callback_data="back"))
            bot.delete_message(call.message.chat.id,call.message.message_id)
            bot.send_message(call.message.chat.id,"Напиши текст",reply_markup=key)
            massiv[0]=int(call.data[1:])
        except Exception as f:
            os.system("echo " + str(f) + " >> exception")
            bot.send_message(call.message.chat.id,"Прости ошибка")
            massiv[0]=6
    elif call.data=="back":
        massiv[0]=6
        bot.delete_message(call.message.chat.id,call.message.message_id)
        admin(call.message)
    elif call.data=="userdelete":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        conn = sqlite3.connect("userbase.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        cursor.execute("DELETE FROM main")
        conn.commit()
        conn.close()
        key = types.InlineKeyboardMarkup()
        key.add(types.InlineKeyboardButton("Назад", callback_data="back"))
        bot.send_message(call.message.chat.id, "Готово", reply_markup=key)
@bot.message_handler(content_types=['text'])
def text(message):

    if massiv[0]==6:
        return 0
    else:
        redaction(message,massiv[0])
def set_time(message):
    conn = sqlite3.connect("timebase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM main WHERE username = '"+str(message.json['chat']['username'])+"'")

    if cursor.fetchone() == None:
        r = datetime.strftime(datetime.now(), "%H:%M")
        if r[3] == '0':
            if r[4]=='0':
                q = str(int(r[:2])-1)
                r=q+":59"
            else:
                q = r[:4]
                w = str(int(r[4]) - 1)
                r = q + w
        else:
            q=r[:3]
            w=str(int(r[3:5])-1)
            r=q+w
        t = (str(message.json['chat']['username']),r,)
        cursor.execute(
            "insert into main values (?,?) ",t)
        conn.commit()
    conn.close()
def suki(message):
    bot.delete_message(message.chat.id, message.message_id)
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton("Назад", callback_data="back"))
    r=yes("debtor","debtorbase.db")
    if r == []:
        bot.send_message(message.chat.id,"Пробных пользователей нет")
    else:
        for x in r:
            bot.send_message(message.chat.id,"@"+x[0])
    bot.send_message(message.chat.id,"Вернуться в админ панель",reply_markup=key)
def set_info(message,info):
    conn = sqlite3.connect("userbase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    t = (str(info),str(message.chat.id),)
    cursor.execute(
        "UPDATE main SET info = ? WHERE chat_id = ?",t)
    conn.commit()
    conn.close()
def yes(text,base):
    conn = sqlite3.connect(base)  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("SELECT " + text + " FROM main")
    r = cursor.fetchall()
    conn.close()
    return r
def no(message):
    set_info(message, "Нет")
    conn = sqlite3.connect("adminbase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("SELECT fourth FROM main")
    one=cursor.fetchall()
    cursor.execute("SELECT fifth FROM main")
    two=cursor.fetchall()
    conn.close()
    return one+two
def polling():
    try:
        bot.polling(timeout=2)
    except Exception as f:
        time.sleep(5)
        polling()
        os.system("echo "+str(f)+" >> exception")
if __name__=="__main__":
        polling()
"""


conn = sqlite3.connect("timebase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''CREATE
TABLE
main
(username
text, time
text)'''
)
cursor.execute("INSERT into main values ('dirtyiggi','21:52')")
conn.commit()
conn.close()


conn = sqlite3.connect("debtorbase.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''CREATE
TABLE
main
(debtor
text)'''
)
cursor.execute("INSERT into main values ('dirtyiggi')")
conn.commit()
cursor.execute("INSERT into main values ('diiggi')")
conn.commit()
conn.close()
"""
