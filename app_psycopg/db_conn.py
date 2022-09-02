## DB Connection
import psycopg2
from psycopg2.extras import RealDictCursor
from sys import exit
from time import sleep
from dotenv import load_dotenv

load_dotenv()

while True:
    try: 
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres', 
            password='postgres',
            cursor_factory=RealDictCursor
        )

        cursor = conn.cursor()
        print("Database connection succesfull!")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error:", error)
        sleep(2)
