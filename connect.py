import mysql.connector
from mysql.connector import Error

def connect_to_sql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='budget_application',
            user='root',
            password='Dahyunfan19!'
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection

    except Error as e:
        print(f"Error: {e}")
        return None