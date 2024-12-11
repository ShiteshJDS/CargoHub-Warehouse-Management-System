# import json
import sqlite3
from models.base import Base

# SUPPLIERS = []


class Suppliers(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Retrieve all suppliers from the database
    def get_suppliers(self):
        query = "SELECT * FROM suppliers"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a specific supplier by ID
    def get_supplier(self, supplier_id):
        query = "SELECT * FROM suppliers WHERE id = ?"
        return self.execute_query(query, params=(supplier_id,), fetch_one=True)

    # Add a new supplier to the database
    def add_supplier(self, supplier):
        query = """
        INSERT INTO suppliers (id, code, name, address, address_extra, city, zip_code, province, country, 
                               contact_name, phonenumber, reference, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        supplier["created_at"] = self.get_timestamp()
        supplier["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            supplier["id"], supplier["code"], supplier["name"], supplier["address"], supplier.get("address_extra", ""),
            supplier["city"], supplier["zip_code"], supplier["province"], supplier["country"],
            supplier["contact_name"], supplier["phonenumber"], supplier["reference"],
            supplier["created_at"], supplier["updated_at"]
        ))

    # Update an existing supplier in the database
    def update_supplier(self, supplier_id, supplier):
        query = """
        UPDATE suppliers SET code = ?, name = ?, address = ?, address_extra = ?, city = ?, zip_code = ?, 
                             province = ?, country = ?, contact_name = ?, phonenumber = ?, reference = ?, 
                             updated_at = ? WHERE id = ?
        """
        supplier["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            supplier["code"], supplier["name"], supplier["address"], supplier.get("address_extra", ""),
            supplier["city"], supplier["zip_code"], supplier["province"], supplier["country"],
            supplier["contact_name"], supplier["phonenumber"], supplier["reference"],
            supplier["updated_at"], supplier_id
        ))

    # Delete a supplier from the database by ID
    def remove_supplier(self, supplier_id):
        query = "DELETE FROM suppliers WHERE id = ?"
        self.execute_query(query, params=(supplier_id,))

    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "suppliers.json"
    #     self.load(is_debug)

    # def get_suppliers(self):
    #     return self.data

    # def get_supplier(self, supplier_id):
    #     for x in self.data:
    #         if x["id"] == supplier_id:
    #             return x
    #     return None

    # def add_supplier(self, supplier):
    #     supplier["created_at"] = self.get_timestamp()
    #     supplier["updated_at"] = self.get_timestamp()
    #     self.data.append(supplier)

    # def update_supplier(self, supplier_id, supplier):
    #     supplier["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == supplier_id:
    #             self.data[i] = supplier
    #             break

    # def remove_supplier(self, supplier_id):
    #     for x in self.data:
    #         if x["id"] == supplier_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = SUPPLIERS
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
