import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

def scheduleTask():
    print("This test runs every 3 seconds")

def get_historic_data(tickers):
  return yf.download(tickers, period="max")

def getSqlEngine():
    db_uri = 'sqlite:///datastore/ov_daily_data.db'
    engine = create_engine(db_uri, echo=True)
    return engine

def create_record(df, ticker):
    engine = getSqlEngine()
    # add new column to the DF
    df['ticker'] = ticker
    df.rename(columns={'Date': 'Date', 'Open': 'open', 'High': 'high',
                        'Low': 'low', 'Close' : 'close', 'Adj Close' : 'adj_close', 
                        'Volume' : 'volume' }, inplace=True)
    df.to_sql("daily_history", engine, if_exists='append')
   
tickers = ['FB', 'AMZN', 'NDX', 'TSLA', 'SPX', 'SPY', 'COIN', 'AAPL', 'AMD', 'TSLA','GOOGL']

def load_data():
    for tick in tickers:
        data = get_historic_data(tick)
        df = pd.DataFrame(data)
        create_record(df, tick)
        print('Loading data completed!')
