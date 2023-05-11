from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from datetime import datetime, timedelta

import logging

import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)

def delete_messages(bot, job):

    chat_id = job.context['chat_id']

    message_ids = job.context['message_ids']

    bot.delete_message(chat_id=chat_id, message_id=message_ids)
    
def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text='Bot started!')

updater = Updater(token=os.environ.get('BOT_TOKEN'), use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)

dispatcher.add_handler(start_handler)

def group_message(update, context):

    message = update.message

    chat_id = message.chat_id

    message_ids = message.message_id

    delay = timedelta(minutes=10)  # Change the time as per your requirement

    context.job_queue.run_once(delete_messages, delay, context={'chat_id': chat_id, 'message_ids': message_ids})


group_message_handler = MessageHandler(Filters.group, group_message)

dispatcher.add_handler(group_message_handler)


updater.start_polling()

updater.idle()

