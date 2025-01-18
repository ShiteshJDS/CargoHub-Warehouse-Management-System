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
                row = cursor.fetchone()
                # Return None if no row is found
                return dict(row) if row else None

            if fetch_all:
                rows = cursor.fetchall()
                # Return an empty list if no rows are found
                return [dict(row) for row in rows] if rows else []

            return None
