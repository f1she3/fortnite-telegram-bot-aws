#!/usr/bin/env python

from telegram import Bot
from handlers import constants
import asyncio


async def main():
    bot = Bot(token=constants.TELEGRAM_TOKEN)
    async with bot:
        """
        """
        await bot.set_webhook(url=constants.LAMBDA_WEBHOOK_ENDPOINT,
                              secret_token=constants.LAMBDA_WEBHOOK_TOKEN)
        status = await bot.get_webhook_info()
        # print(status.url)

if __name__ == '__main__':
    asyncio.run(main())
