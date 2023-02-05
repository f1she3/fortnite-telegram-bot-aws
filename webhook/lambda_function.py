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
    linkHandler,
    statsHandler,
    helpHandler
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
    # application.add_handler(CallbackQueryHandler(
    #    linkHandler.handle_callback_query))
    # application.add_handler(MessageHandler(
    #    filters.StatusUpdate.NEW_CHAT_MEMBERS, welcomeHandler.welcome))

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
        print(e)
        return {
            'statusCode': 500,
            'body': 'Failure'
        }

"""
import json
import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from handlers import constants
from handlers import helpHandler


def lambda_handler(event, context):
    result = asyncio.run(async_handler(event, context))
    return {
        "statusCode": 200,
        "body": result
    }


async def async_handler(event, context):
    bot = Bot(token=constants.TELEGRAM_TOKEN)
    async with bot:
        try:
            body = json.loads(event['body'])
            message = body['message']
            user = message['from']
            current_id = int(message['chat'].get('id'))
            if current_id == int(constants.GROUP_CHAT_ID):
                text = message.get('text').split()
                cmd = text[0]
                if cmd == "/link" or cmd == '/link@ez_fortnite_bot':
                    if len(text) == 1:
                        help_msg = helpHandler.get_help_msg_link(user)
                        await bot.send_message(chat_id=constants.GROUP_CHAT_ID, text=help_msg)
                    else:
                elif cmd == "/stats" or cmd == '/stats@ez_fortnite_bot':
                    help_msg = helpHandler.get_help_msg_stats(user)
                    await bot.send_message(chat_id=constants.GROUP_CHAT_ID, text=help_msg)
                else:
                    help_msg = helpHandler.get_help_msg(user)
                    await bot.send_message(chat_id=constants.GROUP_CHAT_ID, text=help_msg)
                    # await bot.send_message(chat_id=constants.GROUP_CHAT_ID, text=help_msg, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            print(e)

    return 'ok'

"""
