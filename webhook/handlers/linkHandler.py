import fortnite_api
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from handlers import helpHandler, constants
import boto3


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    api = fortnite_api.FortniteAPI(
        api_key=constants.FORTNITE_API_KEY, run_async=True)
    user = update.effective_user
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=helpHandler.get_help_msg_link(user))
    else:
        fortniteUsername = context.args[0]
        try:
            stats = await api.stats.fetch_by_name(fortniteUsername)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Configuration de {repr(fortniteUsername)}')
            msg = (
                f"Quelques informations concernant ce compte :\n\n"
                f"- Ratio : *{stats.stats.all.overall.kd}*\n"
                f"- Parties jouées : {stats.stats.all.overall.matches}\n"
                f"- Kills par partie : {stats.stats.all.overall.kills_per_match}\n"
                f"- Temps de jeu : _{stats.stats.all.overall.minutes_played // 60}h et {stats.stats.all.overall.minutes_played % 60} min_\n"
                f"- Score : {stats.stats.all.overall.score}\n\n"
                f"*Lier ce compte fortnite ?*"
            )
            keyboard = [[InlineKeyboardButton("✅ Oui", callback_data=fortniteUsername),
                         InlineKeyboardButton("❌ Non", callback_data='cancel')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            print(e)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Erreur lors de la récupération des informations.\r\nVeuillez vérifier le nom d\'utilisateur et réessayer.')


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    callback_query = update.callback_query
    data = callback_query.data
    await callback_query.answer()
    user = update.effective_user
    if data != 'cancel':
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('fortnite-bot')
        fortniteUsername = data
        api = fortnite_api.FortniteAPI(
            api_key=constants.FORTNITE_API_KEY, run_async=True)
        # Get the player's stats
        stats = await api.stats.fetch_by_name(fortniteUsername)
        # Check if tg user is in db
        response = table.get_item(
            Key={
                'tg_id': user.id
            }
        )
        try:
            item = response['Item']
            update_response = table.update_item(
                Key={
                    'tg_id': user.id
                },
                UpdateExpression='SET fortnite_username = :username, kills = :k, deaths = :d ',
                ExpressionAttributeValues={
                    ':username': fortniteUsername,
                    ':k': stats.stats.all.overall.kills,
                    ':d': stats.stats.all.overall.deaths
                },
                ReturnValues='UPDATED_NEW'
            )
        # Else create an item in table
        except KeyError:
            item = {
                'tg_id': user.id,
                'fortnite_username': fortniteUsername,
                'kills': stats.stats.all.overall.kills,
                'deaths': stats.stats.all.overall.deaths
            }
            data = table.put_item(Item=item)
        msg = (
            f"✅ *Configuration terminée* !\n\n"
            f"Bienvenue dans la section, soldat."
        )
        await callback_query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
    elif data == 'cancel':
        await callback_query.edit_message_text(text=f"Configuration annulée")
