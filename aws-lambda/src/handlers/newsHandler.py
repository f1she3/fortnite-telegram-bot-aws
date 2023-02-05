import fortnite_api
from telegram.ext import ContextTypes
from handlers import constants
from firebase_admin import firestore


async def news(context: ContextTypes.DEFAULT_TYPE):
    # await context.bot.send_message(chat_id=context.job.chat_id, text="5s")
    api = fortnite_api.FortniteAPI(
        api_key=constants.FORTNITE_API_KEY, run_async=True)
    type = fortnite_api.NewsType('br')
    lang = fortnite_api.GameLanguage('fr')
    news = await api.news.fetch_by_type(language=lang, news_type=type)
    for update in news.motds:
        print(update.id)
        content = " ```ℹ Nouveauté``` \n"
        content += "_" + update.title + "_\n\n"
        content += update.body + "\n\n"
        content += "[img]("+update.image_url+")"
        # await bot.send_message(chat_id=group_chat_id, text=content, parse_mode='Markdown')
        # await context.bot.send_message(chat_id=context.job.chat_id, text=content, parse_mode='Markdown')

    """
    """
