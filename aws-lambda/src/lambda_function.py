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
    ret = 'ok'
    async with bot:
        try:
            body = json.loads(event['body'])
            # Basic auth
            if int(body['message']['chat'].get('id')) == int(constants.GROUP_CHAT_ID):
                # res = body['message'].get('text')
                res = json.dumps(body)
                await bot.send_message(chat_id=constants.GROUP_CHAT_ID,
                                       text=res, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            print(e)

    return ret
