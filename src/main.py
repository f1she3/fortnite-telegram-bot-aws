#!/usr/bin/env python

import logging
import traceback
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, Job, JobQueue, filters
import handlers.errorHandler
import handlers.welcomeHandler
import handlers.helpHandler
import handlers.configHandler
import os
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase_admin import credentials

db = firestore.client()

# loads variables from .env file into the script's environment
load_dotenv()

# access environment variables
telegram_token = os.getenv("TELEGRAM_TOKEN")
group_chat_id = os.getenv("GROUP_CHAT_ID")
fortnite_api_key = os.getenv("FORTNITE_API_KEY")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def scheduled(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text="5s")

if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(telegram_token).build()
        job_queue = application.job_queue
        # job = Job(scheduled, interval=5.0)
        # job_queue.put(job, next_t=0.0)
        # job_minute = job_queue.run_repeating(scheduled, interval=5, first=0, chat_id=group_chat_id)

        application.add_error_handler(handlers.errorHandler.error_handler)
        help_handler = CommandHandler('help', handlers.helpHandler.help)
        config_handler = CommandHandler(
            'config', handlers.configHandler.config)
        application.add_handler(CallbackQueryHandler(
            handlers.configHandler.handle_callback_query))

        welcome_handler = MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS, handlers.welcomeHandler.welcome)
        application.add_handler(welcome_handler)

        application.add_handler(help_handler)
        application.add_handler(help_handler)
        application.add_handler(config_handler)

        application.run_polling()
    except Exception as e:
        print("An error occured : ")
        print(e)
        print(traceback.format_exc())
        # print(e)
    except:
        print("An unexpected error occured")
