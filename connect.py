import mysql.connector
from mysql.connector import Error
import os

database_config = {
    "host": "localhost"
}

def connect_to_sql():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "budget_application"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "Dahyunfan19!")
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection

    except Error as e:
        print(f"Database connection error: {e}")
        return None