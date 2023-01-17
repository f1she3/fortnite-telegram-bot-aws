import requests
import json
import os
from dotenv import load_dotenv

# loads variables from .env file into the script's environment
load_dotenv()

# access environment variables
telegram_token = os.getenv("TELEGRAM_TOKEN")
group_chat_id = os.getenv("GROUP_CHAT_ID")

# Fortnite API
# FORTNITE_API_URL = 'https://fortnite-public-api.theapinetwork.com/prod09/upcoming/get'


def send_message_to_telegram(message):
    """Sends a message to the Telegram group chat"""
    url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
    data = {'chat_id': group_chat_id, 'text': message}
    requests.post(url, json=data)


def check_fortnite_releases():
    """Checks for new Fortnite releases"""
    response = requests.get(FORTNITE_API_URL)
    releases = response.json()['releases']
    if releases:
        message = 'New Fortnite release detected: ' + \
            releases[0]['name'] + ' ' + releases[0]['date']
        send_message_to_telegram(message)
    else:
        print("No releases found")


if __name__ == '__main__':
    # check_fortnite_releases()
    send_message_to_telegram("Hello, world")
