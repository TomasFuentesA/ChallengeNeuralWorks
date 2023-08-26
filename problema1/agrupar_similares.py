import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
from math import radians, cos, sin, asin, sqrt
from datetime import datetime
import db_resources
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


#Conexión a la BD
conn = db_resources.init_db()
cursor = conn.cursor()

cursor.execute("SELECT datetime, latitude_origin, longitude_origin, latitude_destination, longitude_destination FROM trips;")

data = cursor.fetchall()

def get_distance(lat_origin, long_origin, lat_destination, long_destination):
    """
    Calcula la distancia en kilómetros entre dos puntos entre
    las coordenadas de latitud y longitud de ambos puntos.

    :param lat_origin: Latitud del punto de origen en grados.
    :param long_origin: Longitud del punto de origen en grados.
    :param lat_destination: Latitud del punto de destino en grados.
    :param long_destination: Longitud del punto de destino en grados.

    :return: Distancia en kilómetros entre los dos puntos.
    """
    # Convierte las coordenadas de latitud y longitud de cadenas a números de punto flotante
    x = float(lat_origin)
    y = float(long_origin)

    x2 = float(lat_destination)
    y2 = float(long_destination)

    # Convierte las coordenadas de latitud y longitud de grados a radianes
    x = radians(x)
    x2 = radians(x2)
    y = radians(y)
    y2 = radians(y2)

    # Calcula la diferencia en longitud y latitud en radianes
    dlon = x2 - x
    dlat = y2 - y

    # Utiliza la fórmula haversine para calcular la distancia en radianes
    a = sin(dlat / 2)**2 + cos(x) * cos(x2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))

    # Radio de la Tierra en kilómetros
    r = 6371

    # Calcula la distancia final en kilómetros
    return c * r

def timestamp_to_sec(date):
    """
    Convierte una fecha en un objeto datetime en el número de segundos transcurridos desde la época Unix (1 de enero de 1970).

    :param date: Objeto datetime que se va a convertir.
    :return: Número de segundos transcurridos desde la época Unix hasta la fecha dada.
    """
    # Fecha de la época Unix (1 de enero de 1970)
    epoch_time = datetime(1970, 1, 1)

    # Resta la fecha dada (date) de la época Unix (epoch_time)
    delta = (date - epoch_time)

    # Devuelve el número total de segundos en la diferencia de tiempo (delta)
    return delta.total_seconds()

def normalize_data(dataframe):
    dataframe['timestamp_sec'] = MinMaxScaler().fit_transform(dataframe[['timestamp_sec']])
    dataframe['distance'] = MinMaxScaler().fit_transform(dataframe[['distance']])

    return dataframe
    

init_df = {
        'timestamp_sec': [],
        'distance' : []
    }

for row in data:
    date, latitude_origin, longitude_origin, latitude_destination, longitude_destination = row
    init_df['timestamp_sec'].append(timestamp_to_sec(date))
    init_df['distance'].append(get_distance(latitude_origin, longitude_origin, latitude_destination, longitude_destination))

df = pd.DataFrame(init_df)

normalized_df = normalize_data(df)

X = normalized_df.to_numpy()

kmeans = KMeans(n_clusters=4, random_state=0, n_init="auto")
labels = kmeans.fit_predict(X)
print(labels)