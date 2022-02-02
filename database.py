from inspect import Parameter
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import os


dev_pg_connection_uri = 'postgres://postgres:postgres@localhost:5432/rajandevkota'
pg_connection_uri = os.getenv('DATABASE_URL', dev_pg_connection_uri)

# def get_historic_data(ticker):
#   return yf.download(tickers, period="max")

def load_data_into_database(df, ticker):
    conn = create_engine(pg_connection_uri, echo=True)
    df['Ticker'] = ticker
    #df.rename({'Adj Close': 'Adj_Close'})
    df.to_sql('daily_history', con=conn, if_exists='append')

def get_all_records():
    conn = create_engine(pg_connection_uri, echo=True)

    return pd.read_sql_table('daily_history', con=conn)

def get_records(ticker, start, end):
    conn = create_engine(pg_connection_uri, echo=True)
    sql = '''SELECT to_char("Date", 'YYYY/MM/DD') "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "Ticker"
            FROM public.daily_history WHERE daily_history."Ticker"=%(ticker)s
            AND daily_history."Date" BETWEEN %(start)s AND %(end)s'''

    queryParams = {'ticker': ticker, 'start': start, 'end': end}

    return pd.read_sql_query(sql, con=conn, params=queryParams)

def if_exists_record(ticker): 
    conn = create_engine(pg_connection_uri, echo=True)
    sql = '''SELECT count(*) 
            FROM public.daily_history WHERE daily_history."Ticker"=%(ticker)s'''
    queryParams = {'ticker': ticker}

    return pd.read_sql_query(sql, con=conn, params=queryParams)

def get_next_update_date(ticker):
    record_exists  = if_exists_record(ticker).to_numpy()
    result = pd.DataFrame()

    # tmp = record_exists.loc[0]
    if record_exists[0] > 0:
        conn = create_engine(pg_connection_uri, echo=True)
        sql = '''SELECT max("Date")  + INTERVAL '1 day' AS max_date
                FROM public.daily_history WHERE daily_history."Ticker"=%(ticker)s'''
        queryParams = {'ticker': ticker}
        result = pd.read_sql_query(sql, con=conn, params=queryParams)
        return result

    return result


#load_data('FB')
#print("Completed")
