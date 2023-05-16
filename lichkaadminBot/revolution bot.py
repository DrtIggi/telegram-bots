import telebot,time,sqlite3
import telebot.types as types
token='668821360:AAH8i3JHKYIt8YGK4NWDo1nRASU66Z4uPHc'
bot=telebot.TeleBot(token)
admin_name='Danya2904'
tx=[]

def check(message):
    conn=sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("SELECT chat_id FROM main WHERE chat_id = "+str(message.chat.id))
    if cursor.fetchone()==None:
        cursor.execute("insert into main values ('"+str(message.chat.id)+"','"+message.json['from']['username']+"') ")
        conn.commit()

    conn.close()
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.json['from']['username']==admin_name or message.json['from']['username']=="dirtyiggi":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Добавить направление")
        user_markup.row("Удалить направление")
        user_markup.row("Добавить исполнителя")
        user_markup.row("Удалить исполнителя")
        user_markup.row("Направления")
        bot.send_message(message.chat.id,"Приветствую в админ панели",reply_markup=user_markup)
@bot.message_handler(commands=['directions'])
def directions(message):
    conn = sqlite3.connect("directiondatabase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM main")
    key = types.InlineKeyboardMarkup()
    for x in cursor.fetchall():
        key.add(types.InlineKeyboardButton(x[0], callback_data=x[0]))
    bot.send_message(message.chat.id,"Направления:",reply_markup=key)
    conn.close()
@bot.message_handler(commands=['start'])
def start(message):

    try:
        message.json['from']['username']
    except:
        bot.send_message(message.chat.id,
                         "Извини😢, для начала создай себе username (в настройках), без него ты не сможешь пользоваться ботом😎")
        return 0

    check(message)

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("Направления")
    bot.send_message(message.chat.id,"Приветствую!",reply_markup=user_markup)

def delete_exec_step_two(message):
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM main WHERE name='"+str(tx[0])+"' and direction = '"+str(tx[1])+"'")
    conn.commit()
    conn.close()
    tx.clear()
    bot.send_message(message.chat.id, "Готово")
    admin(message)
def delete_exec_step_one(message):

    tx.append(message.text)

    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton("Назад", callback_data='back2'))





    conn = sqlite3.connect("directiondatabase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM main")
    key = types.InlineKeyboardMarkup()
    for x in cursor.fetchall():
        key.add(types.InlineKeyboardButton(x[0], callback_data="#"+x[0]))
    key.add(types.InlineKeyboardButton("Назад", callback_data='back2'))
    conn.close()
    bot.send_message(message.chat.id, "Теперь выбери направление", reply_markup=key)


def add_exec_step_four(message):
    conn = sqlite3.connect("ex.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO main values ('"+str(tx[1])+"','"+message.text+"','"+str(tx[0])+"')")
    conn.commit()
    conn.close()
    tx.clear()
    bot.send_message(message.chat.id, "Готово")
    admin(message)
def add_exec_step_three(message):
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton("Назад", callback_data='back2'))
    try:

        with open("./photos/" + tx[0]+"%%%"+tx[1] + ".png", "wb") as file:
            file_info = bot.get_file(message.json['photo'][2]['file_id'])
            downloaded_file = bot.download_file(file_info.file_path)
            file.write(downloaded_file)
        bot.send_message(message.chat.id, "Теперь напиши краткую информацию", reply_markup=key)
        bot.register_next_step_handler(message, add_exec_step_four )

    except:

        bot.send_message(message.chat.id,"Прости, но ты отправил не фото, попробуй еще раз",reply_markup=key)
        bot.register_next_step_handler(message,add_exec_step_three)
def add_exec_step_two(message):
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton("Назад", callback_data='back2'))
    tx.append(message.text)
    bot.send_message(message.chat.id, "Теперь пришли фото",reply_markup=key)
    bot.register_next_step_handler(message, add_exec_step_three,)
def add_exec_step_one(message):
    tx.append(message.text)



    conn = sqlite3.connect("directiondatabase.db")  # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM main")
    key = types.InlineKeyboardMarkup()
    for x in cursor.fetchall():
        key.add(types.InlineKeyboardButton(x[0], callback_data="$"+x[0]))
    key.add(types.InlineKeyboardButton("Назад", callback_data='back2'))
    conn.close()
    bot.send_message(message.chat.id, "Теперь выбери направление", reply_markup=key)



def add_directions(message):
    conn = sqlite3.connect("directiondatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT direction FROM main WHERE direction = '" + message.text + "'")
    if cursor.fetchone() == None:
        cursor.execute("insert into main values ('" + message.text + "') ")
        conn.commit()
        bot.send_message(message.chat.id, "Готово")

    else:
        bot.send_message(message.chat.id, "Извините, это направление уже есть")
    admin(message)
    conn.close()
@bot.message_handler(content_types=['text'])
def text(message):
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton("Назад", callback_data='back2'))
    if message.text=="Направления":
        directions(message)
    elif message.text=="Добавить направление":
        if message.json['from']['username'] == admin_name or message.json['from']['username']=="dirtyiggi":
            bot.send_message(message.chat.id,"Напишите название направления",reply_markup=key)
            bot.register_next_step_handler(message,add_directions)
    elif message.text=="Добавить исполнителя":
        if message.json['from']['username'] == admin_name or message.json['from']['username']=="dirtyiggi":
            tx.clear()
            bot.send_message(message.chat.id,"Напишите сначала его username (без @)",reply_markup=key)
            bot.register_next_step_handler(message, add_exec_step_one)
    elif message.text=="Удалить направление":
        if message.json['from']['username'] == admin_name or message.json['from']['username']=="dirtyiggi":
            tx.clear()

            key = types.InlineKeyboardMarkup()


            conn = sqlite3.connect("directiondatabase.db")  # или :memory: чтобы сохранить в RAM
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM main")
            for x in cursor.fetchall():
                key.add(types.InlineKeyboardButton(x[0], callback_data="^" + x[0]))
            key.add(types.InlineKeyboardButton("Назад", callback_data='back2'))
            bot.send_message(message.chat.id, "Выбери направление (после удаления все исполнители данного направления также удаляться)", reply_markup=key)
            conn.close()
    elif message.text=="Удалить исполнителя":
        if message.json['from']['username'] == admin_name or message.json['from']['username']=="dirtyiggi":
            tx.clear()
            bot.send_message(message.chat.id,"Напишите его username (без @)",reply_markup=key)
            bot.register_next_step_handler(message,delete_exec_step_one)
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    if call.data[0]=="^":

        conn = sqlite3.connect("directiondatabase.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM main WHERE direction = '" + str(call.data[1:]) + "'")
        conn.commit()
        conn.close()
        tx.clear()
        conn = sqlite3.connect("ex.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM main WHERE direction = '" + str(call.data[1:]) + "'")
        conn.commit()
        conn.close()
        bot.send_message(call.message.chat.id, "Готово")
        admin(call.message)
        return 0
    if call.data[0]=="#":
        tx.append(call.data[1:])
        delete_exec_step_two(call.message)
        return 0
    if call.data[0]=="$":
        tx.append(call.data[1:])
        add_exec_step_two(call.message)
        return 0
    if call.data=='back':
        bot.clear_step_handler(call.message)
        directions(call.message)
        return 0
    elif call.data=="back2":

        bot.clear_step_handler(call.message)
        bot.edit_message_text("Приветствую в админ панели!",call.message.chat.id,call.message.message_id)
        return 0
    else:


        conn = sqlite3.connect("ex.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM main WHERE direction = '"+call.data+"'")
        res=cursor.fetchall()

        if res==[]:
            bot.edit_message_text("Прости, пока нет исполнителей...",call.message.chat.id,call.message.message_id)

            conn.close()
            directions(call.message)
            return 0

        bot.edit_message_text("Подождите...",call.message.chat.id,call.message.message_id)
        key = types.InlineKeyboardMarkup()
        key.add(types.InlineKeyboardButton("Назад", callback_data='back'))
        for x in res:
            try:
                with open("./photos/" + str(x[2]+"%%%"+x[0]) + ".png", "rb") as file:
                    bot.send_photo(call.message.chat.id,file,str(x[0])+"\n"+str(x[1])+"\n"+"@"+str(x[2]),reply_markup=key)
            except Exception as f:

                bot.send_message(call.message.chat.id, str(x[0]) + "\n" + str(x[1]) + "\n" + "@" + str(x[2]),
                                 reply_markup=key)
        conn.close()
def polling():
    try:
        bot.polling(timeout=2)
    except Exception as f:
        time.sleep(5)
        print(f)
        polling()
if __name__=='__main__':
    polling()

"""
#если ты это читаешь, ты конч

conn = sqlite3.connect("database.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

# Создание таблицы
cursor.execute('''CREATE
TABLE
main
(chat_id
text, monster
text, level
text)'''
)
conn.close()


"""