from telegram import Update
from telegram.ext import ContextTypes


def get_help_msg(user):
    help = (
        f"Voici la liste des commandes disponibles @{user.username} :\n\n"
        f"ℹ  /help - Afficher les commandes disponibles\n\n"
        f"🎮  /link <username> - Relier son compte Fortnite\n\n"
        f"📊  /stats - Afficher ses statistiques Fortnite\n\n"
    )

    return help


def get_help_msg_welcome(user):
    help = (
        f"🎉 Bienvenue @{user.username} !\n\n"
        f"Je suis un chatbot conçu pour animer ce groupe Fortnite 🤖\n"
        f"Lorsque tu veux interagir avec moi, écris simplement une commande dans le chat.\n\n"
        f"Par exemple, pour obtenir la liste des commandes disponibles :\n"
        f"/help \n\n"
        f"🟢 Prêt ?\n"
        f"Alors commencons par relier ton compte Fortnite avec la commande suivante :\n"
        f"/link <username> \n"
        f"(où <username> est ton nom d'utilisateur Fortnite)\n\n"
        f"Par exemple : \n"
        f"/link MyFortniteUsername"
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
