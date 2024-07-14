from telebot import TeleBot

def list_prices(bot: TeleBot, message):
    prices = [
        "8 GB - 60k",
        "16 GB - 120k"
    ]
    response = "Daftar Harga RDP:\n" + "\n".join(prices)
    bot.reply_to(message, response)