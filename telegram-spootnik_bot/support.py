import re
import os
import requests

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")


def extract(regularE, init, stop, string):
    return re.findall(regularE, string)[0]\
             .replace(init, "")\
             .replace(stop, "")


def get_term_clock_pid():
    ret = os.popen("systemctl status sputnikDriver.service").read()
    return int(extract(r"term_clock .+ PID", "term_clock ", " PID", ret))


def check_alive():
    ret = os.popen("systemctl status sputnikDriver.service").read()
    return "java" in ret


def send_message(update, text):
    send_text = "https://api.telegram.org/bot" + TOKEN + \
            "/sendMessage?chat_id=" + str(update.message.chat.id) + \
            "&parse_mode=Markdown&text=" + text
    response = requests.get(send_text)
    return response.json()["ok"]

