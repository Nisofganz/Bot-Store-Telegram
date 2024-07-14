import telebot
from config import API_TOKEN, ADMIN_ID
from handlers.buy_handler import ask_vps_size, handle_vps_size
from handlers.list_handler import list_prices
from handlers.start_handler import start 

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    start(bot, message)

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'Fitur:\n/buy - Beli VPS\n/list - Daftar Harga RDP\nOwner: t.me/GloryOfNisof')

@bot.message_handler(commands=['buy'])
def buy_vps(message):
    ask_vps_size(bot, message)

@bot.message_handler(commands=['list'])
def list_vps_prices(message):
    list_prices(bot, message)

@bot.message_handler(func=lambda message: 'gb' in message.text.lower())
def handle_size(message):
    handle_vps_size(bot, message)

if __name__ == '__main__':
    bot.polling()