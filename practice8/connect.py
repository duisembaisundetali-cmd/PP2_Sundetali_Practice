import psycopg2
from config import conn_params

def get_connection():
    conn = psycopg2.connect(**conn_params)
    return conn