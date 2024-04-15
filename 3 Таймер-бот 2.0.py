import logging

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
from config import BOT_TOKEN3 as BOT_TOKEN

TIMER = 5


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global TIMER
    chat_id = update.effective_message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    if len(context.args) != 1:
        await update.effective_message.reply_text("Что-то пошло не так")
        return
    try:
        TIMER = int(context.args[0])
        context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)

        text = f'Вернусь через {TIMER} с.!'
        if job_removed:
            text += ' Старая задача удалена.'
        await update.effective_message.reply_text(text)
    except ValueError:
        await update.effective_message.reply_text("Что-то пошло не так")




async def task(context):
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! {TIMER} c. прошли!')


async def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Таймер отменен!' if job_removed else 'У вас нет активных таймеров'
    await update.message.reply_text(text)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf'''
Привет {user.first_name}! Я умею ставить ставить таймер.
/set_timer x - поставить таймер на x секунд
/unset_timer - убрать поставленный таймер
        ''',
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_timer", set_timer))
    application.add_handler(CommandHandler("unset_timer", unset))

    application.run_polling()


if __name__ == '__main__':
    main()
