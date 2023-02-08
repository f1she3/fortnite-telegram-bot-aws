import fortnite_api
from handlers import constants


async def latestNews():
    # await context.bot.send_message(chat_id=context.job.chat_id, text="5s")
    api = fortnite_api.FortniteAPI(
        api_key=constants.FORTNITE_API_KEY, run_async=True)
    type = fortnite_api.NewsType('br')
    lang = fortnite_api.GameLanguage('fr')
    news = await api.news.fetch_by_type(language=lang, news_type=type)
    for update in news.motds:
        print(update.id)
        content = (
            f"<pre>ℹ Nouveauté</pre>\n"
            f"<i>{update.tile}\n\n"
            f"{update.body}\n\n"
            f"<a href={update.image_url}>img</a>"
        )
        """
        TODO : 
        * récupérer toutes les news en db
        * comparer les nouvelles
        * les retourner à lambda_function
        * publier les news depuis lambda_function
        * gérer la programmation de tâches
        """
