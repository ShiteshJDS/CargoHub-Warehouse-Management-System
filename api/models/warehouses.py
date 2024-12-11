# import json
import sqlite3
from models.base import Base

# WAREHOUSES = []


class Warehouses(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Retrieve all warehouses from the database
    def get_warehouses(self):
        query = "SELECT * FROM warehouses"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a specific warehouse by ID
    def get_warehouse(self, warehouse_id):
        query = "SELECT * FROM warehouses WHERE id = ?"
        return self.execute_query(query, params=(warehouse_id,), fetch_one=True)

    # Add a new warehouse to the database
    def add_warehouse(self, warehouse):
        query = """
        INSERT INTO warehouses (id, code, name, address, zip, city, province, country, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        warehouse["created_at"] = self.get_timestamp()
        warehouse["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            warehouse["id"], warehouse["code"], warehouse["name"], warehouse["address"], warehouse["zip"],
            warehouse["city"], warehouse["province"], warehouse["country"], warehouse["created_at"],
            warehouse["updated_at"]
        ))

    # Update an existing warehouse
    def update_warehouse(self, warehouse_id, warehouse):
        query = """
        UPDATE warehouses SET code = ?, name = ?, address = ?, zip = ?, city = ?, province = ?, country = ?, 
                              updated_at = ? WHERE id = ?
        """
        warehouse["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            warehouse["code"], warehouse["name"], warehouse["address"], warehouse["zip"],
            warehouse["city"], warehouse["province"], warehouse["country"], warehouse["updated_at"], warehouse_id
        ))

    # Delete a warehouse from the database by ID
    def remove_warehouse(self, warehouse_id):
        query = "DELETE FROM warehouses WHERE id = ?"
        self.execute_query(query, params=(warehouse_id,))


    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "warehouses.json"
    #     self.load(is_debug)

    # def get_warehouses(self):
    #     return self.data

    # def get_warehouse(self, warehouse_id):
    #     for x in self.data:
    #         if x["id"] == warehouse_id:
    #             return x
    #     return None

    # def add_warehouse(self, warehouse):
    #     warehouse["created_at"] = self.get_timestamp()
    #     warehouse["updated_at"] = self.get_timestamp()
    #     self.data.append(warehouse)

    # def update_warehouse(self, warehouse_id, warehouse):
    #     warehouse["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == warehouse_id:
    #             self.data[i] = warehouse
    #             break

    # def remove_warehouse(self, warehouse_id):
    #     for x in self.data:
    #         if x["id"] == warehouse_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = WAREHOUSES
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
