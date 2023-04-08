from telegram import Update
from telegram.ext import ContextTypes
from handlers import helpHandler
from telegram.constants import ParseMode, ChatAction


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    new_members = update.message.new_chat_members
    for member in new_members:
        msg = helpHandler.get_help_msg_welcome(member)
        if member.is_bot:
            chatId = update.effective_chat.id
        else:
            chatId = member.id
        await context.bot.send_message(
            chat_id=chatId,
            text=msg,
            parse_mode=ParseMode.HTML
        )
