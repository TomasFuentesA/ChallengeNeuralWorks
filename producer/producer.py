from kafka import KafkaProducer
import json
import pandas as pd



producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

df = pd.read_csv('trips.csv').sort_values(by='datetime')

# Itera a través de las filas y envía cada fila como un diccionario JSON
for _, row in df.iterrows():
    
    # Crea un diccionario con los datos de la fila
    data = {
        'region': row['region'],
        'origin_coord': row['origin_coord'],
        'destination_coord': row['destination_coord'],
        'datetime': row['datetime'],
        'datasource': row['datasource']
    }
    
    # Envía el diccionario como un mensaje JSON a Kafka
    producer.send('test', value=data)

# Cierra el productor
producer.close()
