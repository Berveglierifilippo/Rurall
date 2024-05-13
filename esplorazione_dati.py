import pandas as pd
import geopandas as gpd

def stampa_geojson(file_geojson):
    # visualizzo tutte le colonne
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    # legge il file geojson
    mappa_agricola = gpd.read_file(file_geojson)

    # stampa tutte le righe e colonne del dataframe
    print(mappa_agricola.to_string())

