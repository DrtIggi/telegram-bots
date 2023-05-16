
password on server — ReCRwsweA1!d






import cherrypy
import telebot
import logging


API_TOKEN = '428512177:AAHhDKYnP5SzNmfGXQM04kC6uKVKNmIsuDg'

WEBHOOK_HOST = 'ovz1.9153378047.6el81.vps.myjino.ru'
WEBHOOK_PORT = 	8443 # 443, 80, 88 or 8443 (port need to be 'open')
# In some VPS you may need to put here the IP addr
WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


bot=telebot.TeleBot(API_TOKEN)


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
           'content-type' in cherrypy.request.headers and \
           cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)




@bot.message_handler(commands=['help'])

def help(message):
   sent= bot.send_message(message.chat.id,'Все что от Вас требуется это нажать /start и мы сделаем Вам бота☺️.')


   bot.register_next_step_handler(sent, help_for)

def help_for(message):
    if message.text == '/start':
        message.text='start'
    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            sent=bot.send_message(message.chat.id,'Нажмите /start, чтобы создать бота.')
            bot.register_next_step_handler(sent, help_for)
        else:
            sent = bot.send_message(message.chat.id, 'Я тебя не понимаю😅')
            bot.register_next_step_handler(sent, help_for)
def community(message):
    if message.text == '/start':
        message.text='start'

    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            sent=bot.send_message(message.chat.id,title+', теперь расскажите о том, какой бот вам нужен. Опишите его и добавьте номер телефона(для связи с Вами).')
            bot.register_next_step_handler(sent, community2)
        else:
            sent=bot.send_message(message.chat.id,'Это не может быть именем.')
            bot.register_next_step_handler(sent, community)


def community2(message):
    if message.text == '/start':
        message.text='start'
    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            bot.send_message(232673077,title)
            sent=bot.send_message(message.chat.id,'Спасибо, мы рассмотрим Вашу заявку💪.Наш консультант скоро с Вами свяжется.Если хотите оформить новую заявку, нажмите /start.')
        else:
            sent=bot.send_message(message.chat.id,'Вам нужно описать бота.')
            bot.register_next_step_handler(sent, community2)

bot.remove_webhook()

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH
                )

# Disable CherryPy requests log
access_log = cherrypy.log.access_log
for handler in tuple(access_log.handlers):
    access_log.removeHandler(handler)

# Start cherrypy server
cherrypy.config.update({
    
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})



cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})




@bot.message_handler(commands=['start'])

def start(message):
   sent= bot.send_message(message.chat.id,'Здравствуйте, я консультант по разработке ботов😁. Как Вас зовут?')


   bot.register_next_step_handler(sent, community)


@bot.message_handler(commands=['help'])

def help(message):
   sent= bot.send_message(message.chat.id,'Все что от Вас требуется это нажать /start и мы сделаем Вам бота☺️.')


   bot.register_next_step_handler(sent, help_for)

def help_for(message):
    if message.text == '/start':
        message.text='start'
    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            sent=bot.send_message(message.chat.id,'Нажмите /start, чтобы создать бота.')
            bot.register_next_step_handler(sent, help_for)
        else:
            sent = bot.send_message(message.chat.id, 'Я тебя не понимаю😅')
            bot.register_next_step_handler(sent, help_for)
def community(message):
    if message.text == '/start':
        message.text='start'

    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            sent=bot.send_message(message.chat.id,title+', теперь расскажите о том, какой бот вам нужен. Опишите его и добавьте номер телефона(для связи с Вами).')
            bot.register_next_step_handler(sent, community2)
        else:
            sent=bot.send_message(message.chat.id,'Это не может быть именем.')
            bot.register_next_step_handler(sent, community)


def community2(message):
    if message.text == '/start':
        message.text='start'
    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            bot.send_message(232673077,title)
            sent=bot.send_message(message.chat.id,'Спасибо, мы рассмотрим Вашу заявку💪.Наш консультант скоро с Вами свяжется.Если хотите оформить новую заявку, нажмите /start.')
        else:
            sent=bot.send_message(message.chat.id,'Вам нужно описать бота.')
            bot.register_next_step_handler(sent, community2)


bot.polling(none_stop=True)



import requests
import telebot


import requests
import telebot


def point(event, context):
    print(event)
    bot = telebot.TeleBot("406036597:AAGVNB0mo8ozT1nzNgf0wa1DdPEt_KYzPJQ")
    chat_id=event['message']['from']['id']
    message=event['message']['text']
    
    user_markup=telebot.types.ReplyKeyboardMarkup()
    user_markup.row('/start','не жми это')

    if message == '/start':
        bot.send_message(chat_id,'Добро пожаловать, Нео...',reply_markup=user_markup)
    else:
        lol=event(-1)
        if lol['message']['text']=='Добро пожаловать, Нео...':
            bot.send_message(chat_id,'Ты не пройдешь!!!')


def send_message(chat_id, text):
    url = "https://api.telegram.org/bot{token}/{method}".format(
        token="406036597:AAGVNB0mo8ozT1nzNgf0wa1DdPEt_KYzPJQ",
        method="sendMessage"
    )
    data = {
        "chat_id": chat_id,
        "text": text
    }
    r = requests.post(url, data=data)
    print(r.json())




"""
     def start_function():
         newmessag=messag
         if newmessag == "/start":
             bot.send_message(chat_id, 'hello')




def start_request():
    url="https://api.telegram.org/bot{token}/{method}".format(
        token="406036597:AAGVNB0mo8ozT1nzNgf0wa1DdPEt_KYzPJQ",
        method="setWebhook"
    )
    data={
        "url":"https://czt66gpe29.execute-api.eu-west-2.amazonaws.com/v0/bot_handler_for_Ignat"
    }
    r=requests.post(url,data=data)
    print(r.json())
if __name__=="__main__":
    start_request()
"""



token='433821833:AAHpQIFETF6aS491PBc84IZbQB4V9T3YeUc'


bot=telebot.TeleBot(token)




def point(event,context):
    print('hello')
def start_request():
    url='https://api.telegram.org/bot{token}/{method}'.format(
        token='433821833:AAHpQIFETF6aS491PBc84IZbQB4V9T3YeUc',
        method="setWebhook"
    )
    data={
        "url":"https://o8xr9swe0j.execute-api.eu-west-2.amazonaws.com/v0/bot_daun_handler"
    }
    r=requests.post(url,data=data)
    print(r.json())
def start(message):
   sent= bot.send_message(message.chat.id,'Здравствуйте, я консультант по разработке ботов😁. Как Вас зовут?')


   bot.register_next_step_handler(sent, community)


@bot.message_handler(commands=['help'])

def help(message):
   sent= bot.send_message(message.chat.id,'Все что от Вас требуется это нажать /start и мы сделаем Вам бота☺️.')


   bot.register_next_step_handler(sent, help_for)

def help_for(message):
    if message.text == '/start':
        message.text='start'
    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            sent=bot.send_message(message.chat.id,'Нажмите /start, чтобы создать бота.')
            bot.register_next_step_handler(sent, help_for)
        else:
            sent = bot.send_message(message.chat.id, 'Я тебя не понимаю😅')
            bot.register_next_step_handler(sent, help_for)
def community(message):
    if message.text == '/start':
        message.text='start'

    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            sent=bot.send_message(message.chat.id,title+', теперь расскажите о том, какой бот вам нужен. Опишите его и добавьте номер телефона(для связи с Вами).')
            bot.register_next_step_handler(sent, community2)
        else:
            sent=bot.send_message(message.chat.id,'Это не может быть именем.')
            bot.register_next_step_handler(sent, community)


def community2(message):
    if message.text == '/start':
        message.text='start'
    elif message.text == '/help':
        message.text='help'
    else:
        title=message.text
        if title:
            bot.send_message(232673077,title)
            sent=bot.send_message(message.chat.id,'Спасибо, мы рассмотрим Вашу заявку💪.Наш консультант скоро с Вами свяжется.Если хотите оформить новую заявку, нажмите /start.')
        else:
            sent=bot.send_message(message.chat.id,'Вам нужно описать бота.')
            bot.register_next_step_handler(sent, community2)

if __name__=="__main__":
    bot.polling()



—————————
import requests
import telebot
bot = telebot.TeleBot("406036597:AAGVNB0mo8ozT1nzNgf0wa1DdPEt_KYzPJQ")
def point(event,comments):

    message = event['message']['text']
    if message=='/start':
        send_start(event,comments)
    else:
       community(event,comments)
    print(event)



def send_start(ivent,comments):

    chat_id = ivent['message']['from']['id']
    message = ivent['message']['text']

    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', 'Реклама')



    bot.send_message(chat_id,'Добро пожаловать, Нео..., как тебя зовут', reply_markup=user_markup)




def community(ivent,comments):
    answer='Ты даун'
    chat_id = ivent['message']['from']['id']
    message = ivent['message']['text']
    if message=="Реклама":
        bot.send_message(chat_id,answer+message)
    else:

        bot.send_message(chat_id,"ок")

def send_message(chat_id, text):
    url = "https://api.telegram.org/bot{token}/{method}".format(
        token="406036597:AAGVNB0mo8ozT1nzNgf0wa1DdPEt_KYzPJQ",
        method="sendMessage"
    )
    data = {
        "chat_id": chat_id,
        "text": text


    }

    r = requests.post(url, data=data)
    print(r.json())


"""
     def start_function():
         newmessag=messag
         if newmessag == "/start":
             bot.send_message(chat_id, 'hello')




def start_request():
    url="https://api.telegram.org/bot{token}/{method}".format(
        token="406036597:AAGVNB0mo8ozT1nzNgf0wa1DdPEt_KYzPJQ",
        method="setWebhook"
    )
    data={
        "url":"https://czt66gpe29.execute-api.eu-west-2.amazonaws.com/v0/bot_handler_for_Ignat"
    }
    r=requests.post(url,data=data)
    print(r.json())
if __name__=="__main__":
    start_request()
"""
