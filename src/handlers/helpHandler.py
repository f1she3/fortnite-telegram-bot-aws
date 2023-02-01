from telegram import Update
from telegram.ext import ContextTypes


def get_help_msg(user):
    help = (
        f"Voici la liste des commandes disponibles @{user.username} :\n\n"
        f"ℹ  /help - Guide de démarrage\n\n"
        f"🎮  /link <username> - Relier son compte Fortnite\n\n"
        f"📊  /stats - Une fois le compte lié, affiche ses statistiques\n\n"
    )

    return help


def get_help_msg_link(user):
    help = (
        f"❌ Nom du compte manquant @{user.username}\n\n"
        f"Exemple: \"/link pseudo\""
    )

    return help


def get_help_msg_stats(user):
    help = (
        f"❌ Ton compte Fortnite n'a pas encore été relié @{user.username}\n\n"
        f"Exécute d'abord : \"/link pseudo\""
    )

    return help


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_help_msg(user))
