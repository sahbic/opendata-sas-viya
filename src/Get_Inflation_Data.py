import os
import pandas as pd
import requests
import zipfile

os.chdir("/home/sasdemo/opendata-sas-viya")
from src.utils import save_and_format_date, upload_save_table

import pandas_datareader as dr
from pandas_datareader import wb
from datetime import date

today = date.today()
this_year = today.year

data = wb.download(indicator='FP.CPI.TOTL.ZG', country='all', start=2010, end=this_year)
data = data.reset_index(1)
data.columns = ['year', 'inflation']
inflation_data = data.reset_index()

caslib = "Opendata"
upload_save_table(inflation_data, conn, "WB_INFLATION", caslib)