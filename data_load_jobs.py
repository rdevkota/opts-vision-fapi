import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
from datetime import date, datetime

tickers = ['AMZN']
#['FB', 'AMZN', 'NDX', 'SPX', 'SPY', 'COIN', 'AAPL', 'TSLA']

def get_historic_data_max(ticker):
  print("get_historic_data_max call for: " + ticker)
  return yf.download(ticker, period="max")

def get_historic_data(ticker, start, end):
  print("get_historic_data call for: ")
  print("ticker:" + ticker + " start:" + start + " end:" + end)
  return yf.download(ticker, start=start, end=end)

def load_data_nightly():
    for tick in tickers:
      from database import load_data_into_database, get_next_update_date
      next_date = get_next_update_date(tick)
    
      if next_date.size < 1:
        data = pd.DataFrame(get_historic_data_max(tick))
        load_data_into_database(data, tick)
      else:
        new_date = next_date.iat[0,0]
        today = date.today()
        if new_date < pd.Timestamp(today):
          start_date = new_date.to_pydatetime().strftime("%Y-%m-%d")
          end_date = today.strftime("%Y-%m-%d")
          data = pd.DataFrame(get_historic_data(tick, start_date, end_date))
          load_data_into_database(data, tick)
        else:
          print('Not loading since the date is in the future: ')
      
      # load_data_into_database(data, tick)
      print('Loading data completed for : ' + tick)

    print('Loading data completed!!!!')

def load_data():
    for tick in tickers:
        from database import load_data_into_database
        data = pd.DataFrame(get_historic_data(tick))
        load_data_into_database(data, tick)
        print('Loading data completed!')

def load_ticker_data(ticker):
      from database import load_data_into_database
      data = pd.DataFrame(get_historic_data(ticker))
      load_data_into_database(data, ticker)
      print('Loading data completed!')
      return('load completed')

load_data_nightly()