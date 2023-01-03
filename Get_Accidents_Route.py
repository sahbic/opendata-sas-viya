import requests
import pandas as pd
import os
os.chdir("/home/sasdemo/opendata-sas-viya")

from utils import save_and_format_date, upload_save_table

headers = {
    'Accept': 'application/json, text/plain, */*'
}

params = {
    'type': 'main',
    'page_size': '1000',
    'q': '',
}

response = requests.get('https://www.data.gouv.fr/api/2/datasets/53698f4ca3a729239d2036df/resources/', params=params, headers=headers)

vehicules, caracs, lieux, usagers = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Récupérer l'ensemble des données
for data in response.json()["data"]:
    if ("vehicules-2" in data["title"]):
        part = pd.read_csv(data["latest"], sep=";")
        if part.shape[1] == 1:
            part = pd.read_csv(data["latest"], sep=",", low_memory=False)
        vehicules = pd.concat([vehicules, part])
    elif ("lieux-" in data["title"]):
        part = pd.read_csv(data["latest"], sep=";")
        if part.shape[1] == 1:
            part = pd.read_csv(data["latest"], sep=",", low_memory=False)
        lieux = pd.concat([lieux, part])
    elif ("usagers-" in data["title"]):
        part = pd.read_csv(data["latest"], sep=";")
        if part.shape[1] == 1:
            part = pd.read_csv(data["latest"], sep=",")
        usagers = pd.concat([usagers, part])
    elif ("caracteristiques-" in data["title"]) | ("carcteristiques-" in data["title"]):
        try:
            part = pd.read_csv(data["latest"], sep=";")
        except UnicodeDecodeError as e:
            part = pd.read_csv(data["latest"], sep=",",encoding="ISO-8859-1")
            part["lat"] = part["lat"]/100000
            part["long"] = part["long"]/100000
        caracs = pd.concat([caracs, part])
    else:
        pass

# remplacer les valeurs
caracs.an = caracs.an.replace(17, 2017).replace(18, 2018)

caracs["date"] = caracs.jour.astype("str").str.zfill(2) + "-" + caracs.mois.astype("str").str.zfill(2) + "-" + caracs.an.astype("str")
caracs["date"] = pd.to_datetime(caracs["date"], infer_datetime_format=True)

code2cat = {
    "1":"Autoroute",
    "2":"Route nationale",
    "3":"Route Départementale",
    "4":"Voie Communales",
    "5":"Hors réseau public",
    "6":"Parc de stationnement ouvert à la circulation publique",
    "7":"Routes de métropole urbaine",
    "9":"autre"
}

lieux["categorie"] = lieux.apply(lambda x: code2cat[str(x["catr"])], axis=1)

# merge dataframes
df = caracs.merge(lieux, on="Num_Acc", how="left")

# select columns
df= df[["Num_Acc", "date", "lat", "long","categorie", "vma", "plan", "lartpc", "larrout", "surf", "infra", "situ"]]

# convert lat/long to float
df["lat"] = df["lat"].str.replace(",",".").astype("float")
df["long"] = df["long"].str.replace(",",".").astype("float")

caslib = "Opendata"
save_and_format_date(df, "date", conn, "ACCIDENTS_ROUTE_CARAC_LIEUX", "ACC_ROUTE_TMP", caslib)
save_and_format_date(caracs, "date", conn, "ACCIDENTS_ROUTE_CARAC", "ACC_ROUTE_TMP", caslib)
upload_save_table(lieux, conn, "ACCIDENTS_ROUTE_LIEUX", caslib)
upload_save_table(usagers, conn, "ACCIDENTS_ROUTE_USAGERS", caslib)
upload_save_table(vehicules, conn, "ACCIDENTS_ROUTE_VEHICULES", caslib)