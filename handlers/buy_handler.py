import json
import urllib.request
import logging
from config import TRIPAY_API_KEY, ADMIN_ID
from telebot import types
import time

logging.basicConfig(level=logging.INFO)

def ask_vps_size(bot, message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("4 GB", callback_data="vps_4gb"))
    markup.add(types.InlineKeyboardButton("8 GB", callback_data="vps_8gb"))
    markup.add(types.InlineKeyboardButton("16 GB", callback_data="vps_16gb"))
    bot.reply_to(message, 'Pilih ukuran VPS yang Anda inginkan:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('vps_'))
def handle_vps_selection(call):
    size_map = {
        'vps_4gb': 4,
        'vps_8gb': 8,
        'vps_16gb': 16
    }
    price_map = {
        4: 30000,
        8: 60000,
        16: 120000
    }
    size = size_map[call.data]
    price = price_map[size]

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Kembali", callback_data="back_to_selection"))
    bot.send_message(call.message.chat.id, f'Harga untuk {size} GB adalah {price} IDR. Apakah Anda ingin melanjutkan?', reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data == 'back_to_selection')
    def back_to_selection(call):
        ask_vps_size(bot, call.message)

    time.sleep(20)

    url = 'https://tripay.co.id/api/transaction/create'
    headers = {
        'Authorization': f'Bearer {TRIPAY_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'method': 'QRIS',
        'merchant_ref': 'INV12345',
        'amount': price,
        'customer_name': call.message.chat.first_name,
        'customer_email': 'customer@example.com',
        'order_items': [
            {
                'sku': 'VPS001',
                'name': f'VPS {size} GB',
                'price': price,
                'quantity': 1
            }
        ],
        'callback_url': 'https://-/callback',
        'return_url': 'https://-/return'
    }

    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode())
        qr_url = response_data['data']['qr_url']
        bot.send_message(call.message.chat.id, f'Silakan scan QR berikut untuk pembayaran: {qr_url}')

    bot.send_message(chat_id=ADMIN_ID, text=f'User {call.message.chat.username} ingin membeli VPS {size} GB.')

def send_rdp(bot, message, size):
    rdp_info = f'RDP untuk {size} GB telah dibuat. Berikut adalah detail RDP Anda:\nIP: -\nUsername: -\nPassword: -'
    bot.send_message(chat_id=message.chat.id, text=rdp_info)