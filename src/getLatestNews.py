import fortnite_api

async def get_latest_news():
    type = fortnite_api.NewsType('br')
    lang = fortnite_api.GameLanguage('fr')
    news = await api.news.fetch_by_type(language=lang, news_type=type)
    for update in news.motds:
        content = " ```ℹ Nouveauté``` \n"
        content += "_" + update.title + "_\n\n"
        content += update.body + "\n\n"
        content += "[img]("+update.image_url+")"
        #await bot.send_message(chat_id=group_chat_id, text=content, parse_mode='Markdown')