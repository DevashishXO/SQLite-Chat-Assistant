import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, db_path='data/database.sqlite'):
        self.db_path = db_path

    def execute_query(self, query):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return {"columns": columns, "data": results}
        except Error as e:
            return {"error": str(e)}