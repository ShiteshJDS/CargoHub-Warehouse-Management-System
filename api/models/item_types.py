# import json
import sqlite3
from models.base import Base

# ITEM_TYPES = []


class ItemTypes(Base):
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

    # Retrieve all item types from the database.
    def get_item_types(self):
        query = "SELECT * FROM item_types"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a single item type by ID.
    def get_item_type(self, item_type_id):
        query = "SELECT * FROM item_types WHERE id = ?"
        return self.execute_query(query, params=(item_type_id,), fetch_one=True)


    # Add a new item type to the database.
    def add_item_type(self, item_type):
        query = """
        INSERT INTO item_types (id, name, description, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?)
        """
        item_type["created_at"] = self.get_timestamp()
        item_type["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            item_type["id"], item_type["name"], item_type["description"],
            item_type["created_at"], item_type["updated_at"]
        ))

    # Update an existing item type.
    def update_item_type(self, item_type_id, item_type):
        query = """
        UPDATE item_types SET name = ?, description = ?, updated_at = ? 
        WHERE id = ?
        """
        item_type["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            item_type["name"], item_type["description"],
            item_type["updated_at"], item_type_id
        ))

    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "item_types.json"
    #     self.load(is_debug)

    # def get_item_types(self):
    #     return self.data

    # def get_item_type(self, item_type_id):
    #     for x in self.data:
    #         if x["id"] == item_type_id:
    #             return x
    #     return None

    # def add_item_type(self, item_type):
    #     item_type["created_at"] = self.get_timestamp()
    #     item_type["updated_at"] = self.get_timestamp()
    #     self.data.append(item_type)

    # def update_item_type(self, item_type_id, item_type):
    #     item_type["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == item_type_id:
    #             self.data[i] = item_type
    #             break

    # def remove_item_type(self, item_type_id):
    #     for x in self.data:
    #         if x["id"] == item_type_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = ITEM_TYPES
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
