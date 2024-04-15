import logging
import json


from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes, ConversationHandler
from config import BOT_TOKEN9 as BOT_TOKEN
from random import shuffle

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

async def start(update, context):
    if 'lang' not in context.user_data:
        context.user_data['lang'] = 'ru'
    reply_keyboard = [['/to_russian', '/to_english']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text("Я бот переводчик.", reply_markup=markup)


async def to_english(update, context):
    context.user_data['lang'] = 'en'
    await update.message.reply_text("Ок, теперь перевожу на английский.")


async def to_russian(update, context):
    context.user_data['lang'] = 'ru'
    await update.message.reply_text("Ок, теперь перевожу на русский.")


async def translate(update, context):
    try:
        text = update.message.text
        text_translate = translators.translate_text(text, to_language=context.user_data['lang'])
        if not text_translate:
            text_translate = 'Не получилось'
        await update.message.reply_text(text_translate)
    except Exception as error:
        await update.message.reply_text(error)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, translate)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("to_english", to_english))
    application.add_handler(CommandHandler("to_russian", to_russian))
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
