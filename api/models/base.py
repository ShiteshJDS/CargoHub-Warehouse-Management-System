from datetime import datetime
import sqlite3


class Base:
    def __init__():
        pass

    def get_timestamp(self):
        return datetime.utcnow().isoformat(" ", "seconds")

    # Helper method to interact with the database
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()

    def query_to_dict(self, database_tuple):
        rowquery = f"PRAGMA table_info({self.tablename})"
        table_rows = [row[1]
                      for row in self.execute_query(rowquery, fetch_all=True)]
        result = [dict(zip(table_rows, value)) for value in database_tuple]
        if len(database_tuple) == 1:
            return result[0]
        return result
