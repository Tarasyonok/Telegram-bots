import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN2 as BOT_TOKEN
import datetime

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'''
Привет {user.first_name}! Я умею сообщать дату и время.
/time - время (чч:мм:сс)
/date - дата (дд.мм.гггг)
        ''',
    )


async def show_time(update, context):
    now_time = datetime.datetime.now().time().strftime('%H:%M:%S')
    await update.message.reply_text(now_time)


async def show_date(update, context):
    now_date = datetime.datetime.now().date().strftime('%d.%m.%Y')
    await update.message.reply_text(str(now_date))


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("time", show_time))
    application.add_handler(CommandHandler("date", show_date))

    application.run_polling()


if __name__ == '__main__':
    main()
