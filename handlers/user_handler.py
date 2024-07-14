import os
import json

def user_count(bot, message):
    user_files = [f for f in os.listdir('db') if f.endswith('.json')]
    bot.reply_to(message, f"Jumlah user terdaftar: {len(user_files)}")

def buyer_count(bot, message):
    buyer_count = 0
    for file_name in os.listdir('db'):
        if file_name.endswith('.json'):
            with open(f'db/{file_name}', 'r') as f:
                user_data = json.load(f)
                if user_data.get('total_purchases', 0) > 0:
                    buyer_count += 1
    bot.reply_to(message, f"Jumlah pembeli: {buyer_count}")