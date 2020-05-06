from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai
import json
import os
import time

token = os.environ.get('BOT_TOKEN')
updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher


def start_Command(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, я бот, с которым ты можешь немного поговорить. Я '
                                                          'работаю на ИИ, поэтому мои ответы не всегда корректны, но '
                                                          'меня еще тренируют! Пооговорим?')


def text_Message(bot, update):
    request = apiai.ApiAI('b2ac5a69d50645f581a8ef65c95ce218').text_request()
    request.lang = 'ru'
    request.session_id = 'BatlabAIBot'
    request.query = update.message.text
    response_Json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_Json['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
    time.sleep(0.5)


start_command_handler = CommandHandler('start', start_Command)
text_message_handler = MessageHandler(Filters.text, text_Message)
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
updater.start_polling(clean=True)
updater.idle()
updater.polling()
