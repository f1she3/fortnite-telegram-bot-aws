from telegram import Update, ChatMember, ChatMemberUpdated
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import handlers.helpHandler


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_members = update.message.new_chat_members
    for member in new_members:
        msg = (
            f"Bienvenue @{member.username} !\n\n"
        )
        help = handlers.helpHandler.get_help_msg(member)
        msg += help
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=msg
        )
