# connect.py
import psycopg2
from config import conn_params

def get_connection():
    conn = psycopg2.connect(**conn_params)
    return conn

def init_db():
    """Initialize database with schema"""
    conn = get_connection()
    cur = conn.cursor()
    
    with open('schema.sql', 'r') as f:
        cur.execute(f.read())
    
    conn.commit()
    cur.close()
    conn.close()