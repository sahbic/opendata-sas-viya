import os
import pandas as pd
import requests
import zipfile

os.chdir("/home/sasdemo/opendata-sas-viya")
from src.utils import save_and_format_date, upload_save_table

# change date range here
start_date = '2020-01-01'
    
import yfinance as yf

# Set the ticker as 'EURUSD=X'
forex_data = yf.download('EURUSD=X', start=start_date, end=today)

# Set the index to a datetime object
forex_data.index = pd.to_datetime(forex_data.index)

# rename adj close to eurusd
forex_data = forex_data.rename(columns={'Adj Close': 'eurusd'})

# Keep only the close column
forex_data = forex_data.reset_index()[['Date','eurusd']]

caslib = "Opendata"
upload_save_table(forex_data, conn, "YAHOO_EXCHANGE", caslib)