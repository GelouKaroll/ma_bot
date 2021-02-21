import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem
from datetime import datetime

tokken = settings.API_KEY
PROXY = {'proxy_url' : settings.PROXY_URL,
         'urllib3_proxy_kwargs' : {
             'username' : settings.PROXY_USERNAME, 
             'password' : settings.PROXY_PASSWORD
            }
        }
logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update,context):
    print('Вызван /start')
    update.message.reply_text("let's start")

def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

def get_constellation(update, context):
    today     = datetime.now().strftime("{}/{}/{}".format('%Y', '%m', '%d'))
    print(update.message.text)
    
    user_text = update.message.text.split()
    planet    = user_text[1].capitalize()
    planet = getattr(ephem, planet)
    
    constellation = ephem.constellation(planet(today))
  
    update.message.reply_text(constellation)

def main():
    # creating  bot + set tokken
    mybot = Updater(tokken, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', get_constellation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info('Бот стартовал')
    #start bot to checking new message 
    mybot.start_polling()
    #start bot
    mybot.idle()

if __name__ == '__main__':
    main()
