import os
os.chdir("/home/sasdemo/opendata-sas-viya")

import pandas as pd
import requests
import zipfile
import json

from src.utils import save_and_format_date, upload_save_table

url = "https://carlabelling.ademe.fr/recherche-ajax?searchString=&co2=&brand=&model=&category=&range=&transmission=&price=0%2C500000&maxconso=&energy=0%2C7&RechercherL=Rechercher&limit=100000&offset=0&orderby[]=co2_co_high%20asc&searchString=&co2="
response = requests.get(url)

carlabels = pd.DataFrame.from_records(json.loads(response.text)["content"])

# load data in SAS Viya
caslib = "Opendata"
upload_save_table(carlabels, conn, "EMISSIONS_VEHICULES", caslib)