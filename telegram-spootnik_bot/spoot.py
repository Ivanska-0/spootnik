import time
import schedule
import requests
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def telegram_bot_sendtext():
    send_text = "https://api.telegram.org/bot" + TOKEN + \
        "/sendMessage?chat_id=" + CHAT_ID + "&parse_mode=Markdown&text=Spoot%20Spoot!"
    response = requests.get(send_text)
    return response.json()["ok"]

if __name__ == "__main__":
    time.sleep(15)
    print(telegram_bot_sendtext())
    print("Spoot-Spooted")
    exit()

