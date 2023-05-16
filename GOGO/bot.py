# -*- coding: utf8 -*-
import telebot
import os
import sqlite3
import xlwt

admin_id = ['232673077', '438653934']

# '438653934'
# 1351249927:AAHAhWbjWeY0Wo8X2jgg4OfUyNIbpSTpLQ4
# 1288565459:AAEYcH5uxrb1K0lAiZntDbTNbwi3ykkZtgc
token = "1288565459:AAEYcH5uxrb1K0lAiZntDbTNbwi3ykkZtgc"

bot = telebot.TeleBot(token)
path = '/root/GOGO/'


def checkifuserindb(message):
    conn = sqlite3.connect(f"{path}users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT username FROM main WHERE chat_id = {message.chat.id}")

    if cursor.fetchone() is None:
        try:
            x = message.json['from']['last_name']

            cursor.execute(
            f"insert into main values ('{message.chat.id}',"
            f" {message.chat.id}, '{message.json['from']['first_name']} {x}')")
            dyn_memory(message.chat.id, 'None',
                       message.json['from']['first_name'] + ' ' + message.json['from']['last_name'])
        except Exception:
            cursor.execute(
                f"insert into main values ('{message.chat.id}',"
                f" {message.chat.id}, '{message.json['from']['first_name']}')")
            dyn_memory(message.chat.id, 'None',
                       message.json['from']['first_name'])
        conn.commit()
        conn.close()

        for x in admin_id:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("✅",
                                                       callback_data=f"phil"),
                    telebot.types.InlineKeyboardButton("❌", callback_data="x"))
            bot.send_message(int(x),
                             f"Пользователь /{message.json['from']['first_name']} зарегистрировался в боте!\
                             \n\n Хотите добавить его в какой нибудь список?",
                             reply_markup=key)


@bot.message_handler(commands=['admin'])
def admin(message):
    try:
        if str(message.chat.id) not in admin_id:
            return 1
        else:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("Списки пользователей", callback_data="Получить списки"))
            key.add(telebot.types.InlineKeyboardButton("Список опросов", callback_data="showquiz"))
            key.add(telebot.types.InlineKeyboardButton("Создать опрос", callback_data="Сделать опрос"))
            key.add(telebot.types.InlineKeyboardButton("Статистика голосований", callback_data="stat"))
            bot.send_message(message.chat.id, "*Добро пожаловать в админ панель!*", parse_mode="Markdown",
                             reply_markup=key)
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


def makealist(message):
    try:
        key = telebot.types.InlineKeyboardMarkup()
        key.add(telebot.types.InlineKeyboardButton("✅", callback_data="makealistsure"),
                telebot.types.InlineKeyboardButton("❌", callback_data="x"))
        bot.send_message(message.chat.id, message.text, reply_markup=key)
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


def userinlist(array, username):
    for x in array:
        if username in x:
            return True
    return False

def getdyn_memory():
    conn = sqlite3.connect(f"{path}dyn_memory.db")
    cursor = conn.cursor()
    res = cursor.execute(f"SELECT * FROM main").fetchone()
    cursor.execute(f"DELETE FROM main")
    conn.commit()
    conn.close()
    if res is not None:
        return res
def dyn_memory(one, two, three):

    conn = sqlite3.connect(f"{path}dyn_memory.db")
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM main")
    conn.commit()
    cursor.execute(f"insert into main values ('{one}', '{two}', '{three}')")
    conn.commit()
    conn.close()




# noinspection PyBroadException,PyBroadException
def editlist(message, listname):
    try:
        key = telebot.types.InlineKeyboardMarkup()
        conn = sqlite3.connect(f"{path}lists.db")
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM '{listname}'").fetchall()
        conn.close()
        username = message.text
        if username[0] != '@' and username[0] != '/':
            # noinspection PyBroadException,PyBroadException,PyBroadException
            try:
                username = message.forward_from.username
            except Exception:
                username = ''
        else:
            username = username[1:]

        if userinlist(result, username):
            conn = sqlite3.connect(f"{path}users.db")
            cursor = conn.cursor()
            info = cursor.execute(f"SELECT name FROM main WHERE username = '{username}'").fetchone()
            conn.close()

            dyn_memory(username, listname, info[0])

            key.add(telebot.types.InlineKeyboardButton("✅",
                                                       callback_data=f"deletefromlistsure"),
                    telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
            bot.send_message(message.chat.id,
                             f"Пользователь '{info[0]}' присутствует в списке!\
                             \n\n Хотите удалить его из {listname}?",
                             reply_markup=key)

        else:

            conn = sqlite3.connect(f"{path}users.db")
            cursor = conn.cursor()
            result = cursor.execute(f"SELECT username, name FROM main WHERE username = '{username}'").fetchone()
            conn.close()
            if len(result) == 0:
                key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
                bot.send_message(message.chat.id,
                                 f"Пользователь @{username} не присутствует в боте!"
                                 f"\n\n Его нельзя добавить в {listname}"
                                 f"...Напишите username еще раз!", reply_markup=key)

            else:
                dyn_memory(username, listname, result[1])
                key.add(telebot.types.InlineKeyboardButton("✅",
                                                           callback_data=f"addtolistsure"),
                        telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
                bot.send_message(message.chat.id,
                                 f"Пользователь '{result[1]}' присутствует в боте!\
                                 \n\n Хотите добавить его в {listname}?",
                                 reply_markup=key)
        bot.register_next_step_handler(message, editlist, listname)
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


def makeaquiz(message, quizname, button, templatetext, templatename):
    try:
        if quizname == '':
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="x"))
            bot.send_message(message.chat.id, f'Теперь напишите текст', reply_markup=key)
            bot.register_next_step_handler(message, makeaquiz, message.text, 0, '', '')
        else:
            if button == 0:

                conn = sqlite3.connect(f"{path}quiz.db")
                cursor = conn.cursor()
                cursor.execute(f"CREATE TABLE IF NOT EXISTS '{quizname}' (text text, '1' text, '2' text,"
                               f" '3' text, '4' text, '5' text, '6' text)")
                if templatetext == '':
                    cursor.execute(f"insert into '{quizname}' values ('{message.text}',"
                                   f" 'None', 'None', 'None', 'None', 'None', 'None')")
                    conn.commit()
                else:
                    cursor.execute(
                        f"insert into '{quizname}' values ('{templatetext}', 'None',"
                        f" 'None', 'None', 'None', 'None', 'None')")
                    conn.commit()
                    conn1 = sqlite3.connect(f"{path}templates.db")
                    cursor1 = conn1.cursor()
                    res = cursor1.execute(f"SELECT [11], [12], [13], [14], [15], [16]"
                                          f" FROM main WHERE name = '{templatename}'").fetchone()
                    conn1.close()
                    for x in range(len(res)):
                        if res[x] != 'None':
                            cursor.execute(f"UPDATE '{quizname}' SET '{str(x+1)}' = '{res[x]}'")
                            conn.commit()
                        else:
                            break
                cursor.execute(f"CREATE TABLE IF NOT EXISTS 'users{quizname}' (username text, value text)")
                conn.close()
                if templatetext == '':
                    bot.send_message(message.chat.id, f"Введите текст для кнопки 1")
                    bot.register_next_step_handler(message, makeaquiz, quizname, 1, '', '')
                else:
                    getquiz(message, quizname)
            else:
                conn = sqlite3.connect(f"{path}quiz.db")
                cursor = conn.cursor()
                cursor.execute(f"UPDATE '{quizname}' SET '{str(button)}' = '{message.text}'")
                conn.commit()
                conn.close()
                if button == 6:
                    bot.send_message(message.chat.id, "Опрос создан!")
                    admin(message)
                    return 0
                key = telebot.types.InlineKeyboardMarkup()
                key.add(telebot.types.InlineKeyboardButton("Закончить", callback_data=f"quiz{quizname}"))
                bot.send_message(message.chat.id, f"Введите текст для кнопки {str(button+1)}",
                                 reply_markup=key)
                bot.register_next_step_handler(message, makeaquiz, quizname, button + 1, '', '')
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        checkifuserindb(message)
        bot.send_message(message.chat.id, f"*Добро пожаловать в бота для рассылки!*", parse_mode="Markdown")

    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


def getquiz(message, quizname):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    conn = sqlite3.connect(f"{path}quiz.db")
    cursor = conn.cursor()
    quiz = cursor.execute(f"SELECT * FROM '{quizname}'").fetchone()
    users = cursor.execute(f"SELECT * FROM 'users{quizname}'").fetchall()
    conn.close()
    if len(quiz) == 0:
        bot.send_message(message.chat.id, f"Простите, опроса {quizname} не существует...")
        admin(message)
        return 1
    userstext = ''
    if len(users) == 0:
        userstext = 'Пока никто не проголосовал'
    else:
        for x in range(len(users)):
            conn = sqlite3.connect(f"{path}users.db")
            cursor = conn.cursor()
            name = cursor.execute(f"SELECT name FROM main WHERE username = '{users[x][0]}'").fetchone()[0]
            conn.close()

            userstext += f'{name} - {users[x][1]}\n'
    key = telebot.types.InlineKeyboardMarkup()
    key.add(telebot.types.InlineKeyboardButton(f'Удалить опрос',
                                               callback_data=f"deletequiz{quizname}"))
    key.add(telebot.types.InlineKeyboardButton("Разослать", callback_data=f"sendquiz{quizname}"))
    key.add(telebot.types.InlineKeyboardButton("Редактировать", callback_data=f"edtquiz{quizname}"))
    key.add(telebot.types.InlineKeyboardButton("❌", callback_data="showquiz"))
    bot.send_message(message.chat.id,
                     f"{quizname}\n\n{quiz[0]}\nПроголосовали:\n{userstext}",
                     reply_markup=key)


def editcalldata(message, name, data):
    # noinspection PyBroadException
    try:
        conn = sqlite3.connect(f"{path}templates.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE main SET '{data}' = '{message.text}' WHERE name = '{name}'")
        conn.commit()
        conn.close()
        key = telebot.types.InlineKeyboardMarkup()
        key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"tmpmake{name}"))
        bot.send_message(message.chat.id, f"Кнопка обновлена!",
                         reply_markup=key)
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


def editnamelist(message, listname, username):
    # noinspection PyBroadException
    try:
        if username == '':
            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            result = cursor.execute(f"SELECT * FROM '{listname}'").fetchall()
            if userinlist(result, message.text[1:]):
                key = telebot.types.InlineKeyboardMarkup()
                key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
                bot.send_message(message.chat.id, f"Напишите новое имя пользователя",
                                 reply_markup=key)
                conn.close()
                bot.register_next_step_handler(message, editnamelist, listname, message.text[1:])
            else:
                conn.close()
                bot.send_message(message.chat.id, f"Простите, такого пользователя в списке нет... ")
        else:
            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            result = cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'").fetchall()
            if len(result) == 0:
                pass
            else:
                for x in range(len(result)):
                    cursor.execute(f"UPDATE '{result[x][1]}' SET name = '{message.text}' WHERE username = '{username}'")
                    conn.commit()
            conn.close()
            conn = sqlite3.connect(f"{path}users.db")
            cursor = conn.cursor()
            cursor.execute(f"UPDATE main SET name = '{message.text}' WHERE username = '{username}'")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, f"Готово! Имя"
                                              f" успешно изменено на {message.text}!")
            showlist(message, listname)
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


def addbutton(message, name, number):
    if number == '':
        try:
            int(message.text)
        except Exception:
            bot.send_message(message.chat.id, f"Простите, но вы ввели не число, попробуйте еще раз")
            bot.register_next_step_handler(message, addbutton, name, '')
            return 1

        bot.send_message(message.chat.id, f"Теперь напишите значение для кнопки")
        bot.register_next_step_handler(message, addbutton, name, message.text)
    else:
        if int(number) > 6 or int(number) < 1:
            bot.send_message(message.chat.id, "Простите, но максимальное место это 6,"
                                              " минимальное - 1. Попробуйте еще раз ввести место.")
            bot.register_next_step_handler(message, addbutton, name, '')
            return 1
        conn = sqlite3.connect(f"{path}templates.db")
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT [11], [12], [13], [14], [15], [16] FROM main WHERE name = '{name}'").fetchone()
        z = 0
        for x in range(len(result)):
            if x == int(number) - 1:
                cursor.execute(f"UPDATE main SET '{str(x+11)}' = '{message.text}' WHERE name = '{name}'")
                conn.commit()
            elif x > int(number) - 1:
                cursor.execute(f"UPDATE main SET '{str(x+11)}' = '{z}' WHERE name = '{name}'")
                conn.commit()
            z = result[x]
        conn.close()
        showtmpedit(message, name)


# noinspection PyBroadException
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):

    if call.data[0:8] == 'editlist':
        try:
            conn = sqlite3.connect(f"{path}users.db")
            cursor = conn.cursor()
            r = cursor.execute(f"SELECT username, name FROM main").fetchall()
            conn.close()
            txt = ''
            for x in range(len(r)):
                txt += f"{r[x][1]} /{r[x][0]}\n"
            bot.send_message(call.message.chat.id, txt)
            listname = call.data[8:]
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
            bot.send_message(call.message.chat.id,
                             'Нажмите на того, кого хотите добавить или удалить из списка',
                             reply_markup=key)
            bot.register_next_step_handler(call.message, editlist, listname)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:12] == 'editnamelist':
        try:
            listname = call.data[12:]
            conn = sqlite3.connect(f"{path}users.db")
            cursor = conn.cursor()
            r = cursor.execute(f"SELECT username, name FROM main").fetchall()
            conn.close()
            txt = ''
            for x in range(len(r)):
                txt += f"{r[x][1]} /{r[x][0]}\n"
            bot.send_message(call.message.chat.id, txt)
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
            bot.send_message(call.message.chat.id, "Нажмите на человека, чтобы изменить его имя", reply_markup=key)
            bot.register_next_step_handler(call.message, editnamelist, listname, '')
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:4] == 'tous':
        # noinspection PyBroadException

            text = call.data.split(',')
            button = text[1]
            quizname = text[2]
            conn = sqlite3.connect(f"{path}quiz.db")
            cursor = conn.cursor()
            check = cursor.execute(
                f"SELECT username FROM 'users{quizname}' WHERE username = '{call.message.chat.id}'").fetchone()
            if check is None:
                bot.send_message(call.message.chat.id, "Извините но Вас нет в списке")
            else:
                cursor.execute(
                    f"UPDATE 'users{quizname}' SET value = '{button}' WHERE username = '{call.message.chat.id}'")
                conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, f"Спасибо за Ваш ответ!")


    elif call.data[0:9] == 'addbutton':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            name = call.data[9:]
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="Получить списки"))
            bot.send_message(call.message.chat.id,
                             f"Напишите, какая по счету должна быть кнопка", reply_markup=key)
            bot.register_next_step_handler(call.message, addbutton, name, '')
        except Exception as f:
            os.system(f"echo 704: {f} >> {path}logg.txt")
    else:
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    if call.data == 'Создать список':
        key = telebot.types.InlineKeyboardMarkup()
        key.add(telebot.types.InlineKeyboardButton("❌", callback_data="Получить списки"))
        bot.send_message(call.message.chat.id, 'Напишите название нового списка',
                         reply_markup=key)
        bot.register_next_step_handler(call.message, makealist)
    elif call.data == 'x':
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        admin(call.message)
    elif call.data == 'makealistsure':
        try:
            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS '{call.message.text}' (username text, name text)")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, f"Готово, список '{call.message.text}' успешно создан")
            showlist(call.message, call.message.text)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data == 'Получить списки':
        try:
            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            array = []
            result = cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'").fetchall()
            conn.close()

            for x in range(len(result)):
                array.append(result[x][1])
            key = telebot.types.InlineKeyboardMarkup()
            for x in array:
                key.add(telebot.types.InlineKeyboardButton(f"{x}",
                                                           callback_data=f"showlist{x}"))

            key.add(telebot.types.InlineKeyboardButton(f"Создать список",
                                                       callback_data=f"Создать список"))
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="x"))
            bot.send_message(call.message.chat.id, f"Ваши списки:",
                             reply_markup=key)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")

    elif call.data[0:13] == 'addtolistsure':

            text = getdyn_memory()
            username = text[0]
            listname = text[1]
            name = text[2]
            if listname == 'None':
                listname = call.data[13:]

            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            result = cursor.execute(f"SELECT username FROM '{listname}' WHERE username = '{username}'").fetchone()
            if result is not None:
                bot.send_message(call.message.chat.id, f"Простите, но пользователь {name}"
                                                       f" уже присутствует в списке '{listname}'")
                conn.close()
                admin(call.message)
                return 1
            cursor.execute(f"insert into '{listname}' values ('{username}', '{name}')")
            conn.commit()
            conn.close()
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
            bot.send_message(call.message.chat.id, f"Готово, пользователь {name}\
                             добавлен в список\nНапишите, кого хотите еще добавить в {listname}",
                             reply_markup=key)

    elif call.data[0:18] == 'deletefromlistsure':
        try:
            text = getdyn_memory()
            username = text[0]
            listname = text[1]
            name = text[2]
            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM '{listname}' WHERE username = '{username}'")
            conn.commit()
            conn.close()
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
            bot.send_message(call.message.chat.id, f"Готово, пользователь {name}\
                             удален из списка\nНапишите, кого хотите еще удалить из {listname}",
                             reply_markup=key)

        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:10] == 'deletelist':
        try:
            listname = call.data[10:]
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton(f"✅",
                                                       callback_data=f"suredeletelist{listname}"),
                    telebot.types.InlineKeyboardButton("❌", callback_data=f"showlist{listname}"))
            bot.send_message(call.message.chat.id, f"Вы действительно хотите удалить список '{listname}'?",
                             reply_markup=key)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:14] == 'suredeletelist':
        try:
            listname = call.data[14:]
            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE '{listname}'")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, f"Список '{listname}' успешно удален!")
            admin(call.message)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data == 'Сделать опрос':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("Создать из шабл.", callback_data="templatequizmake"))
            key.add(telebot.types.InlineKeyboardButton("Создать шаблон", callback_data="maketemplate"))
            key.add(telebot.types.InlineKeyboardButton("Создать опрос", callback_data="makeaquiz"))
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="x"))

            bot.send_message(call.message.chat.id, f"Выберите, что хотите сделать",
                             reply_markup=key)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data == 'makeaquiz':
        bot.send_message(call.message.chat.id, "Введите название опроса")
        bot.register_next_step_handler(call.message, makeaquiz, '', 0, '', '')
    elif call.data[0:10] == 'deletequiz':
        try:
            quizname = call.data[10:]

            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("Удалить", callback_data=f"suredeletequiz{quizname}"))
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="x"))
            bot.send_message(call.message.chat.id, f"Вы действительно хотите "
                                                   f"удалить опрос '{quizname}'?",
                             reply_markup=key)

        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:14] == 'suredeletequiz':
        try:
            quizname = call.data[14:]
            conn = sqlite3.connect(f"{path}quiz.db")
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE IF EXISTS '{quizname}'")
            conn.commit()
            cursor.execute(f"DROP TABLE IF EXISTS 'users{quizname}'")
            conn.commit()
            conn.close()
            bot.send_message(call.message.chat.id, f"Опрос '{quizname}' успешно удален!")
            admin(call.message)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data == 'showquiz':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            conn = sqlite3.connect(f"{path}quiz.db")
            cursor = conn.cursor()
            array = []
            result = cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'").fetchall()
            conn.close()
            if len(result) == 0:
                admin(call.message)
                return 1
            for x in range(len(result)):
                array.append(result[x][1])
            key = telebot.types.InlineKeyboardMarkup()

            for x in array:
                if x[0:4] != 'user':
                    key.add(telebot.types.InlineKeyboardButton(f"{x}",
                                                               callback_data=f"quiz{x}"))
                else:
                    pass

            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="x"))
            bot.send_message(call.message.chat.id, f"Ваши опросы:",
                             reply_markup=key)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:4] == 'quiz':
        getquiz(call.message, call.data[4:])

    elif call.data[0:8] == 'calldata':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            text = call.data.split(',')
            name = text[1]
            data = text[2]
            bot.send_message(call.message.chat.id, f"Напишите новое значение для кнопки")
            bot.register_next_step_handler(call.message, editcalldata, name, data)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")

    elif call.data[0:8] == 'showlist':
        showlist(call.message, call.data[8:])
    elif call.data == 'maketemplate':
        try:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="Сделать опрос"))
            bot.send_message(call.message.chat.id, "Введите название шаблона",
                             reply_markup=key)
            bot.register_next_step_handler(call.message, maketemplate, '', 0)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:15] == 'buttonstemplate':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            name = call.data[15:]
            bot.send_message(call.message.chat.id, "Теперь введите значение для 1 кнопки:")
            bot.register_next_step_handler(call.message, buttonstemplate, name, 11)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data == 'templatequizmake':
        try:
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
            conn = sqlite3.connect(f"{path}templates.db")
            cursor = conn.cursor()
            result = cursor.execute(f"SELECT name FROM main").fetchall()
            conn.close()
            if len(result) == 0:
                admin(call.message)
                return 1

            key = telebot.types.InlineKeyboardMarkup()

            for x in result:
                key.add(telebot.types.InlineKeyboardButton(f"{x[0]}",
                                                           callback_data=f"tmpmake{x[0]}"))
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="Сделать опрос"))
            bot.send_message(call.message.chat.id, f"Ваши шаблоны:",
                             reply_markup=key)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:7] == 'tmpmake':
        try:
            name = call.data[7:]
            conn = sqlite3.connect(f"{path}templates.db")
            cursor = conn.cursor()
            result = cursor.execute(f"SELECT * FROM main WHERE name = '{name}'").fetchone()
            conn.close()
            text = ''
            key = telebot.types.InlineKeyboardMarkup()
            for x in range(len(result)):

                if result[x] == 'None':
                    continue
                else:
                    if x == 0:
                        text += f"*{result[x]}*\n\n"
                    elif x < 10:
                        text += f"*{result[x]} - ...*\n"
                    else:
                        pass
            key.add(telebot.types.InlineKeyboardButton("Создать опрос из шаблона", callback_data=f"fulltemplate{name}"))
            key.add(telebot.types.InlineKeyboardButton("Редактировать шаблон", callback_data=f"tmpedit{name}"))
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="Сделать опрос"))
            bot.send_message(call.message.chat.id, f"Ваш шаблон выглядит так:\n\n{text}", reply_markup=key)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:7] == 'tmpedit':
        name = call.data[7:]
        showtmpedit(call.message, name)
    elif call.data[0:12] == 'fulltemplate':

        fulltemplate(call.message, call.data[12:], 1, '', '')
    elif call.data[0:8] == 'sendquiz':
        try:
            quizname = call.data[8:]

            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            array = []
            result = cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'").fetchall()
            conn.close()
            if len(result) == 0:
                admin(call.message)
                return 1
            for x in range(len(result)):
                array.append(result[x][1])
            key = telebot.types.InlineKeyboardMarkup()

            for x in array:
                key.add(telebot.types.InlineKeyboardButton(f"{x}",
                                                           callback_data=f"srs,{x},{quizname}"))
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="x"))
            bot.send_message(call.message.chat.id, f"Выберете список:",
                             reply_markup=key)

        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data[0:3] == 'srs':

        text = call.data.split(',')
        listname = text[1]
        quizname = text[2]
        conn = sqlite3.connect(f"{path}lists.db")
        cursor = conn.cursor()
        listnames = cursor.execute(f"SELECT username, name FROM '{listname}'").fetchall()
        conn.close()
        if len(listnames) == 0:
            bot.send_message(call.message.chat.id, "Извините, список пустой")
            return 1

        conn = sqlite3.connect(f"{path}quiz.db")
        cursor = conn.cursor()
        quizinfo = cursor.execute(f"SELECT * FROM '{quizname}'").fetchone()
        conn.close()
        info = ''
        for x in range(len(listnames)):
            conn = sqlite3.connect(f"{path}users.db")
            cursor = conn.cursor()
            chat_id = cursor.execute(f"SELECT chat_id FROM main WHERE username = '{listnames[x][0]}'").fetchone()[0]
            conn.close()
            conn = sqlite3.connect(f"{path}quiz.db")
            cursor = conn.cursor()
            check = cursor.execute(f"SELECT username FROM 'users{quizname}' WHERE username = '{listnames[x][0]}'").fetchone()
            if check is None:
                cursor.execute(f"insert into 'users{quizname}' values ('{listnames[x][0]}', 'Игнор')")
            else:
                pass
            conn.commit()
            conn.close()
            quiztext = quizinfo[0]
            key = telebot.types.InlineKeyboardMarkup()
            for y in range(len(quizinfo)):
                if quizinfo[y] == 'None':
                    continue
                else:
                    if y == 0:
                        continue
                    else:
                        key.add(telebot.types.InlineKeyboardButton(f"{quizinfo[y]}",
                                                                   callback_data=f"tous,{quizinfo[y]},{quizname}"))
            try:
                bot.send_message(int(chat_id), quiztext, reply_markup=key)
                info += f'{listnames[x][1]} - Получил опрос\n'
            except Exception:
                info += f'{listnames[x][1]} - Не удалось отправить\n'
        for x in admin_id:
            bot.send_message(int(x), info)
        admin(call.message)


    elif call.data == 'stat':
        try:
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("Общая стат.", callback_data=f"Общая стат."))
            key.add(telebot.types.InlineKeyboardButton("Стат. пользователя", callback_data=f"usersstat"))
            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="x"))
            bot.send_message(call.message.chat.id, "Выберите, что хотите посмотреть", reply_markup=key)
        except Exception as f:
            os.system(f"echo {f} >> {path}logg.txt")
    elif call.data == 'Общая стат.':
        conn = sqlite3.connect(f"{path}quiz.db")
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'").fetchall()

        array = []
        if len(result) == 0:
            bot.send_message(call.message.chat.id, "Нет опросов, чтобы отобразить статистику")
            admin(call.message)
            return 1
        for x in range(len(result)):
            if result[x][1][0:5] == 'users':
                array.append(result[x][1])
            else:
                continue
        wb = xlwt.Workbook()
        z = 0
        ws = wb.add_sheet(f'Статистика')
        #ws = wb.add_sheet(f'{x[5:]}')
        for x in array:
            ws.write(z, 0, f"{x[5:]}")
            z+=1
            result = cursor.execute(f"SELECT * FROM '{x}'").fetchall()

            for y in range(len(result)):
                z+=1
                conn1 = sqlite3.connect(f"{path}users.db")
                cursor1 = conn1.cursor()
                name = cursor1.execute(f"SELECT name FROM main WHERE username = '{result[y][0]}'").fetchone()
                conn1.close()
                ws.write(z, 0, name)
                ws.write(z, 1, result[y][1])
            z += 2




        wb.save(f'{path}table.xls')
        conn.close()
        with open(f"{path}table.xls", 'rb') as f:
            bot.send_document(call.message.chat.id, f)
        admin(call.message)
    elif call.data == 'usersstat':
        try:
            conn = sqlite3.connect(f"{path}users.db")
            cursor = conn.cursor()
            result = cursor.execute("SELECT username, name FROM main").fetchall()
            conn.close()
            text = ''
            for x in range(len(result)):
                text += f'{result[x][1]} /{result[x][0]}\n'
            bot.send_message(call.message.chat.id, f"Нажмите на имя:\n{text}")
            bot.register_next_step_handler(call.message, usersstat)
        except Exception as f:
            os.system(f"echo 704: {f} >> {path}logg.txt")
    elif call.data[0:4] == 'phil':
        try:
            conn = sqlite3.connect(f"{path}lists.db")
            cursor = conn.cursor()
            array = []
            result = cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'").fetchall()
            conn.close()

            for x in range(len(result)):
                array.append(result[x][1])
            key = telebot.types.InlineKeyboardMarkup()
            for x in array:
                key.add(telebot.types.InlineKeyboardButton(f"{x}",
                                                           callback_data=f"addtolistsure{x}"))

            key.add(telebot.types.InlineKeyboardButton("❌", callback_data="x"))
            bot.send_message(call.message.chat.id, f"Ваши списки:",
                             reply_markup=key)
        except Exception as f:
            os.system(f"echo 704: {f} >> {path}logg.txt")
    elif call.data[0:7] == 'edtquiz':
        try:
            quizname = call.data[7:]
            conn = sqlite3.connect(f"{path}quiz.db")
            cursor = conn.cursor()
            text = cursor.execute(f"SELECT text FROM '{quizname}'").fetchone()
            conn.close()
            if text is None:
                bot.send_message(call.message.chat.id, "Произошла ошибка")
            else:
                key = telebot.types.InlineKeyboardMarkup()
                key.add(telebot.types.InlineKeyboardButton("❌", callback_data="showquiz"))
                bot.send_message(call.message.chat.id, f"Напишите новый текст!", reply_markup=key)
                bot.send_message(call.message.chat.id, f"{text[0]}")
                bot.register_next_step_handler(call.message, edtquiz, quizname)
        except Exception as f:
            os.system(f"echo 704: {f} >> {path}logg.txt")


def edtquiz(message, quizname):
    try:
        conn = sqlite3.connect(f"{path}quiz.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE '{quizname}' SET text = '{message.text}'")
        conn.commit()
        conn.close()
        getquiz(message, quizname)
    except Exception as f:
        os.system(f"echo 704: {f} >> {path}logg.txt")


def usersstat(message):
    try:
        conn = sqlite3.connect(f"{path}quiz.db")
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM sqlite_master WHERE type='table'").fetchall()
        username = message.text[1:]
        array = []
        if len(result) == 0:
            bot.send_message(message.chat.id, "Нет опросов, чтобы отобразить статистику")
            admin(message)
            return 1
        for x in range(len(result)):
            if result[x][1][0:5] == 'users':
                array.append(result[x][1])
            else:
                continue
        wb = xlwt.Workbook()
        ws = wb.add_sheet(f'Статистика')
        z = 1
        conn1 = sqlite3.connect(f"{path}users.db")
        cursor1 = conn1.cursor()
        name = cursor1.execute(f"SELECT name FROM main WHERE username = '{username}'").fetchone()
        conn1.close()
        ws.write(0, 0, f"{name[0]}")
        for x in array:
            ws.write(z, 0, f"{x[5:]}")
            result = cursor.execute(f"SELECT * FROM '{x}' WHERE username = '{username}'").fetchone()

            if result is None:
                z += 1
                continue
            else:
                z += 1
                ws.write(z, 0, name[0])
                ws.write(z, 1, result[1])
            z += 1
        wb.save(f'{path}table.xls')
        conn.close()
        with open(f"{path}table.xls", 'rb') as f:
            bot.send_document(message.chat.id, f)
        admin(message)
    except Exception as f:
        os.system(f"echo 704: {f} >> {path}logg.txt")


def fulltemplate(message, name, x, text, quizname):
    # noinspection PyBroadException
    try:
        if quizname == '' and x == 1:
            bot.send_message(message.chat.id, "Для начала напишите название опроса")
            bot.register_next_step_handler(message, fulltemplate, name, 1, '', 's')
            return 1
        elif quizname != '' and x == 1:
            quizname = message.text
        conn = sqlite3.connect(f"{path}templates.db")
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT [{str(x)}] FROM main WHERE name = '{name}'").fetchone()
        conn.close()
        if x == 1:
            bot.send_message(message.chat.id, f"Введите значение для '{result[0]}'")
            bot.register_next_step_handler(message, fulltemplate, name, x + 1, text + f"{result[0]}:", quizname)
        else:
            text += f" {message.text}\n"
            if result[0] == 'None':
                makeaquiz(message, quizname, 0, text, name)
                return 0
            bot.send_message(message.chat.id, f"Введите значение для '{result[0]}'")
            bot.register_next_step_handler(message, fulltemplate, name, x + 1, text + f"{result[0]}:", quizname)

    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


# noinspection PyBroadException
def tmpedit(message, name, info):
    try:
        if info == '':
            bot.send_message(message.chat.id, "Теперь напишите новое значение!")
            bot.register_next_step_handler(message, tmpedit, name, message.text)
        else:
            conn = sqlite3.connect(f"{path}templates.db")
            cursor = conn.cursor()
            key = telebot.types.InlineKeyboardMarkup()
            if info[1:] == 'name':
                cursor.execute(f"UPDATE main SET name = '{message.text}' WHERE name = '{name}'")
                conn.commit()
                key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"tmpmake{message.text}"))
            else:
                cursor.execute(f"UPDATE main SET '{info[1:]}' = '{message.text}' WHERE name = '{name}'")
                conn.commit()
                key.add(telebot.types.InlineKeyboardButton("❌", callback_data=f"tmpedit{name}"))
            conn.close()
            bot.send_message(message.chat.id, "Готово!", reply_markup=key)
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


# noinspection PyBroadException
def buttonstemplate(message, name, button):
    try:
        conn = sqlite3.connect(f"{path}templates.db")
        cursor = conn.cursor()
        cursor.execute(f"UPDATE main SET '{str(button)}' = '{message.text}' WHERE name = '{name}'")
        conn.commit()
        conn.close()
        key = telebot.types.InlineKeyboardMarkup()
        key.add(telebot.types.InlineKeyboardButton("Закончить", callback_data=f"Сделать опрос"))
        bot.send_message(message.chat.id, f"Напишите значение для  {str(button-9)} кнопки:", reply_markup=key)
        bot.register_next_step_handler(message, buttonstemplate, name, button + 1)
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


def maketemplate(message, name, number):
    # noinspection PyBroadException
    try:
        if number == 0:
            conn = sqlite3.connect(f"{path}templates.db")
            cursor = conn.cursor()
            cursor.execute(f"insert into main values ('{message.text}', 'None', 'None', 'None', 'None',"
                           f" 'None', 'None', 'None', 'None', 'None',"
                           f" 'None', 'None', 'None', 'None', 'None', 'None', 'None')")
            conn.commit()
            conn.close()
            bot.send_message(message.chat.id, f"Шаблон {message.text} создан!")
            bot.send_message(message.chat.id, f"Напишите {str(number+1)} нередактируемое поле:")
            bot.register_next_step_handler(message, maketemplate, message.text, 1)
        else:
            conn = sqlite3.connect(f"{path}templates.db")
            cursor = conn.cursor()
            cursor.execute(f"UPDATE main SET '{str(number)}' = '{message.text}' WHERE name = '{name}'")
            conn.commit()
            conn.close()
            if number == 10:
                bot.send_message(message.chat.id, "Теперь введите значение для 1 кнопки:")
                bot.register_next_step_handler(message, buttonstemplate, name, 11)
                return 0
            key = telebot.types.InlineKeyboardMarkup()
            key.add(telebot.types.InlineKeyboardButton("Закончить", callback_data=f"buttonstemplate{name}"))
            bot.send_message(message.chat.id, f"Напишите {str(number+1)} нередактируемое поле:", reply_markup=key)
            bot.register_next_step_handler(message, maketemplate, name, number + 1)
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


# noinspection PyBroadException
def showlist(message, listname):
    try:
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        conn = sqlite3.connect(f"{path}lists.db")
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM '{listname}'").fetchall()
        conn.close()
        text = ''
        if len(result) != 0:
            for y in range(len(result)):
                text += f'{result[y][1]}\n'
        else:
            pass
        key = telebot.types.InlineKeyboardMarkup()
        key.add(telebot.types.InlineKeyboardButton("Редактировать список",
                                                   callback_data=f"editlist{listname}"),
                telebot.types.InlineKeyboardButton("Переим. людей", callback_data=f"editnamelist{listname}"))
        key.add(telebot.types.InlineKeyboardButton("Удалить список",
                                                   callback_data=f"deletelist{listname}"),
                telebot.types.InlineKeyboardButton("❌", callback_data="Получить списки"))
        bot.send_message(message.chat.id, f"{listname}\n\n{text}", reply_markup=key)

    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


def showtmpedit(message, name):
    try:
        text = ''
        conn = sqlite3.connect(f"{path}templates.db")
        cursor = conn.cursor()
        result = cursor.execute(f"SELECT * FROM main WHERE name = '{name}'").fetchone()
        conn.close()
        key = telebot.types.InlineKeyboardMarkup()
        for x in range(len(result)):
            if result[x] == 'None':
                continue
            else:
                if x == 0:
                    text += f"/name *{result[x]}*\n\n"
                elif x < 10:
                    text += f"/{str(x)} *{result[x]} - ...*\n"
                else:
                    key.add(telebot.types.InlineKeyboardButton(f"{result[x]}",
                                                               callback_data=f"calldata,{name},{str(x)}"))
        key.add(telebot.types.InlineKeyboardButton("Добавить кнопку", callback_data=f"addbutton{name}"))
        key.add(telebot.types.InlineKeyboardButton("❌", callback_data="Сделать опрос"))
        bot.send_message(message.chat.id, f"Нажмите на то, что хотите изменить:\n\n{text}",
                         reply_markup=key)
        bot.register_next_step_handler(message, tmpedit, name, '')
    except Exception as f:
        os.system(f"echo {f} >> {path}logg.txt")


# noinspection PyBroadException
def polling():
    # noinspection PyBroadException
    try:
        bot.polling(timeout=2)
    except Exception:
        os.system(f"echo 123 >> {path}except.txt")


if __name__ == "__main__":
    polling()
