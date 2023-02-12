import logging
import random
from threading import Timer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler

import bot_settings

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

minGuess = 1
maxGuess = 100
guess = 1
keyboard = [
    [
        InlineKeyboardButton("הכנס-משרה", callback_data='add'),
        InlineKeyboardButton("מחק-משרה", callback_data='remove'),
    ],
    [InlineKeyboardButton("הצג את כל המשרות", callback_data='all')],
]
reply_markup = InlineKeyboardMarkup(keyboard)


# def help_command(update: Update, context: CallbackContext):
#     chat_id = update.effective_chat.id
#     user = update.message.from_user
#     context.bot.send_message(chat_id=chat_id, text=f"{user.first_name}, Use /start to restart the game.")
#     # update.message.reply_text("Use /start to restart the game.")
#

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    user = update.message.from_user

    context.bot.send_message(chat_id=chat_id, text=f"Hello {user.first_name}! Welcome to our bot!")
    try:
        update.message.reply_text('click:', reply_markup=reply_markup)
    except:
        update.callback_query.message.edit_text(f'click:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    print('hi')
    query = update.callback_query
    query.answer()
    print(query.data)

    chat_id = update.effective_chat.id
    # guess_status = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {query.data!r}")
    if query.data == "add":
        context.bot.send_message(chat_id=chat_id, text='added')


start_handler = CommandHandler('start', start)
# guess_handler = CommandHandler('guess', start)
# help_handler = CommandHandler('help', help_command)
# dispatcher.add_handler(help_handler)
dispatcher.add_handler(start_handler)
# dispatcher.add_handler(guess_handler)

updater.dispatcher.add_handler(CallbackQueryHandler(button))

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")










#
# my_bot = Updater(token=bott_setings.BOT_TOKEN, use_context=True)
#
#
# my_bot.dispatcher.add_handler(CommandHandler("start", start))
#
# updater.dispatcher.add_handler(CallbackQueryHandler(button))
#
# logger.info("* Start polling...")
# my_bot.start_polling()  # Starts polling in a background thread.
# my_bot.idle()  # Wait until Ctrl+C is pressed
# logger.info("* Bye!")
