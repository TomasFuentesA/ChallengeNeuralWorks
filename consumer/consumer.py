from kafka import KafkaConsumer
import json
import re
import db_resources
import pandas as pd



def get_x_y_cord(row):
    """
    Extrae las coordenadas en formato POINT (x y) de una cadena y las devuelve como una tupla (x, y).

    :param row: Cadena que representa coordenadas en formato POINT (x y).
    :return: Tupla (x, y) que contiene las coordenadas extraídas.
    """
    # Utiliza una expresión regular para encontrar todas las coincidencias de números en la cadena.
    matches = re.findall(r'[-+]?\d*\.\d+|\d+', row)

    # Extrae las coordenadas x e y de las coincidencias encontradas.
    x = float(matches[0])
    y = float(matches[1])

    # Devuelve las coordenadas como una tupla (x, y).
    return (x, y)

#Conexión a la BD
conn = db_resources.init_db()
cursor = conn.cursor()

# Configura el consumidor de Kafka
consumer = KafkaConsumer('test', bootstrap_servers='kafka:9092', value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Escucha eventos del producer
for event in consumer:
    
    if 'message' in event.value:
        # Este es un mensaje de estado, puedes manejarlo de acuerdo a tus necesidades.
        state_message = event.value['message']
        if state_message == 'Ingesta de datos iniciada':
            print(state_message)
            pass
        elif state_message == 'Ingesta de datos completada':
            print(state_message)
            consumer.close()
            pass
        elif state_message == 'Interrupción de teclado detectada. Enviando mensaje de ingesta interrumpida...':
            print(state_message)
            consumer.close()
            pass
    else:
        print(event.value)
        lat_origin, long_origin = get_x_y_cord(event.value['origin_coord'])
        lat_destination, long_destination = get_x_y_cord(event.value['destination_coord'])
        cursor.execute("INSERT INTO trips (region, latitude_origin, longitude_origin, latitude_destination, longitude_destination, datetime, datasource) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                        (event.value['region'], lat_origin, long_origin, lat_destination, long_destination, pd.to_datetime(event.value['datetime']), event.value['datasource']))
        conn.commit()