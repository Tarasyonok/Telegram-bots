import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN1 as BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.user.first_name}! Я эхо-бот.",
    )


async def echo(update, context):
    await update.message.reply_text(f"Я получил сообщение {update.message.text}")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, echo)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
