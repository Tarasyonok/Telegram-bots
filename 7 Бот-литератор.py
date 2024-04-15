import logging

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes, ConversationHandler
from config import BOT_TOKEN7 as BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

CURR_INDEX = 0
POEM = [
    'Мороз и солнце; день чудесный!',
    'Еще ты дремлешь, друг прелестный -',
    'Пора, красавица, проснись:',
    'Открой сомкнуты негой взоры',
    'Навстречу северной Авроры,',
    'Звездою севера явись!',
    'Вечор, ты помнишь, вьюга злилась,',
    'На мутном небе мгла носилась;',
    'Луна, как бледное пятно,',
    'Сквозь тучи мрачные желтела,',
    'И ты печальная сидела -',
    'А нынче... погляди в окно:',
    'Под голубыми небесами',
    'Великолепными коврами,',
    'Блестя на солнце, снег лежит;',
    'Прозрачный лес один чернеет,',
    'И ель сквозь иней зеленеет,',
    'И речка подо льдом блестит.',
    'Вся комната янтарным блеском',
    'Озарена. Веселым треском',
    'Трещит затопленная печь.',
    'Приятно думать у лежанки.',
    'Но знаешь: не велеть ли в санки',
    'Кобылку бурую запречь?',
    'Скользя по утреннему снегу,',
    'Друг милый, предадимся бегу',
    'Нетерпеливого коня',
    'И навестим поля пустые,',
    'Леса, недавно столь густые,',
    'И берег, милый для меня.',
]
POEM = [
    '1',
    '2',
    '3',
    '4',
]

async def start(update, context):
    global CURR_INDEX
    await update.message.reply_text(POEM[CURR_INDEX])
    CURR_INDEX += 1

    return 1


async def new_line(update: Update, context):
    global CURR_INDEX
    if update.message.text != POEM[CURR_INDEX]:
        reply_keyboard = [['/suphler', '/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            f"нет, не так",
            reply_markup=markup,
        )
        return 2
    else:
        CURR_INDEX += 1
        print(CURR_INDEX, len(POEM))
        if CURR_INDEX == len(POEM):
            reply_keyboard = [['/play_again', '/stop']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
            await update.message.reply_text(
                "Ура! У нас получилось дойти до конца. Хотите начать сначала?",
                reply_markup=markup,
            )
            return 3
        else:
            print('-------')
            await update.message.reply_text(
                POEM[CURR_INDEX],
                reply_markup=ReplyKeyboardRemove(),
            )
            print(CURR_INDEX)
            if CURR_INDEX == len(POEM) - 1:
                reply_keyboard = [['да', 'нет']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                await update.message.reply_text(
                    "Ура! У нас получилось дойти до конца. Хотите начать сначала?",
                    reply_markup=markup,
                )
                return 3
            CURR_INDEX += 1
            return 1


async def stop(update, context):
    await update.message.reply_text(
        "Останавливаю игру",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def suphler(update, context):
    await update.message.reply_text(
        POEM[CURR_INDEX],
    )
    return 2


async def play_again(update, context):
    global CURR_INDEX
    CURR_INDEX = 0
    await update.message.reply_text(
        POEM[CURR_INDEX],
        reply_markup=ReplyKeyboardRemove(),
    )
    CURR_INDEX += 1
    return 1


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_line)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, new_line), CommandHandler('suphler', suphler)],
            3: [CommandHandler('play_again', play_again)],
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
