# import json
import sqlite3
from models.base import Base

# ITEMS = []


class Items(Base):
    def __init__(self, db_path):
        self.db_path = db_path

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

    # Retrieve all items from the database
    def get_items(self):
        query = "SELECT * FROM items"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a single item by UID
    def get_item(self, item_id):
        query = "SELECT * FROM items WHERE uid = ?"
        return self.execute_query(query, params=(item_id,), fetch_one=True)

    # Retrieve items associated with a specific item line
    def get_items_for_item_line(self, item_line_id):
        query = "SELECT * FROM items WHERE item_line_id = ?"
        return self.execute_query(query, params=(item_line_id,), fetch_all=True)

    # Retrieve items associated with a specific item group
    def get_items_for_item_group(self, item_group_id):
        query = "SELECT * FROM items WHERE item_group_id = ?"
        return self.execute_query(query, params=(item_group_id,), fetch_all=True)

    # Retrieve items associated with a specific item type
    def get_items_for_item_type(self, item_type_id):
        query = "SELECT * FROM items WHERE item_type_id = ?"
        return self.execute_query(query, params=(item_type_id,), fetch_all=True)

    # Retrieve items associated with a specific supplier
    def get_items_for_supplier(self, supplier_id):
        query = "SELECT * FROM items WHERE supplier_id = ?"
        return self.execute_query(query, params=(supplier_id,), fetch_all=True)


    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "items.json"
    #     self.load(is_debug)

    # def get_items(self):
    #     return self.data

    # def get_item(self, item_id):
    #     for x in self.data:
    #         if x["uid"] == item_id:
    #             return x
    #     return None

    # def get_items_for_item_line(self, item_line_id):
    #     result = []
    #     for x in self.data:
    #         if x["item_line"] == item_line_id:
    #             result.append(x)
    #     return result

    # def get_items_for_item_group(self, item_group_id):
    #     result = []
    #     for x in self.data:
    #         if x["item_group"] == item_group_id:
    #             result.append(x)
    #     return result

    # def get_items_for_item_type(self, item_type_id):
    #     result = []
    #     for x in self.data:
    #         if x["item_type"] == item_type_id:
    #             result.append(x)
    #     return result

    # def get_items_for_supplier(self, supplier_id):
    #     result = []
    #     for x in self.data:
    #         if x["supplier_id"] == supplier_id:
    #             result.append(x)
    #     return result

    # def add_item(self, item):
    #     item["created_at"] = self.get_timestamp()
    #     item["updated_at"] = self.get_timestamp()
    #     self.data.append(item)

    # def update_item(self, item_id, item):
    #     item["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["uid"] == item_id:
    #             self.data[i] = item
    #             break

    # def remove_item(self, item_id):
    #     for x in self.data:
    #         if x["uid"] == item_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = ITEMS
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
