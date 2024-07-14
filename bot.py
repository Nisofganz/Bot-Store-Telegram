import telebot
import json
import os
from config import API_TOKEN, ADMIN_ID
from handlers.buy_handler import ask_vps_size, handle_vps_size
from handlers.list_handler import list_prices
from handlers.start_handler import start 

bot = telebot.TeleBot(API_TOKEN)

if not os.path.exists('db'):
    os.makedirs('db')

@bot.message_handler(commands=['start'])
def start_command(message):
    start(bot, message)

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'Fitur:\n/buy - Beli VPS\n/list - Daftar Harga RDP\n/register - Daftar\nOwner: t.me/GloryOfNisof')

@bot.message_handler(commands=['buy'])
def buy_vps(message):
    telegram_id = message.from_user.id
    file_path = f'db/{telegram_id}.json'
    if os.path.exists(file_path):
        ask_vps_size(bot, message)
    else:
        bot.reply_to(message, "Anda belum terdaftar. Silakan daftar terlebih dahulu dengan perintah /register.")

@bot.message_handler(commands=['list'])
def list_vps_prices(message):
    list_prices(bot, message)

@bot.message_handler(func=lambda message: 'gb' in message.text.lower())
def handle_size(message):
    handle_vps_size(bot, message)
    telegram_id = message.from_user.id
    update_total_purchases(telegram_id, 1)

def update_total_purchases(telegram_id, amount):
    file_path = f'db/{telegram_id}.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            user_data = json.load(f)
        user_data['total_purchases'] += amount
        with open(file_path, 'w') as f:
            json.dump(user_data, f)

if __name__ == '__main__':
    bot.polling()