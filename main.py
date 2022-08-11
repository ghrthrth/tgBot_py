import requests
import telebot
import json

bot = telebot.TeleBot("5424627277:AAEMba6dgSMkNyoznHAx_LfSK6kclTfWqNQ")

response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?CMC_PRO_API_KEY=f46b82c6-947c-4fb9-89d1-0cd39a4a3675&id=10908")
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['go'])
def send_welcome_go(message):
	price = response.json()['data']['10908']['quote']['USD']['price']
	bot.send_message(message.chat.id, round(price, 5))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.infinity_polling()