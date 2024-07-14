import json
import urllib.request
import logging
from config import TRIPAY_API_KEY, ADMIN_ID

logging.basicConfig(level=logging.INFO)

def ask_vps_size(bot, message):
    bot.reply_to(message, 'Berapa GB VPS yang Anda inginkan?')

def handle_vps_size(bot, message):
    try:
        
        size = int(''.join(filter(str.isdigit, message.text)))
        price = size * 7500 
        bot.reply_to(message, f'Oke, harga untuk {size} GB adalah {price} IDR. Membuatkan QRIS...')

        
        url = 'https://tripay.co.id/api/transaction/create'
        headers = {
            'Authorization': f'Bearer {TRIPAY_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'method': 'QRIS',
            'merchant_ref': 'INV12345',
            'amount': price,
            'customer_name': message.from_user.first_name,
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
            bot.reply_to(message, f'Silakan scan QR berikut untuk pembayaran: {qr_url}')
    except urllib.error.HTTPError as e:
        error_message = e.read().decode()
        logging.error(f'HTTPError: {e.code} - {error_message}')
        bot.reply_to(message, f'Terjadi kesalahan saat membuat invoice: {error_message}. Silakan coba lagi.')
    except Exception as e:
        logging.error(f'Exception: {str(e)}')
        bot.reply_to(message, 'Terjadi kesalahan saat membuat invoice. Silakan coba lagi.')

    bot.send_message(chat_id=ADMIN_ID, text=f'User {message.from_user.username} ingin membeli VPS {size} GB.')

def send_rdp(bot, message, size):
    rdp_info = f'RDP untuk {size} GB telah dibuat. Berikut adalah detail RDP Anda:\nIP: 192.168.1.1\nUsername: user\nPassword: password'
    bot.send_message(chat_id=message.chat.id, text=rdp_info)