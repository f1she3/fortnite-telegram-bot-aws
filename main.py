#!/usr/bin/env python

import traceback
import asyncio
import requests
#import telegram
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
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

async def check_fortnite_news():
    type = fortnite_api.NewsType('br')
    lang = fortnite_api.GameLanguage('fr')
    news = await api.news.fetch_by_type(language=lang, news_type=type)
    for update in news.motds:
        content = " ```ℹ Nouveauté``` \n"
        content += "_" + update.title + "_\n\n"
        content += update.body + "\n\n"
        content += "[img]("+update.image_url+")"
        await bot.send_message(chat_id=group_chat_id, text=content, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Salut {user.first_name} !\r\nConfigure ton compte fortnite en exécutant \"/config <username>\"")
    #await update.message.reply_text("test")

"""
async def main():
    #await check_fortnite_news()
"""
if __name__ == '__main__':
    try:
        #asyncio.run(main())
        application = ApplicationBuilder().token(telegram_token).build()
        
        start_handler = CommandHandler('start', start)
        application.add_handler(start_handler)
        
        application.run_polling()
    except Exception as e:
        print("An error occured : ")
        print(e)
        print(traceback.format_exc())
        # print(e)
    except:
        print("An unexpected error occured")
