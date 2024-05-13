import numpy as np
from scipy.spatial.distance import cdist

def interpolazione_idw_wrapper(gdf, punti_interpolazione, power):
    # estraggo i punti noti e i valori ottenuti in quei punti
    punti_noto = gdf[['Longitudin', 'Latitudine']].values
    valori_noto = gdf[['RESAKG', 'VELOCITA', 'UMIDITA', 'AREA']].values

    # trovo le distanze tra i punti noti e i punti da interpolare
    distances = cdist(punti_interpolazione, punti_noto)

    # calcoliamo i valori interpolati per ciascuna variabile di interesse
    valori_interpolati = []
    for i in range(valori_noto.shape[1]):
        # calcolo dei pesi utilizzando la distanza inversa
        weights = 1 / (distances ** power)

        # somma dei pesi
        total_weight = np.sum(weights, axis=1)

        # formula per il calcolo dei valori interpolati
        interpolated_values = np.sum(valori_noto[:, i] * weights, axis=1) / total_weight

        # li aggiungo alla lista
        valori_interpolati.append(interpolated_values)

    return valori_interpolati
