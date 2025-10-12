# test_connection.py
from database.db_connection import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("Database connected successfully!")
        for row in result:
            print(row)
except Exception as e:
    print("Connection failed:", e)
