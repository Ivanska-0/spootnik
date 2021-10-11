import os
import requests

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


def reply_message(update, msg):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    req = "https://api.telegram.org/bot" + TOKEN + \
        "/sendMessage?chat_id="+ str(chat_id) + \
        "&text=" + msg + \
        "&reply_to_message_id=" + str(msg_id)
    requests.get(req)
