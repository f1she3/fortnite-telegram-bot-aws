import logging
import asyncio
from telegram import Bot
from handlers import (
    constants,
    rankHandler
)
from telegram.constants import ParseMode

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def lambda_handler(event, context):
    return asyncio.get_event_loop().run_until_complete(main(event, context))


async def main(event, context):
    bot = Bot(constants.TELEGRAM_TOKEN)
    ranking_msg = await rankHandler.getRankingMsg()
    async with bot:
        await bot.send_message(chat_id=constants.GROUP_CHAT_ID, text=ranking_msg, parse_mode=ParseMode.HTML)
"""
if __name__ == '__main__':
    lambda_handler("", "")
"""
