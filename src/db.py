import psycopg2
from psycopg2 import pool

try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20,
        user='your_user',
        password='your_password',
        host='localhost',
        port='5432',
        database='your_database'
    )
except Exception as e:
    print(f"Error connecting to database: {e}")

def get_conn():
    return connection_pool.getconn()

def release_conn(conn):
    connection_pool.putconn(conn)
