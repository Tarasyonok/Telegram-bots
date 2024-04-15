import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes, ConversationHandler
from config import BOT_TOKEN6 as BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    await update.message.reply_text(
        "Добро пожаловать! Я бот экскурсовод. Вы можете передвигаться"
        " по музею с помощью команд, которые есть на клавиатуре.")
    await update.message.reply_text(
        "Пожалуйста, сдайте верхнюю одежду в гардероб!")

    reply_keyboard = [['/exit_museum', '/to_second']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_text(
        f"В данном зале представлено to_first",
        reply_markup=markup,
    )

    return 1

async def exit_museum(update, context):
    await update.message.reply_text(
        "Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def stop(update, context):
    await update.message.reply_text("Телепортирую вас у выходу")
    await update.message.reply_text(
        "Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def to_first(update, context):
    reply_keyboard = [['/exit_museum', '/to_second']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        f"В данном зале представлено to_first",
        reply_markup=markup,
    )
    return 1


async def to_second(update, context):
    reply_keyboard = [['/to_third', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        f"В данном зале представлено to_second",
        reply_markup=markup,
    )
    return 2


async def to_third(update, context):
    reply_keyboard = [['/to_first', '/to_fourth', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        f"В данном зале представлено to_third",
        reply_markup=markup,
    )
    return 3


async def to_fourth(update, context):
    reply_keyboard = [['/to_first', '/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        f"В данном зале представлено to_fourth",
        reply_markup=markup,
    )
    return 4


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [CommandHandler('exit_museum', exit_museum), CommandHandler('to_second', to_second)],
            2: [CommandHandler('to_third', to_third)],
            3: [CommandHandler('to_first', to_first), CommandHandler('to_fourth', to_fourth)],
            4: [CommandHandler('to_first', to_first)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()



