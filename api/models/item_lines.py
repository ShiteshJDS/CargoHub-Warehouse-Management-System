# import json
import sqlite3
from models.base import Base

# ITEM_LINES = []


class ItemLines(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Helper method to interact with the database.
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()

    # Retrieve all item lines from the database.
    def get_item_lines(self):
        query = "SELECT * FROM item_lines"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a single item line by ID.
    def get_item_line(self, item_line_id):
        query = "SELECT * FROM item_lines WHERE id = ?"
        return self.execute_query(query, params=(item_line_id,), fetch_one=True)

    # Add a new item line to the database.
    def add_item_line(self, item_line):
        query = """
        INSERT INTO item_lines (id, name, description, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?)
        """
        item_line["created_at"] = self.get_timestamp()
        item_line["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            item_line["id"], item_line["name"], item_line["description"],
            item_line["created_at"], item_line["updated_at"]
        ))

    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "item_lines.json"
    #     self.load(is_debug)

    # def get_item_lines(self):
    #     return self.data

    # def get_item_line(self, item_line_id):
    #     for x in self.data:
    #         if x["id"] == item_line_id:
    #             return x
    #     return None

    # def add_item_line(self, item_line):
    #     item_line["created_at"] = self.get_timestamp()
    #     item_line["updated_at"] = self.get_timestamp()
    #     self.data.append(item_line)

    # def update_item_line(self, item_line_id, item_line):
    #     item_line["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == item_line_id:
    #             self.data[i] = item_line
    #             break

    # def remove_item_line(self, item_line_id):
    #     for x in self.data:
    #         if x["id"] == item_line_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = ITEM_LINES
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
