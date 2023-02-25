import fortnite_api
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction
from handlers import (
    helpHandler,
    constants,
    statsHandler
)
import boto3


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    api = fortnite_api.FortniteAPI(
        api_key=constants.FORTNITE_API_KEY, run_async=True)
    user = update.effective_user
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=helpHandler.get_help_msg_link(user))
    else:
        fortniteUsername = context.args[0]
        try:
            # stats = await api.stats.fetch_by_name(fortniteUsername)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Configuration de {fortniteUsername}')
            full_stats = await statsHandler.get_full_stats(fortniteUsername)
            msg = (
                f"Quelques informations concernant ce compte :\n\n"
            )
            msg += full_stats
            msg += (
                f"\n<b>Lier ce compte fortnite ?</b>"
            )
            keyboard = [[InlineKeyboardButton("✅ Oui", callback_data=fortniteUsername),
                         InlineKeyboardButton("❌ Non", callback_data='cancel')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(e)
            errMsg = (
                f"Erreur lors de la récupération des informations.\n"
                f"Veuillez vérifier le nom d\'utilisateur et réessayer."
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text=errMsg)


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    callback_query = update.callback_query
    data = callback_query.data
    await callback_query.answer()
    user = update.effective_user
    if data != 'cancel':
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('fortnite-users')
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
        kills = stats.stats.all.overall.kills - stats.stats.all.solo.kills
        deaths = stats.stats.all.overall.deaths - stats.stats.all.solo.deaths
        matches = stats.stats.all.overall.matches - stats.stats.all.solo.matches
        try:
            item = response['Item']
            update_response = table.update_item(
                Key={
                    'tg_id': user.id
                },
                UpdateExpression='SET fortnite_username = :username, kills = :k, deaths = :d, matches = :m ',
                ExpressionAttributeValues={
                    ':username': fortniteUsername,
                    ':k': kills,
                    ':d': deaths,
                    ':m': matches
                },
                ReturnValues='UPDATED_NEW'
            )
        # Else create an item in table
        except KeyError:
            item = {
                'tg_id': user.id,
                'fortnite_username': fortniteUsername,
                'kills': kills,
                'deaths': deaths,
                'matches': matches
            }
            data = table.put_item(Item=item)
        msg = (
            f"✅ <b>Configuration terminée</b> !\n\n"
            f"Bienvenue dans la section, soldat.\n"
        )
        await callback_query.edit_message_text(text=msg, parse_mode=ParseMode.HTML)
    elif data == 'cancel':
        await callback_query.edit_message_text(text=f"Configuration annulée")
