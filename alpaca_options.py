from alpaca.trading.client import TradingClient
import os
from dotenv import load_dotenv
load_dotenv()

trading_client = TradingClient(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
    paper=os.getenv("ALPACA_PAPER") == "true"
)

def execute_option_trade(signal, stake):
    print(f"[TRADE] {signal['signal'].upper()} on {signal['ticker']} | Stake: ${stake}")
    # Add real options order logic here later
