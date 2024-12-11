# import json
import sqlite3
from models.base import Base

# INVENTORIES = []


class Inventories(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Retrieve all inventories from the database.
    def get_inventories(self):
        query = "SELECT * FROM inventories"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a single inventory by ID.
    def get_inventory(self, inventory_id):
        query = "SELECT * FROM inventories WHERE id = ?"
        return self.execute_query(query, params=(inventory_id,), fetch_one=True)

    # Retrieve all inventories associated with a specific item.
    def get_inventories_for_item(self, item_id):
        query = "SELECT * FROM inventories WHERE item_id = ?"
        return self.execute_query(query, params=(item_id,), fetch_all=True)

    # Retrieve total inventory details for a specific item.
    def get_inventory_totals_for_item(self, item_id):
        query = """
        SELECT SUM(total_expected) AS total_expected,
               SUM(total_ordered) AS total_ordered,
               SUM(total_allocated) AS total_allocated,
               SUM(total_available) AS total_available
        FROM inventories WHERE item_id = ?
        """
        return self.execute_query(query, params=(item_id,), fetch_one=True)

    # Add a new inventory entry.
    def add_inventory(self, inventory):
        query = """
        INSERT INTO inventories (id, item_id, description, item_reference, total_on_hand, total_expected, 
                                 total_ordered, total_allocated, total_available, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        inventory['created_at'] = self.get_timestamp()
        inventory['updated_at'] = self.get_timestamp()
        self.execute_query(query, params=(
            inventory['id'], inventory['item_id'], inventory['description'], inventory['item_reference'],
            inventory['total_on_hand'], inventory['total_expected'], inventory['total_ordered'],
            inventory['total_allocated'], inventory['total_available'], inventory['created_at'],
            inventory['updated_at']
        ))

    # Update an existing inventory entry.
    def update_inventory(self, inventory_id, inventory):
        query = """
        UPDATE inventories SET item_id = ?, description = ?, item_reference = ?, total_on_hand = ?, 
                               total_expected = ?, total_ordered = ?, total_allocated = ?, total_available = ?, 
                               updated_at = ? WHERE id = ?
        """
        inventory['updated_at'] = self.get_timestamp()
        self.execute_query(query, params=(
            inventory['item_id'], inventory['description'], inventory['item_reference'], inventory['total_on_hand'],
            inventory['total_expected'], inventory['total_ordered'], inventory['total_allocated'],
            inventory['total_available'], inventory['updated_at'], inventory_id
        ))
    
    # Delete an existing inventory entry.
    def remove_inventory(self, inventory_id):
        query = "DELETE FROM inventories WHERE id = ?"
        self.execute_query(query, params=(inventory_id,))

    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "inventories.json"
    #     self.load(is_debug)

    # def get_inventories(self):
    #     return self.data

    # def get_inventory(self, inventory_id):
    #     for x in self.data:
    #         if x["id"] == inventory_id:
    #             return x
    #     return None

    # def get_inventories_for_item(self, item_id):
    #     result = []
    #     for x in self.data:
    #         if x["item_id"] == item_id:
    #             result.append(x)
    #     return result

    # def get_inventory_totals_for_item(self, item_id):
    #     result = {
    #         "total_expected": 0,
    #         "total_ordered": 0,
    #         "total_allocated": 0,
    #         "total_available": 0
    #     }
    #     for x in self.data:
    #         if x["item_id"] == item_id:
    #             result["total_expected"] += x["total_expected"]
    #             result["total_ordered"] += x["total_ordered"]
    #             result["total_allocated"] += x["total_allocated"]
    #             result["total_available"] += x["total_available"]
    #     return result

    # def add_inventory(self, inventory):
    #     inventory["created_at"] = self.get_timestamp()
    #     inventory["updated_at"] = self.get_timestamp()
    #     self.data.append(inventory)

    # def update_inventory(self, inventory_id, inventory):
    #     inventory["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == inventory_id:
    #             self.data[i] = inventory
    #             break

    # def remove_inventory(self, inventory_id):
    #     for x in self.data:
    #         if x["id"] == inventory_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = INVENTORIES
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
