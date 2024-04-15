import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
from config import BOT_TOKEN4 as BOT_TOKEN
import random

TIMER = 0
TIMER_TEXT = ''


def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def task(context):
    await context.bot.send_message(context.job.chat_id, text=f'{TIMER_TEXT} истекло')


async def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def start(update, context):
    user = update.effective_user
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_html(
        rf'''
Привет {user.first_name}! Я умею кидать игральные кости и ставить таймер.
/dice - открыть панель броска кубика
/timer - открыть панель таймера
        ''',
        reply_markup=markup
    )



async def open_dice(update, context):
    user = update.effective_user
    reply_keyboard = [
        ['кинуть один шестигранный кубик', 'кинуть 2 шестигранных кубика одновременно'],
        ['кинуть 20-гранный кубик', 'вернуться назад'],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_html(
        rf'Открыл панель броска кубика',
        reply_markup=markup
    )


async def open_timer(update, context):
    user = update.effective_user
    reply_keyboard = [
        ['30 секунд', '1 минута'],
        ['5 минут', 'вернуться назад'],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_html(
        rf'Открыл панель таймера',
        reply_markup=markup
    )


async def return_to_main(update, context):
    reply_keyboard = [['/dice', '/timer']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_html(
        rf'''Вернулся назад''',
        reply_markup=markup
    )


async def echo(update, context):
    if update.message.text.startswith('/'):
        return
    if update.message.text in ['30 секунд', '1 минута','5 минут']:
        global TIMER, TIMER_TEXT
        chat_id = update.effective_message.chat_id
        job_removed = remove_job_if_exists(str(chat_id), context)
        if update.message.text == '30 секунд':
            TIMER = 30
            TIMER_TEXT = '30 секунд'
        elif update.message.text == '1 минута':
            TIMER = 60
            TIMER_TEXT = '1 минута'
        elif update.message.text == '5 минут':
            TIMER = 60 * 5
            TIMER_TEXT = '5 минут'
        context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)
        text = f'засек {TIMER_TEXT}!'

        if job_removed:
            text += ' Старый таймер удалён.'
        await update.effective_message.reply_text(text)

    elif update.message.text in ['кинуть один шестигранный кубик', 'кинуть 2 шестигранных кубика одновременно', 'кинуть 20-гранный кубик']:
        if update.message.text == 'кинуть один шестигранный кубик':
            n = random.randint(1, 6)
            await update.effective_message.reply_text(str(n))
        elif update.message.text == 'кинуть 2 шестигранных кубика одновременно':
            n1 = random.randint(1, 6)
            n2 = random.randint(1, 6)
            await update.effective_message.reply_text(str(n1) + ' ' + str(n2))
        elif update.message.text == 'кинуть 20-гранный кубик':
            n = random.randint(1, 20)
            await update.effective_message.reply_text(str(n))
    elif update.message.text == 'вернуться назад':
        reply_keyboard = [['/dice', '/timer']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

        await update.message.reply_html(
            rf'''Вернулся назад''',
            reply_markup=markup
        )
    else:
        await update.message.reply_text("Не понял команду")


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, echo)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dice", open_dice))
    application.add_handler(CommandHandler("timer", open_timer))
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
