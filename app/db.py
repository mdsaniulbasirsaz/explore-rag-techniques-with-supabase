import psycopg2
import os
from dotenv import load_dotenv
from app.logger import logger

load_dotenv()


try:
    connection = psycopg2.connect(os.getenv("SUPABASE_DB_URL"))
    logger.info("Database connection established successfully.")
except Exception as e:
    logger.error(f"Error connecting to the database: {e}")

def get_cursor():
    return connection.cursor()
