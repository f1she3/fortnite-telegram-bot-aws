from dotenv import load_dotenv
import os

# loads variables from .env file into the script's environment
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
FORTNITE_API_KEY = os.getenv("FORTNITE_API_KEY")
