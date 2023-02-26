# 🤖 Telegram bot for Fortnite
### Intro
This project is a simple [Telegram bot](https://core.telegram.org/bots/api) aimed at [Fortnite](https://www.fortnite.com/) players.<br>
The project is built to be deployed to [AWS lambda](https://aws.amazon.com/lambda/?nc1=h_ls). It is built on [webhooks](https://core.telegram.org/bots/webhooks) and the [API Gateway](https://aws.amazon.com/api-gateway/).<br>

💵 Using the [free tier](https://aws.amazon.com/free/), you can host a fully-featured telegram bot <b>for free</b>.<br>

### Features
The bot currently serves 3 functions : 
* ℹ Fetch the latest battle-royale news and posts them to a group
* 📊 Display any player's statistics
* 🥇 Provide a monthly ranking between members of a group
<br>
Feel free to fork the project, adapt it to your needs and deploy your own version of this bot to your group.

## Quick guide
* `lambda/` : The code of the lambda functions
* `layers/python.zip` : the Lambda layer. A layer contains the dependencies required to execute your lamdba functions. [Check here](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html#configuration-layers-create) for more information about Lambda layers.

For every Lambda function, you should place a `.env` file inside the corresponding folder :
* `lambda/webhook/.env` :
```
TELEGRAM_TOKEN = "<TELEGRAM TOKEN>"
GROUP_CHAT_ID = "<THE ID OF YOUR GROUP CHAT>"
FORTNITE_API_KEY = "<CHECK HERE https://dash.fortnite-api.com/>"
LAMBDA_WEBHOOK_ENDPOINT = "<API GATEWAY ENDPOINT (ex : https://example.execute-api.eu-west-3.amazonaws.com/default/webhook)>"
LAMBDA_WEBHOOK_TOKEN = "<API GATEWAY TOKEN>"
```
* `lambda/mensual-ranking/.env` :
```
TELEGRAM_TOKEN = "<TELEGRAM TOKEN>"
GROUP_CHAT_ID = "<THE ID OF YOUR GROUP CHAT>"
FORTNITE_API_KEY = "<CHECK HERE https://dash.fortnite-api.com/>"
NEWS_LANG="<LANG (ex : en)>"
```
* `lambda/fetch-fortnite-news/.env` : same as `lambda/mensual-ranking/.env` 

## Thanks
* The awesome [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library
* [Fortnite-API](https://fortnite-api.com/) for their service and their cool [python wrapper](https://github.com/Fortnite-API/py-wrapper)
* [Knowledge Amplifier](https://www.youtube.com/@KnowledgeAmplifier1) (YouTube) for their [tutorial about AWS](https://www.youtube.com/watch?v=oYMgw4M4cD0)
