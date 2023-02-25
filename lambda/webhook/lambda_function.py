import logging
import asyncio
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler
)

from handlers import (
    constants,
    errorHandler,
    helpHandler,
    welcomeHandler,
    linkHandler,
    statsHandler,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = Application.builder().token(constants.TELEGRAM_TOKEN).build()


def lambda_handler(event, context):
    return asyncio.get_event_loop().run_until_complete(main(event, context))


async def main(event, context):
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

    try:
        await application.initialize()
        await application.process_update(
            Update.de_json(json.loads(event["body"]), application.bot)
        )

        return {
            'statusCode': 200,
            'body': 'Success'
        }

    except Exception as e:
        logging.error('Error at %s', 'division', exc_info=e)
        return {
            'statusCode': 500,
            'body': 'Failure'
        }
