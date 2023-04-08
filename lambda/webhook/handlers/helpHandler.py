from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode, ChatAction


def get_help_msg(user):
    help = (
        f"Voici la liste des commandes disponibles <a href=\"tg://user?id={user.id}\">{user.first_name}</a> :\n\n"
        f"ℹ  /help - Afficher les commandes disponibles\n\n"
        f"🎮  /link \"username\" - Relier son compte Fortnite\n\n"
        f"📊  /stats - Afficher ses statistiques Fortnite\n\n"
    )

    return help


def get_help_msg_welcome(user):
    help = (
        f"🎉 Bienvenue <a href=\"tg://user?id={user.id}\">{user.first_name}</a> !\n\n"
        f"🤖 Je suis un chatbot conçu pour animer ce groupe Fortnite.\n"
        f"Lorsque tu veux interagir avec moi, écris simplement une commande dans le chat.\n\n"
        f"Par exemple :\n"
        f"/help \n\n"
        f"🟢 Prêt ?\n\n"
        f"Alors commencons par relier ton compte Fortnite avec la commande suivante :\n\n"
        f"/link <i>my_fortnite_username</i>\n\n"
        f"(où <i>my_fortnite_username</i> est ton nom d'utilisateur Fortnite)"
    )

    return help


def get_help_msg_link(user):
    help = (
        f"❌ Nom du compte manquant <a href=\"tg://user?id={user.id}\">{user.first_name}</a>\n\n"
        f"Exemple :\n"
        f"/link <i>my_fortnite_username</i>"
    )

    return help


def get_help_msg_stats(user):
    help = (
        f"❌ Ton compte Fortnite n'a pas encore été relié <a href=\"tg://user?id={user.id}\">{user.first_name}</a>\n\n"
        f"Exécute d'abord : \n"
        f"/link <i>my_fortnite_username</i>"
    )

    return help


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    user = update.effective_user
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=get_help_msg(user),
        parse_mode=ParseMode.HTML
    )
