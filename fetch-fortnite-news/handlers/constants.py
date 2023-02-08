from dotenv import load_dotenv
import os

# loads variables from .env file into the script's environment
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
FORTNITE_API_KEY = os.getenv("FORTNITE_API_KEY")
LAMBDA_WEBHOOK_ENDPOINT = os.getenv("LAMBDA_WEBHOOK_ENDPOINT")
LAMBDA_WEBHOOK_TOKEN = os.getenv("LAMBDA_WEBHOOK_TOKEN")
