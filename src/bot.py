import logging
from os import listdir
from pprint import pprint
from random import randrange

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, CallbackQueryHandler, ConversationHandler
import bot_settings
from class_application import Application
from mongo_storage import MongoStorage
from myJobs import get_jobs
from openAPI import get_company_info

# Bot:
updater = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# logging:
logging.basicConfig(
    format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# DB:
storage = MongoStorage()

# Keyboard:
keyboard = [
    [InlineKeyboardButton("הכנס משרה", callback_data='add')],
    [InlineKeyboardButton("הצג את כל המשרות", callback_data='display_all')],
    [InlineKeyboardButton("עדכן הפסקת תהליך", callback_data='update')],
    [InlineKeyboardButton("יש משרות חדשות?", callback_data='find')],
    [InlineKeyboardButton("מה החברה הזאת עושה??", callback_data='info')],
]

# Handlers:
update_keyboard = []
reply_markup = InlineKeyboardMarkup(keyboard)
reply_update_markup = InlineKeyboardMarkup(update_keyboard)


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    user = update.message.from_user
    context.chat_data['app'] = Application()
    context.bot.send_message(chat_id=chat_id, text=f"!😊 {user.first_name} היי ")
    try:
        update.message.reply_text('מה תרצה לעשות? 🧐', reply_markup=reply_markup)
    except:
        update.callback_query.message.edit_text('מה תרצה לעשות? 🧐', reply_markup=reply_markup)


info = False
find = False
addnewapp = False


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = update.effective_chat.id
    logger.info(f"= Got on chat #{chat_id}: {query.data!r}")

    match query.data: #### Switch case
        case "add":
            global addnewapp
            addnewapp = True
            context.bot.send_message(chat_id=chat_id, text='מה שם החברה?')

        case "display_all":  #### Maybe by status?
            jobs = storage.findAllAppliedByChatId(chat_id)
            if len(jobs) == 0:
                context.bot.send_message(chat_id=chat_id, text='אתה לא בתהליך קבלה לאף משרה...')
            else:
                context.bot.send_message(chat_id=chat_id, text='כל המשרות שלך:')
                #logger.info(f'len of jobs:{len(jobs)}')
                for job in jobs:
                    context.bot.send_message(chat_id=chat_id,
                                             text=f'{job["company"]}: {job["title"]}, {job["stack"]}, {job["date_applied"]}, status:{job["status"]}')
            context.bot.send_message(chat_id=chat_id, text='מה תרצה לעשות? 🧐', reply_markup=reply_markup)

        case "update":
            jobs = storage.findAllAppliedByChatId(chat_id)
            if len(jobs) == 0:
                context.bot.send_message(chat_id=chat_id, text='אין לך אף משרה! לחץ "הכנס משרה"')
            else:
                global update_keyboard
                update_keyboard.clear()
                for job in jobs:
                    update_keyboard.append(
                        [InlineKeyboardButton(f'{job["company"]} : {job["title"]}', callback_data=f'{job["company"]}')])
                update.callback_query.message.edit_text('בחר את המשרה בה הפסקת תהליך', reply_markup=reply_update_markup)

        case "find":
            global find
            find = True
            context.bot.send_message(chat_id=chat_id, text='רשום באנגלית שם משרה לחיפוש')

        case "info":
            global info
            info = True
            context.bot.send_message(chat_id=chat_id, text='רשום באנגלית שם חברה')

        case _:
            storage.updateJobStatus(chat_id, query.data)
            context.bot.send_message(chat_id=chat_id, text='המשרה עודכנה 😢')
            context.bot.send_message(chat_id=chat_id, text='מה תרצה לעשות? 🧐', reply_markup=reply_markup)


def add_new_app(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = update.message.from_user
    logger.info(f"< Add new app on chat #{chat_id} by {user.first_name}")
    app = context.chat_data['app']
    if not app.company:
        app.set_company(update.message.text)
        context.bot.send_message(chat_id=chat_id, text='מה שם המשרה?')
    elif not app.title:
        app.set_title(update.message.text)
        context.bot.send_message(chat_id=chat_id, text='רשום את הטכנולוגיות הנדרשות לתפקיד')
    elif not app.stack:
        global addnewapp
        app.set_stack(update.message.text)
        storage.insertJob(chat_id, app)
        context.bot.send_message(chat_id=chat_id, text='המשרה הוכנסה ! 📋')
        del context.chat_data['app']
        start(update, context)
        addnewapp = False


def find_new_job(update: Update, context: CallbackContext):
    global find
    chat_id = update.effective_chat.id
    jobs_found = get_jobs(update.message.text)
    if jobs_found:
        context.bot.send_message(chat_id=chat_id, text='מצאתי!')
        for job in jobs_found:
            context.bot.send_message(chat_id=chat_id, text=f'company:{job["company"]}\nCity:{job["city"]}\nLink to apply:{job["link"]}')
        context.bot.send_message(chat_id=chat_id, text='מה תרצה לעשות? 🧐', reply_markup=reply_markup)
        find = False
    else:
        context.bot.send_message(chat_id=chat_id, text='אין לי משרה חדשה בשבילך..')
        context.bot.send_message(chat_id=chat_id, text='מה תרצה לעשות? 🧐', reply_markup=reply_markup)
        find = False




def get_gif_data():
    """ Generates binary data to post animation """
    files = []
    file = '../gif/giphy.gif'
    files.append(file)
    new_gif = files[randrange(1)]
    logger.info(f"-== Used gif file: {new_gif}")
    animation = open(new_gif, 'rb').read()
    return animation
def company_info(update: Update, context: CallbackContext):
    global info
    info = False
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text='רק רגע, מביא נתונים.......')
    context.bot.sendAnimation(chat_id=update.message.chat_id,
                              animation=get_gif_data())
    result = get_company_info(update.message.text)
    context.bot.send_message(chat_id=chat_id, text=result)
    context.bot.send_message(chat_id=chat_id, text='מה תרצה לעשות? 🧐', reply_markup=reply_markup)


def userInputText(update: Update, context: CallbackContext):
    global addnewapp
    global find
    global info
    if addnewapp:
        add_new_app(update, context)
    elif find:
        find_new_job(update, context)
    elif info:
        company_info(update, context)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
answer_handler = MessageHandler(Filters.text, userInputText)
dispatcher.add_handler(answer_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
