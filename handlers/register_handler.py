import json
import os

def register_user(bot, message):
    telegram_id = message.from_user.id
    user_data = {
        "telegram_id": telegram_id,
        "total_purchases": 0
    }
    file_path = f'db/{telegram_id}.json'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(user_data, f)
        bot.reply_to(message, "Anda berhasil terdaftar!")
    else:
        bot.reply_to(message, "Anda sudah terdaftar.")