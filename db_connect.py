import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():

    try:
        connection = psycopg2.connect(

            host=os.getenv("DB_HOST"),

            database=os.getenv("DB_NAME"),

            user=os.getenv("DB_USER"),

            password=os.getenv("DB_PASSWORD"),

            port=os.getenv("DB_PORT", "5432")
        )

        print("Connection established successfully")

        return connection

    except Exception as e:

        print("DATABASE ERROR:", e)

        return None