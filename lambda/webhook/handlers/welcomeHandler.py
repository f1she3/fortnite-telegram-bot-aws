from telegram import Update
from telegram.ext import ContextTypes
from handlers import helpHandler


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.message.new_chat_members
    for member in new_members:
        msg = helpHandler.get_help_msg_welcome(member)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg
        )
