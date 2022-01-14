import requests  
import os
from flask import Flask, request, json

BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'  # <-- add your telegram token as environment variable
page = 'https://api.coingecko.com/api/v3/coins/'

app = Flask(__name__)


@app.route('/', methods=['POST'])

def answer(word):
    api = requests.get(f'{page}{word}')
    json_data = json.loads(api.content)
    market_data = json_data['market_data']['current_price']['eur']
    market_cap = json_data['market_data']['market_cap']['eur']
    links = json_data['links']['homepage'][0]
    symbol= json_data['symbol']
    return f'Symbol: {symbol}\nCurrent_price: {market_data}€\nMarket_cap: {market_cap}€\nOfficial_website: {links}'

def main():  
    data = request.json

    print(data)  # Comment to hide what Telegram is sending you
    chat_id = data['message']['chat']['id']
    message = data['message']['text']
    word = message
    json_data = {
        "chat_id": chat_id,
        "text":  answer(word),
    }

    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)

    return ''


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
