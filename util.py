from django.template import engine
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

#pg_connection_uri = 'postgres://ysfanjjm:4e0quiWFDwOUf7R_P6PIc3r-C8PJqz4l@raja.db.elephantsql.com/ysfanjjm'
pg_connection_uri = 'postgres://postgres:postgres@localhost:5432/rajandevkota'


def scheduleTask():
    print("This test runs every 3 seconds")

def get_historic_data(tickers):
  return yf.download(tickers, period="max")

def getSqlEngine():
    engine = create_engine(pg_connection_uri, echo=True)
    return engine

def create_record(df, ticker, engine):
    tmp = df.rename(columns={'Date': 'day', 'Open': 'open', 'High': 'high',
                        'Low': 'low', 'Close' : 'close', 'Adj Close' : 'adj_close', 
                        'Volume' : 'volume' }, inplace=True)
    # add new column to the DF
    data_df = pd.DataFrame(tmp)
    # print(tmp)
    data_df['ticker'] = ticker

    with engine.connect() as conn:
        if engine.has_table('daily_history'):
            data_df.to_sql('daily_history', con=conn, if_exists='append', 
            schema='public', index=False, chunksize=1000, method='multi')
        else:
            print("there is no table daily_history")

def load_data_into_db(df, ticker):
    conn = getSqlEngine()  
    tmp = df.rename(columns={'Date': 'day', 'Open': 'open', 'High': 'high',
                        'Low': 'low', 'Close' : 'close', 'Adj Close' : 'adj_close', 
                        'Volume' : 'volume' }, inplace=True)
    # add new column to the DF
    data_df = pd.DataFrame(tmp)
    # print(tmp)
    data_df['ticker'] = ticker

    data_df.to_sql('daily_history', con=conn, if_exists='append')


tickers = ['FB', 'AMZN', 'NDX', 'TSLA', 'SPX', 'SPY', 'COIN', 'AAPL', 'AMD', 'TSLA','GOOGL']

def load_data():
    for tick in tickers:
        data = get_historic_data(tick)
        df = pd.DataFrame(data)
        create_record(df, tick, engine = getSqlEngine())
        print('Loading data completed!')

def fetch_and_load_data():
    for tick in tickers:
        data = get_historic_data(tick)
        df = pd.DataFrame(data)
        load_data_into_db(df, tick)
        print('Fetch and Load data completed!')


fetch_and_load_data()
