from dotenv import load_dotenv
import fortnite_api
from telegram import Update
from telegram.ext import ContextTypes
import handlers.helpHandler
import os
from telegram.constants import ParseMode

load_dotenv()


async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_chat_id = os.getenv("GROUP_CHAT_ID")
    fortnite_api_key = os.getenv("FORTNITE_API_KEY")
    api = fortnite_api.FortniteAPI(api_key=fortnite_api_key, run_async=True)
    user = update.effective_user
    if len(context.args) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=handlers.helpHandler.get_help_msg(user))
    else:
        fortniteUsername = context.args[0]
        try:
            stats = await api.stats.fetch_by_name(fortniteUsername)
            await context.bot.send_message(chat_id=group_chat_id, text=f'Parfait, {fortniteUsername} !')
            msg = (
                f"Quelques informations concernant ce compte :\n\n"
                f"- Ratio : *{stats.stats.all.overall.kd}*\n"
                f"- Parties jouées : {stats.stats.all.overall.matches}\n"
                f"- Kills par partie : {stats.stats.all.overall.kills_per_match}\n"
                f"- Temps de jeu : _{stats.stats.all.overall.minutes_played // 60}h et {stats.stats.all.overall.minutes_played % 60} min_\n"
                f"- Score : {stats.stats.all.overall.score}\n"
            )
            await context.bot.send_message(chat_id=group_chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)
        except:
            await context.bot.send_message(chat_id=group_chat_id, text=f'Erreur lors de la récupération des informations.\r\nVeuillez vérifier le nom d\'utilisateur et réessayer.')