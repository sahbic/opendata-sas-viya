import os
os.chdir("/home/sasdemo/opendata-sas-viya")

import pandas as pd
import requests
import zipfile

from utils import save_and_format_date, upload_save_table

TMP_PATH = "tmp"

# create directory if it doesn't exist
os.makedirs(TMP_PATH, exist_ok=True)

# remove files from directory
for file in os.listdir(TMP_PATH):
    os.remove(TMP_PATH + "/" + file)

# Download the zip file from the URL
URL = "https://files.georisques.fr/GASPAR/gaspar.zip"
response = requests.get(URL)

# Save the zip file
open(TMP_PATH + '/file.zip', 'wb').write(response.content)

# Unzip the file
with zipfile.ZipFile(TMP_PATH + '/file.zip', 'r') as zip_ref:
    zip_ref.extractall(TMP_PATH)

# read files
catnat = pd.read_csv(TMP_PATH + "/catnat_gaspar.csv", sep=";")
azi = pd.read_csv(TMP_PATH + "/azi_gaspar.csv", sep=";")
risq = pd.read_csv(TMP_PATH + "/risq_gaspar.csv", sep=";")

# remove files from directory
for file in os.listdir(TMP_PATH):
    os.remove(TMP_PATH + "/" + file)

# load data in SAS Viya
caslib = "Opendata"
upload_save_table(catnat, conn, "GASPAR_CATASTROPHES_NATURELLES", caslib)
upload_save_table(azi, conn, "GASPAR_ATLAS_ZONES_INNONDABLES", caslib)
upload_save_table(risq, conn, "GASPAR_RISQUES_MAJEURS", caslib)