from flask import Flask, request, jsonify, make_response
from telegramApi import TelegramApi
import os, sys , re, json, time

#BOT_URL = f'https://api.telegram.org/bot{os.environ["{BOT_KEY}"]}/'  # <-- add your telegram token as environment variable
page = 'https://api.coingecko.com/api/v3/coins/'

app = Flask(__name__)


telegramApi = TelegramApi(os.environ["BOT_KEY"])

def logger(message):
    timestamp = time.strftime('%y-%m-%d %H:%M:%S', time.gmtime())
    sys.stdout.write('{} | {}\n'.format(timestamp, message))


def answer(word):
    api = requests.get(f'{page}{word}')
    json_data = json.loads(api.content)
    logger(json_data)
    market_data = json_data['market_data']['current_price']['eur']
    market_cap = json_data['market_data']['market_cap']['eur']
    links = json_data['links']['homepage'][0]
    symbol= json_data['symbol']
    return f'Symbol: {symbol}\nCurrent_price: {market_data}€\nMarket_cap: {market_cap}€\nOfficial_website: {links}'


@app.route('/status', methods=['GET'])
def get_status():
    return 'Up and running', 201


@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        if request.method == 'GET' or not request.json:
            return 'OK', 200
    except Exception:
        return 'OK', 200
    payload = request.json
    if payload["message"]["text"] == "/hola":
        chat_id = payload["message"]["chat"]["id"]
        name = payload["message"]["from"]["first_name"]
        message = "Hola mi Amo!!"
        telegramApi.send_message(chat_id, message)
    logger(json.dumps(payload, indent=4, sort_keys=True))
    return 'OK', 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)


if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
