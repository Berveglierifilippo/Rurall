import geopandas as gpd
import pandas as pd

def datetime(file_geojson):
    # legge il file geojson
    gdf = gpd.read_file(file_geojson)

    # traduco i mesi nella colonna data
    month_translation = {
        'gen': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'apr': 'Apr', 'mag': 'May', 'giu': 'Jun',
        'lug': 'Jul', 'ago': 'Aug', 'set': 'Sep', 'ott': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
    }

    # applico la traduzione dei mesi
    gdf['Data'] = gdf['Data'].str.lower().replace(month_translation, regex=True)

    # creo la colonna datetime combinando data e ora
    gdf['Datetime'] = pd.to_datetime(gdf['Data'] + ' ' + gdf['Ora'], format='%d %b %Y %H:%M:%S')

    # rimuovo le vecchie colonne "data" e "ora"
    gdf.drop(columns=['Data', 'Ora'], inplace=True)

    # salvo il dataframe modificato in un altro file
    new_file = file_geojson.split('.')[0] + '_modificato.geojson'
    gdf.to_file(new_file, driver='GeoJSON', index=False)

    return new_file


def elimina_nan(file_geojson):
    gdf = gpd.read_file(file_geojson)

    # tolgo i valori nan dalla colonna umidità
    gdf.dropna(subset=['UMIDITA'], inplace=True)

    # salvataggio del geojson esistente
    gdf.to_file(file_geojson, driver='GeoJSON', index=False)


def separa_data_ora(file_geojson):
    gdf = gpd.read_file(file_geojson)

    # separa la colonna data/ora del geojson iniziale in due colonne data e ora separate
    gdf[['Data', 'Ora']] = gdf['Data/Ora'].str.split(', ', expand=True)

    # toglie la colonna "data/ora" inziale
    gdf.drop(columns=['Data/Ora'], inplace=True)

    new_file = file_geojson.split('.')[0] + '_modificato.geojson'
    gdf.to_file(new_file, driver='GeoJSON')

    return new_file

def formatta_colonne(file_geojson):
    # Leggi il file GeoJSON modificato
    gdf = gpd.read_file(file_geojson)

    # Formatta le colonne "Latitudine" e "Longitudine"
    gdf['Latitudine'] = gdf['Latitudine'].str.replace(',', '.').astype(float)
    gdf['Longitudin'] = gdf['Longitudin'].str.replace(',', '.').astype(float)

    gdf.to_file(file_geojson, driver='GeoJSON', index=False)


if __name__ == "__main__":
    file_geojson = "resa_girasole_2022.geojson"
    separa_data_ora(file_geojson)