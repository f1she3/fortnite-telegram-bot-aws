#!/usr/bin/env python

import logging
import traceback
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Job,
    JobQueue,
    filters
)
from handlers import (
    errorHandler,
    welcomeHandler,
    helpHandler,
    linkHandler,
    statsHandler,
    newsHandler,
    constants
)
from firebase_admin import firestore

db = firestore.client()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# async def scheduled(context: ContextTypes.DEFAULT_TYPE):
#    await context.bot.send_message(chat_id=context.job.chat_id, text="5s")

if __name__ == '__main__':
    try:
        application = ApplicationBuilder().token(constants.TELEGRAM_TOKEN).build()

        # Scheduled jobs
        job_queue = application.job_queue
        # job = Job(scheduled, interval=5.0)
        # job_queue.put(job, next_t=0.0)
        job_minute = job_queue.run_repeating(
            newsHandler.news, interval=5, first=0, chat_id=constants.GROUP_CHAT_ID)

        # Error handler
        application.add_error_handler(errorHandler.error_handler)

        # Commands
        application.add_handler(CommandHandler('help', helpHandler.help))
        application.add_handler(CommandHandler('link', linkHandler.link))
        application.add_handler(CommandHandler('stats', statsHandler.stats))

        # Other handlers
        application.add_handler(CallbackQueryHandler(
            linkHandler.handle_callback_query))
        application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS, welcomeHandler.welcome))

        application.run_polling()
    except Exception as e:
        print("An error occured : ")
        print(e)
        print(traceback.format_exc())
    except:
        print("An unexpected error occured")
