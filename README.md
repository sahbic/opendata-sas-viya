# opendata-sas-viya

This projects aims to provide, scripts and flows that continously fetch Datasets from the Open Data into SAS Viya.

## Datasets

- [Road accidents in France](https://www.data.gouv.fr/fr/datasets/bases-de-donnees-annuelles-des-accidents-corporels-de-la-circulation-routiere-annees-de-2005-a-2021/)
- [Natural disasters in France](https://www.georisques.gouv.fr/donnees/bases-de-donnees/base-gaspar)
- [Emissions of vehicles marketed in France](https://carlabelling.ademe.fr/)

## Set up

1. Run `1_Initialize.flw` to initialize the environment.
2. Run `2_Get_Data.flw` to fetch the datasets.