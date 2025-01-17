# import json
import sqlite3
from models.base import Base

# ITEM_GROUPS = []


class ItemGroups(Base):
    def __init__(self, db_path):
        self.db_path = db_path
        self.tablename = "item_groups"

    # Retrieve all item groups from the database.#!#1#!#
    def get_item_groups(self):
        query = "SELECT * FROM item_groups"
        return self.execute_query(query, fetch_all=True)

    # Retrieve all item groups from the database.#!#1#!#
    def get_item_group(self, item_group_id):
        query = "SELECT * FROM item_groups WHERE id = ?"
        return self.execute_query(query, params=(item_group_id,), fetch_one=True)

    # Add a new item group to the database.
    def add_item_group(self, item_group):
        query = """
        INSERT INTO item_groups (id, name, description, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?)
        """
        item_group["created_at"] = self.get_timestamp()
        item_group["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            item_group["id"], item_group["name"], item_group["description"],
            item_group["created_at"], item_group["updated_at"]
        ))

    # Update an existing item group.
    def update_item_group(self, item_group_id, item_group):
        query = """
        UPDATE item_groups SET name = ?, description = ?, updated_at = ? 
        WHERE id = ?
        """
        item_group["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            item_group["name"], item_group["description"],
            item_group["updated_at"], item_group_id
        ))

    # Delete an item group from the database.
    def remove_item_group(self, item_group_id):
        query = "DELETE FROM item_groups WHERE id = ?"
        self.execute_query(query, params=(item_group_id,))

    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "item_groups.json"
    #     self.load(is_debug)

    # def get_item_groups(self):
    #     return self.data

    # def get_item_group(self, item_group_id):
    #     for x in self.data:
    #         if x["id"] == item_group_id:
    #             return x
    #     return None

    # def add_item_group(self, item_group):
    #     item_group["created_at"] = self.get_timestamp()
    #     item_group["updated_at"] = self.get_timestamp()
    #     self.data.append(item_group)

    # def update_item_group(self, item_group_id, item_group):
    #     item_group["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == item_group_id:
    #             self.data[i] = item_group
    #             break

    # def remove_item_group(self, item_group_id):
    #     for x in self.data:
    #         if x["id"] == item_group_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = ITEM_GROUPS
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
