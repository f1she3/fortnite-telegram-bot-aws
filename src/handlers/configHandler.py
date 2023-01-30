from dotenv import load_dotenv
import fortnite_api
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import handlers.helpHandler
import os
from telegram.constants import ParseMode

load_dotenv()


async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fortnite_api_key = os.getenv("FORTNITE_API_KEY")
    api = fortnite_api.FortniteAPI(api_key=fortnite_api_key, run_async=True)
    user = update.effective_user
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=handlers.helpHandler.get_help_msg(user))
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
            keyboard = [[InlineKeyboardButton("✅ Oui", callback_data='confirm'),
                         InlineKeyboardButton("❌ Non", callback_data='cancel')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            print(e)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Erreur lors de la récupération des informations.\r\nVeuillez vérifier le nom d\'utilisateur et réessayer.')


async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    update.effective_chat.id
    await query.answer()

    if data == 'confirm':
        msg = (
            f"🎉🎊 *Configuration terminée* 🎉🎊\n\n"
            f"Bienvenue dans la section, soldat."
        )
        await query.edit_message_text(text=msg, parse_mode=ParseMode.MARKDOWN)
    elif data == 'cancel':
        await query.edit_message_text(text=f"Configuration annulée")
