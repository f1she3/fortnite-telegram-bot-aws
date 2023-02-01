from dotenv import load_dotenv
import fortnite_api
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import handlers.helpHandler
import os
from telegram.constants import ParseMode
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('../service-account.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

load_dotenv()


async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fortnite_api_key = os.getenv("FORTNITE_API_KEY")
    api = fortnite_api.FortniteAPI(api_key=fortnite_api_key, run_async=True)
    user = update.effective_user
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=handlers.helpHandler.get_help_msg_config(user))
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
        fortniteUsername = data
        fortnite_api_key = os.getenv("FORTNITE_API_KEY")
        api = fortnite_api.FortniteAPI(
            api_key=fortnite_api_key, run_async=True)
        # Get the player's stats
        stats = await api.stats.fetch_by_name(fortniteUsername)
        # Check if tg user is in db
        query = db.collection('users').where('tg_id', '==', user.id)
        docs = query.get()
        doc_exists = False
        for doc in docs:
            doc_exists = True
            doc_ref = doc.reference
        # If it is link its fortnite account
        if doc_exists:
            doc_ref.update({
                u'fortnite_name': fortniteUsername,
                u'kills': stats.stats.all.overall.kills,
                u'deaths': stats.stats.all.overall.deaths
            })
        # Else create a doc in db
        else:
            doc_ref = db.collection(u'users').document()
            doc_ref.set({
                u'tg_id': user.id,
                u'fortnite_name': fortniteUsername,
                u'kills': stats.stats.all.overall.kills,
                u'deaths': stats.stats.all.overall.deaths
            })
        msg = (
            f"✅ *Configuration terminée* !\n\n"
            f"Bienvenue dans la section, soldat."
        )
        await callback_query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
    elif data == 'cancel':
        await callback_query.edit_message_text(text=f"Configuration annulée")
