import logging
import json

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes, ConversationHandler
from config import BOT_TOKEN8 as BOT_TOKEN
from random import shuffle

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

# f_name = input('Введите путь json файла: ')
f_name = 'q.json'

with open(f_name, 'r', encoding='utf-8') as file:
    data = json.load(file)
    QUESTIONS = data['test']
    print(QUESTIONS)


async def start(update, context):
    context.user_data['curr_index'] = 0
    context.user_data['user_ans'] = []
    context.user_data['questions'] = QUESTIONS[:]
    shuffle(context.user_data['questions'])

    await update.message.reply_text("Пройдите небольшой тестовый тест")
    await update.message.reply_text(context.user_data['questions'][context.user_data['curr_index']]['question'])

    return 1


async def ask_question(update: Update, context):
    quests = context.user_data['questions']
    context.user_data['user_ans'].append(update.message.text)
    context.user_data['curr_index'] += 1
    if context.user_data['curr_index'] == len(quests):
        count = 0
        for i in range(len(quests)):
            if quests[i]['response'] == context.user_data['user_ans'][i]:
                count += 1
        await update.message.reply_text(f"Ваш результат {count} из {len(quests)}")
        reply_keyboard = [['/play_again', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text("Ходите пройти тест снова? (/play_again)", reply_markup=markup)
        return 2
    await update.message.reply_text(quests[context.user_data['curr_index']]['question'])
    return 1



async def stop(update, context):
    await update.message.reply_text(
        "Останавливаю тестирование",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def play_again(update, context):
    global CURR_INDEX
    context.user_data['curr_index'] = 0
    shuffle(context.user_data['questions'])
    context.user_data['user_ans'].clear()
    await update.message.reply_text(
        context.user_data['questions'][context.user_data['curr_index']]['question'],
        reply_markup=ReplyKeyboardRemove(),
    )
    return 1


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_question)],
            2: [CommandHandler('play_again', play_again)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
