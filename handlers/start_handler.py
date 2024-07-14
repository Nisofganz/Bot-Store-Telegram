from telebot import TeleBot, types

def start(bot: TeleBot, message):
    markup = types.InlineKeyboardMarkup()
    owner_button = types.InlineKeyboardButton("Owner", url="t.me/GloryOfNisof")
    credit_button = types.InlineKeyboardButton("Credit", url="t.me/GloryOfNisof")
    markup.add(owner_button, credit_button)
    
    bot.reply_to(message, 'Selamat datang di bot VPS kami! Ketik /help untuk melihat fitur.', reply_markup=markup)