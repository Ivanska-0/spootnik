#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
from dotenv import load_dotenv
from random import randrange
from random_facts import random_fact
import support
import requests
import time
import schedule
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def id(update, context):
    update.message.reply_text("La ID del chat es: " + \
                            str(update.message.chat.id) + \
                            " mi pana.")


def dance(update, context):
    support.send_message(update,
            "♪┌|∵|┘♪ └|∵|┐♪♪┌|∵|┘♪ └|∵|┐♪♪┌|∵|┘♪")


def echo(update, context):
    """Echo the user message."""
    if update.message.text == "a." and randrange(20) == 1:
        support.send_message(update,
                "PAPOPEPOPARAPAPAPAPA")
    elif update.message.text == "a.":
        support.send_message(update,
                "a.")

    if randrange(50) == 1:
        support.send_message(update,
                "Hey guys, did you know that " + random_fact())


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("id", id))
    dp.add_handler(CommandHandler("dance", dance))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
