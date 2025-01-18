import datetime
import sqlite3


class Base:
    def __init__():
        pass

    def get_timestamp(self):
        return datetime.datetime.now(datetime.UTC).isoformat(" ", "seconds")

    # Helper method to interact with the database
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        with sqlite3.connect(self.db_path) as conn:
            # Use sqlite3.Row to enable dictionary-like access
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()
            if fetch_one:
                return dict(cursor.fetchone())
            if fetch_all:
                return [dict(row) for row in cursor.fetchall()]
