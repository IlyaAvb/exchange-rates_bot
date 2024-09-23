import csv

import requests
import fake_useragent
from fake_useragent import UserAgent

import telebot

user_agent = fake_useragent.UserAgent().random
headers = {
    'user-agent': user_agent
}



def read_file():
    coins = []
    with open('coins.txt') as file:
        for line in file:
            coins.append(line)
    return coins

data = {
        'ByBit': {},
        'OKX': {},
        'Binance': {},
    }

def add_to_dict(market, market_price):

    if market == 'Bybit':
        data['ByBit'].update(market_price)
    elif market == 'OKX':
        data['OKX'].update(market_price)
    elif market == 'Binance':
        data['Binance'].update(market_price)



def get_price_from_bybit(coins): #bybit
    bybit_price = {}
    market = 'Bybit'
    for coin in coins:
        try:
            response = requests.get(f'https://api-testnet.bybit.com/v5/market/tickers?category=spot&symbol={coin.strip().upper()}USDT')
            data = response.json()
            bybit_price[coin] = data['result']['list'][0]['usdIndexPrice']
        except Exception as error:
            bybit_price[coin] = 'none'
    add_to_dict(market, bybit_price)

def get_price_from_okx(coins): #bybit
    okx_price = {}
    market = 'OKX'
    for coin in coins:
        response = requests.get(f'https://www.okx.com/api/v5/market/ticker?instId={coin.strip().upper()}-USD-SWAP')
        data = response.json()
        if data['code'] == '0':
            okx_price[coin] = data['data'][0]['last']
        else:
            okx_price[coin] = 'none'
    add_to_dict(market, okx_price)

def get_price_from_binace(coins): #bybit
    binace_price = {}
    market = 'Binance'
    for coin in coins:
        try:
            response = requests.get(f'https://www.okx.com/api/v5/market/ticker?instId={coin.strip().upper()}-USD-SWAP')
            data = response.json()
            binace_price[coin] = data['data'][0]['last']
        except Exception as err:
            binace_price[coin] = 'none'
    add_to_dict(market, binace_price)

def update_data():
    global response_message
    response_message = ''
    for key, values in data.items():
        response_message += f'{key} \n'
        for k, v in values.items():
            if v != 'none':
                response_message += f'{str(k).strip().upper()} - {v} USDT \n'
        response_message += '\n'
    return response_message



coins = read_file()
get_price_from_bybit(coins)
get_price_from_okx(coins)
get_price_from_binace(coins)



bot = telebot.TeleBot('7895098930:AAEsEPvq9YAR36DgNp2pQWJ653hLZIM0SsU')


def telegram_bot():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} 🙊 \n\n"
                                           f"Этот бот будет отслеживать стоимость BTC, ETH, SOl на разных биржах")

    @bot.message_handler(commands=['get_price'])
    def get_prices(message):
        update_data()
        bot.send_message(message.chat.id, response_message)

    bot.infinity_polling()
