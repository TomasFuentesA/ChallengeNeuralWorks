import db_resources

def get_weekly_mean(cursor, region, lat_origin, long_origin, lat_destination, long_destination):
    """
    Calcula el promedio semanal de viajes en una región dentro de un rango geográfico.

    Parámetros:
    cursor (psycopg2.cursor): Cursor de la base de datos PostgreSQL.
    region (str): Nombre de la región de interés.
    lat_origin (float): Latitud mínima de origen.
    long_origin (float): Longitud mínima de origen.
    lat_destination (float): Latitud máxima de destino.
    long_destination (float): Longitud máxima de destino.

    Retorna:
    pd.Series: Una serie de Pandas que contiene el promedio semanal de viajes.
    """

    #Conexión a la BD
    conn = db_resources.init_db()
    cursor = conn.cursor()

    # Ejecuta la consulta SQL para obtener los datos de la región y rango geográfico.
    cursor.execute("""
            SELECT region, datetime 
            FROM trips 
            WHERE region = %s 
            AND latitude_origin >= %s 
            AND longitude_origin >= %s 
            AND latitude_destination <= %s 
            AND longitude_destination <= %s;
            """,
       (region, lat_origin, long_origin, lat_destination, long_destination))

    # Obtiene los datos de la consulta.
    data = cursor.fetchall()

    # Si no se encontraron datos, devuelve 0.
    if len(data) == 0:
        return pd.Series([0])

    # Crea un DataFrame inicial con los datos de la consulta.
    init_data = {
        'region': [fila[0] for fila in data],
        'timestamp': [fila[1] for fila in data]
    }
    init_df = pd.DataFrame(init_data)

    # Convierte la columna 'timestamp' a tipo datetime.
    init_df['timestamp'] = pd.to_datetime(init_df['timestamp'])

    # Ordena el DataFrame por la columna 'timestamp'.
    init_df = init_df.sort_values(by='timestamp')

    # Resamplea el DataFrame a semanas y calcula el conteo semanal de viajes.
    conteo_semanal = init_df.resample('W', on='timestamp').count()

    # Calcula el promedio semanal dividiendo el conteo semanal por 7.
    promedio_semanal = conteo_semanal['region'] / 7

    return promedio_semanal