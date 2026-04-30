import mysql.connector
from mysql.connector import Error

def connect_to_sql():
    try:
        connection = mysql.connector.connect(
            host="shuttle.proxy.rlwy.net",
            port=18649,
            user="root",
            password="DaMOizkYDeMrZekwwoGDhqjFgCAVcUxD",
            database="railway"
        )

        if connection.is_connected():
            print("Connected to MySQL database")
            return connection

    except Error as e:
        print(f"Database connection error: {e}")
        return None