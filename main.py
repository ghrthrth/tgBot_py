# -*- coding: utf-8 -*-
import requests
import telebot
from telebot import types

bot = telebot.TeleBot("5792158917:AAEKgndL9kw6wu1lBgPEhMcGr-Htng9rEQs")

CMC_PRO_API_KEY = "f46b82c6-947c-4fb9-89d1-0cd39a4a3675"

BTC = "bitcoin"
ETH = "ethereum"
SOL = "solana"
KCS = "KCS"
KUS = "Kuswap"
USD = "usd"

def bot_error_max_requests(message):
    bot.send_message(message.chat.id, 'Превышено максимальное количество запросов в минуту!')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, {0.first_name}, чем Я могу помочь?".format(message.from_user, bot.get_me()), parse_mode='html',
                 reply_markup=markup)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
itembtn1 = types.KeyboardButton('✅ Актуальная информация по топ-3 активам:')
itembtn2 = types.KeyboardButton('💰 Выбор актива из доступных')
markup.add(itembtn1, itembtn2)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}

    response_btc = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + BTC, headers=headers)

    response_eth = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + ETH, headers=headers)

    response_sol = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + SOL, headers=headers)

    if response_btc.status_code == 429:
        bot.send_message(message.chat.id, 'Превышен лимит запросов цены криптовалют за минуту, повторите позже!')
    else:
        if message.text == '✅ Актуальная информация по топ-3 активам:':
            BTC_price = response_btc.json()[BTC][USD]
            ETH_price = response_eth.json()[ETH][USD]
            SOL_price = response_sol.json()[SOL][USD]
            bot.send_message(message.chat.id, "Цена биткоина - " + str(round(BTC_price, 2)) + '$' + '\n' + "Цена эфириума - " + str(round(ETH_price, 2)) + '$' + '\n' + "Цена соланы - " + str(round(SOL_price, 2)) + '$')

        elif message.text == '💰 Выбор актива из доступных':
            markup = types.InlineKeyboardMarkup(row_width=1)
            itembtn11 = types.InlineKeyboardButton("BTC", callback_data='BTC')
            itembtn22 = types.InlineKeyboardButton("KUS", callback_data='KUS')
            itembtn33 = types.InlineKeyboardButton("ETH", callback_data='ETH')
            itembtn44 = types.InlineKeyboardButton("SOL", callback_data='SOL')
            itembtn55 = types.InlineKeyboardButton("KCS", callback_data='KCS')
            itembtn66 = types.InlineKeyboardButton("Назад в меню", callback_data='Назад в меню')
            markup.add(itembtn11, itembtn22, itembtn33, itembtn44, itembtn55, itembtn66)
            bot.send_message(message.chat.id, 'Выберите доступный актив: ', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я тебя не понимаю!')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    response_btc = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + BTC)

    response_eth = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + ETH)

    response_sol = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + SOL)

    response_kus = requests.get(
        "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + KUS)

    response_kcs = requests.get(
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?CMC_PRO_API_KEY=" + CMC_PRO_API_KEY + "&symbol=" + KCS)

    BTC_price = response_btc.json()[BTC][USD]
    ETH_price = response_eth.json()[ETH][USD]
    SOL_price = response_sol.json()[SOL][USD]
    KUS_price = response_kus.json()[KUS][USD]
    KCS_price = response_kcs.json()['data']['' + KCS]['quote']['USD']['price']
    try:
        if call.message:
            if call.data == 'BTC':
                if response_btc.status_code == 429:
                    bot.send_message(call.message.chat.id,
                                     'Превышен лимит запросов цены криптовалют за минуту, повторите позже!')
                else:
                    bot.send_message(call.message.chat.id, 'Актуальная цена биткоина - ' + str(round(BTC_price, 4)) + '$')
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чтобы ты хотел от меня?",
                                      reply_markup=None)

            elif call.data == 'ETH':
                if response_eth.status_code == 429:
                    bot.send_message(call.message.chat.id,
                                     'Превышен лимит запросов цены криптовалют за минуту, повторите позже!')
                else:
                    bot.send_message(call.message.chat.id, 'Актуальная цена эфира - ' + str(round(ETH_price, 4)) + '$')
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чтобы ты хотел от меня?",
                                      reply_markup=None)

            elif call.data == 'KCS':
                bot.send_message(call.message.chat.id, 'Актуальная цена кукоина - ' + str(round(KCS_price, 4)) + '$')
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чтобы ты хотел от меня?",
                                      reply_markup=None)

            elif call.data == 'SOL':
                if response_sol.status_code == 429:
                    bot.send_message(call.message.chat.id,
                                     'Превышен лимит запросов цены криптовалют за минуту, повторите позже!')
                else:
                    bot.send_message(call.message.chat.id, 'Актуальная цена соланы - ' + str(round(SOL_price, 4)) + '$')
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чтобы ты хотел от меня?",
                                      reply_markup=None)

            elif call.data == 'KUS':
                if response_kus.status_code == 429:
                    bot.send_message(call.message.chat.id,
                                     'Превышен лимит запросов цены криптовалют за минуту, повторите позже!')
                else:
                    bot.send_message(call.message.chat.id, 'Актуальная цена кусвап - ' + str(round(KUS_price, 4)) + '$')
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чтобы ты хотел от меня?",
                                      reply_markup=None)

            elif call.data == 'Назад в меню':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Чтобы ты хотел от меня?",
                                      reply_markup=None)
            else:
                bot.send_message(call.message.chat.id, 'Я тебя не понимаю!')
    except Exception as e:
        print(repr(e))


bot.infinity_polling(none_stop=True)
