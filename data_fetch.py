import yfinance as yf

def get_market_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return f"Price:{info.get('currentPrice')} IV:{info.get('impliedVolatility')} Vol:{info.get('volume')}"
    except:
        return "Data error"
