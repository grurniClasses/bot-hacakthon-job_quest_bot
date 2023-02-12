import logging
from pprint import pprint
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, CallbackQueryHandler
import bot_settings
from src.class_application import Application

logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


keyboard = [
    [InlineKeyboardButton("הכנס משרה", callback_data='add')],
    [InlineKeyboardButton("הצג את כל המשרות", callback_data='display_all')],
    [InlineKeyboardButton("עדכן משרה", callback_data='update')],
]

update_keyboard = []
# def create_update_keyboard():
#     global update_keyboard
#     for key,value in all_apps.items():
#         update_keyboard.append([InlineKeyboardButton(str(value), callback_data=f'{key}')])

reply_markup = InlineKeyboardMarkup(keyboard)
reply_update_markup = InlineKeyboardMarkup(update_keyboard)

counter = 0
new_app = {}
all_apps = {}

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
    context.bot.send_message(chat_id=chat_id, text=f"!{user.first_name}היי  ")
    try:
        update.message.reply_text('מה תרצה לעשות?', reply_markup=reply_markup)
    except:
        update.callback_query.message.edit_text('מה תרצה לעשות?', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    global all_apps
    # print(query.data)
    chat_id = update.effective_chat.id
    # guess_status = update.message.text
    logger.info(f"= Got on chat #{chat_id}: {query.data!r}")
    if query.data == "add":
        context.bot.send_message(chat_id=chat_id, text='מה שם החברה?')
    elif query.data == "display_all":
        # print('here')
        context.bot.send_message(chat_id=chat_id, text='כל המשרות שלך:')
        for value in all_apps.values():
            context.bot.send_message(chat_id=chat_id, text=str(value))
        context.bot.send_message(chat_id=chat_id, text='מה תרצה לעשות?', reply_markup=reply_markup)
        # update.callback_query.message.edit_text('מה תרצה לעשות עכשיו?', reply_markup=reply_markup)

        # print(all_apps)
            # print(json.dump(all_apps))
            # context.bot.send_message(chat_id=chat_id, text=value)
    elif query.data == "update":
        if len(all_apps) == 0:
            context.bot.send_message(chat_id=chat_id, text='אין לך אף משרה! לחץ "הכנס משרה"')
        else:
            # create_update_keyboard()
            # print('here')
            global update_keyboard
            for key, value in all_apps.items():
                update_keyboard.append([InlineKeyboardButton(str(value), callback_data=f'{key}')])
            # print(update_keyboard)

            update.callback_query.message.edit_text('בחר את המשרה בה הפסקת תהליך', reply_markup=reply_update_markup)

def add_new_app(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    global counter
    global new_app
    counter += 1
    if counter == 1:
        new_app['company'] = update.message.text
        context.bot.send_message(chat_id=chat_id, text='מה שם המשרה?')
    elif counter == 2:
        new_app['title'] = update.message.text
        context.bot.send_message(chat_id=chat_id, text='רשום את הטכנולוגיות הנדרשות לתפקיד')
    if counter == 3:
        new_app['stack'] = update.message.text
        app = Application(new_app['company'], new_app['title'], new_app['stack'])
        all_apps[app.get_company()] = app
        counter = 0
        new_app = {}
        context.bot.send_message(chat_id=chat_id, text='המשרה הוכנסה !')
        start(update,context)
    # pprint(all_apps)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
answer_handler = MessageHandler(Filters.text, add_new_app)
dispatcher.add_handler(answer_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")

