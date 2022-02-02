import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from app import db

#pg_connection_uri = 'postgres://ysfanjjm:4e0quiWFDwOUf7R_P6PIc3r-C8PJqz4l@raja.db.elephantsql.com/ysfanjjm'
pg_connection_uri = 'postgres://postgres:postgres@localhost:5432/rajandevkota'


def scheduleTask():
    print("This test runs every 3 seconds")

def get_historic_data(tickers):
  return yf.download(tickers, period="max")

def create_record(df):
    conn = create_engine(pg_connection_uri, echo=True)
    df.to_sql('daily_history', con=conn, if_exists='append')

    # for data in data_df:
    #     from app import DailyHistory
    #     history = DailyHistory(ticker=ticker, day=data[1])
    #     db.session.add(history)
    #     db.session.commit()

tickers = ['AMD']
# ['FB', 'AMZN', 'NDX', 'TSLA', 'SPX', 'SPY', 'COIN', 'AAPL', 'AMD', 'TSLA','GOOGL']

def load_data():
    for tick in tickers:
        data = get_historic_data(tick)
        df = pd.DataFrame(data)
        df.rename(columns={0:'day'}, inplace=True)

        print(df)
        # df['ticker'] = tick
        print(df)
        new_df = df.rename(columns={'"Date"': 'day', 'Open': 'open', 'High': 'high',
                        'Low': 'low', 'Close' : 'close', 'Adj Close' : 'adj_close', 
                        'Volume' : 'volume' })

        # print(new_df)
        # create_record(df)
        print('Loading data completed!')



load_data()
