#!/usr/bin/env python

import logging
import traceback
import html
import json
import asyncio
import requests
#import telegram
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram.constants import ParseMode

import handlers.helpHandler

import logging

import os
from dotenv import load_dotenv
import fortnite_api

# loads variables from .env file into the script's environment
load_dotenv()

# access environment variables
telegram_token = os.getenv("TELEGRAM_TOKEN")
group_chat_id = os.getenv("GROUP_CHAT_ID")
fortnite_api_key = os.getenv("FORTNITE_API_KEY")

bot = Bot(token=telegram_token)
api = fortnite_api.FortniteAPI(api_key=fortnite_api_key, run_async=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)



async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    #await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Salut {user.first_name} !\r\nConfigure ton compte fortnite en exécutant \"/config <username>\"")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=context.args[20])
        await context.bot.send_message(chat_id=update.effective_chat.id, text=handlers.helpHandler.get_help_msg(user))
    else:
        fortniteUsername = context.args[0]
        try:
            stats = await api.stats.fetch_by_name(fortniteUsername)
            print(stats.user.raw_data)
            print(stats.stats.all.overall.minutes_played)
            await bot.send_message(chat_id=group_chat_id, text=f'Parfait, {fortniteUsername} !')
            await bot.send_message(chat_id=group_chat_id, text=f'Voici ton nombre moyen de kills par partie : _{stats.stats.all.overall.kills_per_match}_', parse_mode='Markdown')
        except:
            await bot.send_message(chat_id=group_chat_id, text=f"Erreur lors de la récupération des informations.\r\nVeuillez vérifier le nom d'utilisateur et réessayer.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # Finally, send the message
    await context.bot.send_message(
        #chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML
        await bot.send_message(chat_id=group_chat_id, text=message, parse_mode=ParseMode.HTML)
    )

"""
async def main():
    #await check_fortnite_news()
"""
if __name__ == '__main__':
    try:
        #asyncio.run(main())
        application = ApplicationBuilder().token(telegram_token).build()
        
        help_handler = CommandHandler('help', handlers.helpHandler.help)
        config_handler = CommandHandler('config', config)
        application.add_handler(help_handler)
        application.add_handler(config_handler)
        application.add_error_handler(error_handler)
        
        application.run_polling()
    except Exception as e:
        print("An error occured : ")
        print(e)
        print(traceback.format_exc())
        # print(e)
    except:
        print("An unexpected error occured")
