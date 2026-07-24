import psycopg2
def get_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database="startup_funding",
            user="postgres",
            password="*******"
        )
        print("Connection established successfully")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None
if __name__ == "__main__":
    conn = get_connection()

    if conn:
        print("Database connection is working!")
        conn.close()
        print("Connection closed.")
