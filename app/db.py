import sqlite3
from sqlite3 import Error
from .utils import validate_sql
import logging

class Database:
    def __init__(self, db_path='data/database.sqlite'):
        self.db_path = db_path

    def execute_query(self, query):
        logging.info(f"Executing SQL: {query}")
        if not validate_sql(query):
            return {"error": "Invalid SQL query. Only SELECT queries are allowed at this point."}
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return {"columns": columns, "data": results}
        except Error as e:
            logging.error(f"SQL Error: {str(e)}")
            return {"error": str(e)}