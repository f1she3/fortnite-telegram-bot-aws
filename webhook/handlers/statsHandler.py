import fortnite_api
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from handlers import helpHandler, constants
import boto3


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('fortnite-bot')
    user = update.effective_user

    try:
        response = table.get_item(
            Key={
                'tg_id': user.id
            }
        )
        item = response['Item']
        fortniteUsername = item['fortnite_username']
        full_stats = await get_full_stats(fortniteUsername)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=full_stats, parse_mode=ParseMode.MARKDOWN)
    except KeyError:
        help = helpHandler.get_help_msg_stats(user)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=help)


async def get_full_stats(fortniteUsername):
    api = fortnite_api.FortniteAPI(
        api_key=constants.FORTNITE_API_KEY, run_async=True)
    data = await api.stats.fetch_by_name(fortniteUsername)
    msg = (
        f"```Statistiques```\n\n"
        f"- Taux de victoire : *{data.stats.all.overall.win_rate}*\n\n"
        f"- Ratio (kills / morts) : *{data.stats.all.overall.kd}*\n"
        f"- Nombre total de kills : {data.stats.all.overall.kills}\n"
        f"- Kills par partie : {data.stats.all.overall.kills_per_match}\n\n"
        f"- Score total : {data.stats.all.overall.score}\n"
        f"- Score par partie : {data.stats.all.overall.scorePerMatch}\n"
        f"- Parties jouées : {data.stats.all.overall.matches}\n"
        f"- Temps de jeu : _{data.stats.all.overall.minutes_played // 60}h et {data.stats.all.overall.minutes_played % 60} min_\n\n"
        f"- Dernière modification : {data.stats.all.overall.last_modified}\n"
    )

    return msg
