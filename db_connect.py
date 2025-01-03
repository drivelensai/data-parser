
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
# Load environment variables from .env
load_dotenv()

# Настройки подключения к MySQL

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}


def connect_to_db():
    """Подключение к базе данных."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Подключено к базе данных")
        return connection
    except Error as e:
        print(f"Ошибка подключения: {e}")
        return None
