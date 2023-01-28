from telegram import Update
from telegram.ext import ContextTypes

def get_help_msg(user):
    return f"Salut {user.first_name} !\r\nPour finaliser la configuration, exécute la commande suivante :\r\n/config <fortnite_username>"

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_help_msg(user))