import fortnite_api
from handlers import constants
import boto3

async def getLatestNews():
    # Fetch the id of old news in db
    dynamodb = boto3.resource('dynamodb', region_name="eu-west-3")
    table = dynamodb.Table('fortnite-news')
    res = table.scan()
    db_index = []
    for item in res['Items']:
        db_index.append(str(item['news_id']))

    # Fetch latest news
    api = fortnite_api.FortniteAPI(
        api_key=constants.FORTNITE_API_KEY, run_async=True)
    type = fortnite_api.NewsType('br')
    lang = fortnite_api.GameLanguage(constants.NEWS_LANG)
    news = await api.news.fetch_by_type(language=lang, news_type=type)
    # Will only contain new news
    api_news = []
    for update in news.motds:
        # Skip old news
        if update.id in db_index:
            continue
        else:
            # Insert news into db
            item = {
                'news_id': update.id,
            }
            data = table.put_item(Item=item)
            content = (
                f"<pre>ℹ Nouveauté</pre>\n\n"
                f"<i>{update.title}</i>\n\n"
                f"{update.body}\n\n"
                f"<a href=\"{update.image_url}\">img</a>"
            )
            api_news.append(content)
    return api_news