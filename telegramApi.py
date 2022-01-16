import requests

BOT_URL = 'https://api.telegram.org/bot{}'  # <-- add your telegram token as environment variable

class TelegramApi():
  def __init__(self, token):
    self._token = token
    self._channel =  channel
  
  def send_message(self, chat_id, message, reply_markup=None):
        url = BOT_URL.format(self._token) + '/sendMessage'
        data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
        if reply_markup:
          data['reply_markup'] = reply_markup
        r = requests.post(url, data=data)
        if r.status_code == 200:
          return r.json()
        return None
  
  def send_chat_action(self, action=None, chat_id=None):
        chat_id = chat_id if chat_id else self._channel
        url = f"https://api.telegram.org/bot{self._token}/sendChatAction"
        data = {"chat_id": chat_id, "action": action} 
        r = requets.get(url, data=data)
        if r.status_code == 200:
          return r.json()
        return None
