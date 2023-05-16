import telebot, requests

bad_dict = ['хуй', 'пизд', 'залупа', 'хуев', 'хуёв', 'бляд', 'блят', 'ебать', 'ёбан', 'ебля', 'впиздячил', 'выблядок',
            'выебон', 'выебывается', 'выёбывается', 'доеба', 'доёба', 'ебал', 'ебан', 'ёбан', 'заебись', 'наеб', 'наёб',
            'подъеб', 'подъёб', 'пидр', 'пидор', 'бля']
checker1 = [5]
checker2 = [5]
checker3=[5]
bot = telebot.TeleBot("536521259:AAHQ_JNcZ_dssj4OibHudoOjpPNpiQL3upE")


def point(event, context):
    print(event)
    if checker1[0] == 1 and event['message']['chat']['id'] == 331253447:
        try:
            message_id = event['message']['message_id']
            bot.unpin_chat_message(-1001358737422)

            hh = bot.forward_message(-1001358737422, 331253447, message_id)
            pin = hh.message_id
            bot.pin_chat_message(-1001358737422, pin)
            bot.send_message(331253447, 'Все хорошо')
            checker1.pop(0)
            checker1.append(5)
        except Exception as f:
            bot.send_message(232673077, str(f))
    elif checker2[0] == 1 and event['message']['chat']['id'] == 331253447:
        try:
            message_id = event['message']['message_id']
            bot.unpin_chat_message(-1001188423732)

            hh = bot.forward_message(-1001188423732, 331253447, message_id)
            pin = hh.message_id
            bot.pin_chat_message(-1001188423732, pin)
            bot.send_message(331253447, 'Все хорошо')
            checker2.pop(0)
            checker2.append(5)
        except Exception as f:
            bot.send_message(232673077, str(f))
    elif checker3[0] == 1 and event['message']['chat']['id'] == 331253447:
        try:
            message_id = event['message']['message_id']
            bot.unpin_chat_message(-1001237358444)

            hh = bot.forward_message(-1001237358444, 331253447, message_id)
            pin = hh.message_id
            bot.pin_chat_message(-1001237358444, pin)
            bot.send_message(331253447, 'Все хорошо')
            checker3.pop(0)
            checker3.append(5)
        except Exception as f:
            bot.send_message(232673077, str(f))
    else:
        if event['message']['chat']['type'] == 'group' or event['message']['chat']['type'] == 'supergroup':
            group(event)
        elif event['message']['chat']['type'] == 'private':
            private(event)
        else:
            pass


def group(event):
    if 'new_chat_member' in event['message']:
        try:
            chat_id = event['message']['chat']['id']
            greeting = bot.get_chat(-1001358737422).pinned_message.text

            if chat_id != -1001358737422 and chat_id != 1001188423732:
                bot.send_message(chat_id, greeting + ' ' + event['message']['new_chat_member']['first_name'])
        except Exception as f:
            bot.send_message(232673077, str(f))
    elif 'left_chat_member' in event['message']:
        try:
            chat_id = event['message']['chat']['id']
            greeting = bot.get_chat(-1001188423732).pinned_message.text

            if chat_id != -1001358737422 and chat_id != 1001188423732:
                bot.send_message(chat_id, greeting + ' ' + event['message']['left_chat_member']['first_name'])
        except Exception as f:
            bot.send_message(232673077, str(f))

    message = event['message']['text']
    chat_id = event['message']['chat']['id']

    message = message.lower()
    lenn = len(message)
    for x in bad_dict:
        y = message.find(x, 0, lenn)
        if y != -1:
            bot.send_message(chat_id, 'Не ругайся, ' + event['message']['from']['first_name'])
            break
    chatid=event['message']['from']['id']
    if chatid==331253447:
        hhf = bot.get_chat(-1001237358444).pinned_message.text
        if message.startswith(hhf)==True:
            bot.send_message(chat_id,'Внимание, важная информация⬆️')

def private(event):
    if event['message']['chat']['id'] == 331253447:
        message = event['message']['text']
        if message == '/start':
            bot.send_message(331253447, 'Привет админ, я чат бот.')
        elif message == '/settext':
            if checker1[0] == 1:
                checker1.pop(0)
                checker1.append(1)
                bot.send_message(331253447, 'Теперь напишите сообщение')
            else:
                checker1.pop(0)
                checker1.append(1)
                bot.send_message(331253447, 'Теперь напишите сообщение')
        elif message == '/goodbye':
            if checker2[0] == 1:
                checker2.pop(0)
                checker2.append(1)
                bot.send_message(331253447, 'Теперь напишите сообщение')
            else:
                checker2.pop(0)
                checker2.append(1)
                bot.send_message(331253447, 'Теперь напишите сообщение')

        elif message == '/help':
            help_message()
        elif message == '/what':
            try:
                hhf = bot.get_chat(-1001358737422).pinned_message.text

                bot.send_message(331253447, hhf)

            except Exception as f:
                bot.send_message(232673077, str(f))
        elif message == '/quit':
            hhf = bot.get_chat(-1001188423732).pinned_message.text

            bot.send_message(331253447, hhf)
        elif message=='/settextwanted':
            if checker3[0] == 1:
                checker3.pop(0)
                checker3.append(1)
                bot.send_message(331253447, 'Теперь напишите сообщение')
            else:
                checker3.pop(0)
                checker3.append(1)
                bot.send_message(331253447, 'Теперь напишите сообщение')
        elif message=='/wanted':
            hhf = bot.get_chat(-1001237358444).pinned_message.text

            bot.send_message(331253447, hhf)
        else:

            bot.send_message(331253447, 'Простите, я вас не понимаю, босс.')
    else:
        message = event['message']['text']
        chat_id = event['message']['chat']['id']
        if message == '/start':
            bot.send_message(chat_id, 'Не вижу смысла тебе здесь находиться.')
        else:
            bot.send_message(chat_id, 'Ты что-то хотел? Я просто бот, я не собираюсь с тобой разговаривать.')


def help_message():
    bot.send_message(331253447,
                     '/settext - Указываете приветствие при новом пользователе.(username стоит в конце по умолчанию)\n/goodbye - Указываете прощание при уходе пользователя.(username стоит в конце по умолчанию)\n/help - Помощь.\n/what - Показать текст приветствия.\n/quit - Показать текст прощания.\n/settextwanted - Установка кодового слова, чтобы бот посоветовал обратить внимание.\n/wanted - просмотр кодового слова.')


'''
def start_request():
    url="https://api.telegram.org/bot{token}/{method}".format(
        token="540702570:AAGfGleOhSxzewf4GWRyH1FUOqaSmDwmONo",
        method="setWebhook"
    )
    data={
        "url":"https://g4v7c4ag97.execute-api.us-east-2.amazonaws.com/v0/group-bot12345iggy228"
    }
    r=requests.post(url,data=data)
    print(r.json())
if __name__=="__main__":
    start_request()
'''