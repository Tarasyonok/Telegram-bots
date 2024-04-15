import logging
import json
import translators
import requests
import aiohttp

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes, ConversationHandler
from config import BOT_TOKEN10 as BOT_TOKEN
from random import shuffle

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

async def start(update, context):
    await update.message.reply_text("Я бот геокодер.")


async def geocoder(update, context):
    try:
        geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
        response = await get_response(geocoder_uri, params={
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "format": "json",
            "geocode": update.message.text
        })

        toponym = response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]

        lower_c = toponym["boundedBy"]["Envelope"]["lowerCorner"].replace(' ', ',')
        upper_c = toponym["boundedBy"]["Envelope"]["upperCorner"].replace(' ', ',')

        mark = toponym["Point"]["pos"].replace(' ', ',')

        bbox = f"{lower_c}~{upper_c}"


        # Можно воспользоваться готовой функцией,
        # которую предлагалось сделать на уроках, посвящённых HTTP-геокодеру.

        static_api_request = f"http://static-maps.yandex.ru/1.x/?bbox={bbox}&pt={mark},pm2rdm&l=map"
        await context.bot.send_photo(
            update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
            # Ссылка на static API, по сути, ссылка на картинку.
            # Телеграму можно передать прямо её, не скачивая предварительно карту.
            static_api_request,
            caption="Нашёл:"
        )
    except:
        await update.message.reply_text("По вашему запросу нечего не нашлось")


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            print(resp.url)
            return await resp.json()


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, geocoder)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
