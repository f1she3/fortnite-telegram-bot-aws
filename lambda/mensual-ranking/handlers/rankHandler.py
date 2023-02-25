import fortnite_api
from handlers import constants
import boto3


async def getRanking():
    # Fetch the old stats
    dynamodb = boto3.resource('dynamodb', region_name="eu-west-3")
    table = dynamodb.Table('fortnite-users')
    res = table.scan()
    players = []
    api = fortnite_api.FortniteAPI(
        api_key=constants.FORTNITE_API_KEY, run_async=True)
    for item in res['Items']:
        # Fetch the new stats
        latest_stats = await api.stats.fetch_by_name(item['fortnite_username'])
        # Get a summary for the previous time period
        player = getPlayerSummary(item, latest_stats)
        players.append(player)

        updatePlayerStats(item['tg_id'], latest_stats)

    rankedPlayers = sorted(players, key=lambda d: d['ratio'], reverse=True)

    return rankedPlayers


def getPlayerSummary(dbItem, latest_stats):
    # Get the delta between previous period and today
    new_kill_count = latest_stats.stats.all.overall.kills - \
        latest_stats.stats.all.solo.kills
    monthly_kills = new_kill_count - dbItem['kills']

    new_death_count = latest_stats.stats.all.overall.deaths - \
        latest_stats.stats.all.solo.deaths
    monthly_deaths = new_death_count - dbItem['deaths']
    if monthly_deaths != 0:
        monthly_ratio = monthly_kills / monthly_deaths
    else:
        if monthly_kills == 0:
            monthly_ratio = 0
        else:
            monthly_ratio = 100

    new_match_count = latest_stats.stats.all.overall.matches - \
        latest_stats.stats.all.solo.matches
    monthly_matches = new_match_count - dbItem['matches']

    # Save a summary for every player
    player = {
        "name": dbItem['fortnite_username'],
        "ratio": monthly_ratio,
        "kills": monthly_kills,
        "deaths": monthly_deaths,
        "matches": monthly_matches
    }

    return player


async def getRankingMsg():
    ranking_emojis = [
        "🥇",
        "🥈",
        "🥉",
        "🐐"
    ]
    rankedPlayers = await getRanking()
    msg = f"<code>Classement mensuel</code>\n\n"
    for i in range(len(rankedPlayers)):
        if i < len(ranking_emojis):
            msg += f"{ranking_emojis[i]} {rankedPlayers[i]['name']} - ratio: {round(rankedPlayers[i]['ratio'], 2)}; kills: {rankedPlayers[i]['kills']}; parties: {rankedPlayers[i]['matches']}\n"
        else:
            msg += f"{rankedPlayers[i]['name']} - ratio: {round(rankedPlayers[i]['ratio'], 2)}; kills: {rankedPlayers[i]['kills']}; parties: {rankedPlayers[i]['matches']}\n"

    return msg


def updatePlayerStats(tgId, latestStats):
    newKillCount = latestStats.stats.all.overall.kills - \
        latestStats.stats.all.solo.kills
    newDeathCount = latestStats.stats.all.overall.deaths - \
        latestStats.stats.all.solo.deaths
    newMatchCount = latestStats.stats.all.overall.matches - \
        latestStats.stats.all.solo.matches

    dynamodb = boto3.resource('dynamodb', region_name="eu-west-3")
    table = dynamodb.Table('fortnite-users')
    update_response = table.update_item(
        Key={
            'tg_id': tgId
        },
        UpdateExpression='SET kills = :k, deaths = :d, matches = :m ',
        ExpressionAttributeValues={
            ':k': newKillCount,
            ':d': newDeathCount,
            ':m': newMatchCount
        },
        ReturnValues='UPDATED_NEW'
    )
