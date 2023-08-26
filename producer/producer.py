from kafka import KafkaProducer
import json
import pandas as pd
import time

producer = KafkaProducer(bootstrap_servers='kafka:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))

df = pd.read_csv('trips.csv').sort_values(by='datetime')



try:
    # Itera y envía cada fila como un diccionario JSON
    producer.send('test', value={'message': 'Ingesta de datos iniciada'})
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
      time.sleep(1)
    producer.send('test', value={'message': 'Ingesta de datos completada'})
except KeyboardInterrupt:
    producer.send('test', value={'message': 'Interrupción de teclado detectada. Enviando mensaje de ingesta interrumpida...'})
finally:
    # Cierra el productor
    producer.close()

