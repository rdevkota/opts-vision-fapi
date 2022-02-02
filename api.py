import yfinance as yf
from sqlalchemy import create_engine
import pandas as pd

def get_historic_data(ticker, start, end):
    print("get_historic_data call for: ")
    print("ticker:" + ticker + " start:" + start + " end:" + end)
    want = ["Ticker", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
    stocks = pd.DataFrame(columns = want)

    stock = yf.download(ticker, start=start, end=end)
    stock = stock.reset_index()
    stock["Ticker"] = ticker
    
    stocks = pd.concat([stocks, stock])  

    return stocks

# df = get_historic_data('FB', '2022-01-02', '2022-01-13')
# print(df)