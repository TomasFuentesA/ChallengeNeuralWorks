from psycopg2 import connect

def init_db():
    """
    args= No recibe
    return= retorna la conexion a la bd
    """
    conn = connect(
        host="postgres",
        dbname="challengeNW",
        password="postgres",
        port=5432,
        user="postgres"
    )
    return conn