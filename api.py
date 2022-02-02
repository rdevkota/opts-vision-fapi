import yfinance as yf

def get_historic_data(ticker, start, end):
  print("get_historic_data call for: ")
  print("ticker:" + ticker + " start:" + start + " end:" + end)
  return yf.download(ticker, start=start, end=end)