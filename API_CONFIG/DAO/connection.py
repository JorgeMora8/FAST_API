import psycopg2
from psycopg2.extras import RealDictCursor

connection = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="08012002", cursor_factory=RealDictCursor)
cursor = connection.cursor()




class ConnectDB: 
        connection = connection
        cursor = cursor