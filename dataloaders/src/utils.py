from mysql.connector import connect
import os
import json


def get_db_connection():
    return connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "sanchay"),
    )


def check_db():
    """
    Check if the database connection is successful.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE()")
            row = cursor.fetchone()
            if row is None or len(row) == 0:
                raise ValueError("Failed to fetch database name from connection")
            db_name = row[0]
            print(f"Connected to database: {db_name}")
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise


def generate_notes(row, columns={}):
    """
    Generate notes for a bill based on the row data.
    """
    notes = {}
    for key, value in columns.items():
        if key in row and row[key] is not None:
            notes[value] = row[key]
    return json.dumps(notes) if notes else None
