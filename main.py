import pandas as pd
import geopandas as gpd
from esplorazione_dati import stampa_geojson
from pulizia_dati import separa_data_ora, formatta_colonne, datetime, elimina_nan
from interpolazione_idw import interpolazione_idw_wrapper


def main():
    file_geojson = "resa_girasole_2022.geojson"

    # leggo il file jsom
    print(f"Lettura del file '{file_geojson}' in corso...")

    print("\nSeparazione della colonna 'Data/Ora' in corso...")
    file_modificato = separa_data_ora(file_geojson)

    print("\nFormattazione delle colonne in corso...")
    formatta_colonne(file_modificato)

    print("\nCreazione colonna datetime in corso...")
    file_modificato = datetime(file_modificato)

    print("\nEliminazione righe con valori NaN...")
    elimina_nan(file_modificato)

    # stampa il dataframe pulito
    print("\nModifica completata. Visualizzazione del DataFrame modificato:")
    stampa_geojson(file_modificato)

    gdf = gpd.read_file(file_modificato)

    # inserire i punti da interpolare

    punti_interpolazione = [
        [44.50497, 11.57541],
        [44.847223, 11.977560],
        [44.843056, 11.965127],
        [44.843149, 11.977643]
    ]

    # Eseguire l'interpolazione
    try:
        valori_interpolati = interpolazione_idw_wrapper(gdf, punti_interpolazione, power=2)  # Specifica il valore di power
        for i, punto in enumerate(punti_interpolazione):
            print(f"Valori interpolati nel punto {punto}: {valori_interpolati[i]}")
    except ValueError as e:
        print("Si è verificato un errore durante l'interpolazione:", e)

    numeric_columns = gdf.select_dtypes(include=['float64', 'int64']).columns
    correlation_matrix = gdf[numeric_columns].corr()
    print("\nMatrice di correlazione:")
    print(correlation_matrix)

if __name__ == "__main__":
    main()
