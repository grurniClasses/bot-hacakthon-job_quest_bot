import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, \
    Filters, Updater, CallbackQueryHandler, ConversationHandler
import bot_settings
from src.class_application import Application
from src.mongo_storage import MongoStorage

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
    [InlineKeyboardButton("עדכן משרה", callback_data='update')],
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
    context.bot.send_message(chat_id=chat_id, text=f"! {user.first_name}היי  ")
    try:
        update.message.reply_text('מה תרצה לעשות?', reply_markup=reply_markup)
    except:
        update.callback_query.message.edit_text('מה תרצה לעשות?', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = update.effective_chat.id
    logger.info(f"= Got on chat #{chat_id}: {query.data!r}")

    match query.data: #### Switch case
        case "add":
            context.bot.send_message(chat_id=chat_id, text='מה שם החברה?')

        case "display_all":  #### Maybe by status?
            context.bot.send_message(chat_id=chat_id, text='כל המשרות שלך:')
            jobs = storage.findAllByChatId(chat_id)
            logger.info(f'len of jobs:{len(jobs)}')
            for job in jobs:
                context.bot.send_message(chat_id=chat_id,
                                         text=f'{job["company"]}: {job["title"]}, {job["stack"]}, {job["date_applied"]}')
            context.bot.send_message(chat_id=chat_id, text='מה תרצה לעשות?', reply_markup=reply_markup)

        case "update":
            jobs = storage.findAllByChatId(chat_id)
            if len(jobs) == 0:
                context.bot.send_message(chat_id=chat_id, text='אין לך אף משרה! לחץ "הכנס משרה"')
            else:
                global update_keyboard
                update_keyboard.clear()
                for job in jobs:
                    update_keyboard.append(
                        [InlineKeyboardButton(f'{job["company"]} : {job["title"]}', callback_data=f'{job["company"]}')])
                update.callback_query.message.edit_text('בחר את המשרה בה הפסקת תהליך', reply_markup=reply_update_markup)

        case _:
            storage.updateJobStatus(chat_id, query.data)
            context.bot.send_message(chat_id=chat_id, text='המשרה עודכנה!')
            context.bot.send_message(chat_id=chat_id, text='מה תרצה לעשות?', reply_markup=reply_markup)


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
        app.set_stack(update.message.text)
        storage.insertJob(chat_id, app)
        context.bot.send_message(chat_id=chat_id, text='המשרה הוכנסה !')
        del context.chat_data['app']
        start(update, context)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
answer_handler = MessageHandler(Filters.text, add_new_app)
dispatcher.add_handler(answer_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))

logger.info("* Start polling...")
updater.start_polling()  # Starts polling in a background thread.
updater.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
