#!/usr/bin/env python

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from random import randrange
import utils
import re
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "gpt-text-parsed.txt")

with open(PATH, "r") as f:
    tweets = f.readlines()
    f.close()

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Buenas noches, señora.')


def echo(update, context):
    if update.message.chat.type == "private":
        utils.send_message(update, tweets[randrange(8000)])

    elif re.search(
                r"(([A,a]((rturo)|(RTURO))))|((([R,r]((everte)|(EVERTE)))[D,d]{0,1}))",
                update.message.text) \
            or randrange(50) == 1:
        utils.reply_message(update, tweets[randrange(8000)])


def main():
    """Start the bot."""
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
