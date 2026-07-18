import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TICKERS = ["AAPL", "TSLA", "NVDA", "AMD", "META", "AMZN", "GOOGL", "MSFT", "NFLX", "SPY"]

MIN_CONFIDENCE = 80
DEFAULT_STAKE = 100
