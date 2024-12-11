# import json
import sqlite3
from models.base import Base

# SHIPMENTS = []


class Shipments(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Helper method to interact with the database.
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Helper method to interact with the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()

    # Retrieve all shipments from the database.
    def get_shipments(self):
        query = "SELECT * FROM shipments"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a specific shipment by ID.
    def get_shipment(self, shipment_id):
        query = "SELECT * FROM shipments WHERE id = ?"
        return self.execute_query(query, params=(shipment_id,), fetch_one=True)

    # Retrieve all items in a specific shipment.
    def get_items_in_shipment(self, shipment_id):
        query = "SELECT * FROM shipment_items WHERE shipment_id = ?"
        return self.execute_query(query, params=(shipment_id,), fetch_all=True)

    # Add a new shipment to the database.
    def add_shipment(self, shipment):
        query = """
        INSERT INTO shipments (id, order_id, source_id, shipment_date, shipment_type, shipment_status, 
                               notes, carrier_code, carrier_description, service_code, payment_type, 
                               transfer_mode, total_package_count, total_package_weight, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        shipment["created_at"] = self.get_timestamp()
        shipment["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            shipment["id"], shipment["order_id"], shipment["source_id"], shipment["shipment_date"],
            shipment["shipment_type"], shipment["shipment_status"], shipment["notes"], shipment["carrier_code"],
            shipment["carrier_description"], shipment["service_code"], shipment["payment_type"],
            shipment["transfer_mode"], shipment["total_package_count"], shipment["total_package_weight"],
            shipment["created_at"], shipment["updated_at"]
        ))

    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "shipments.json"
    #     self.load(is_debug)

    # def get_shipments(self):
    #     return self.data

    # def get_shipment(self, shipment_id):
    #     for x in self.data:
    #         if x["id"] == shipment_id:
    #             return x
    #     return None

    # def get_items_in_shipment(self, shipment_id):
    #     for x in self.data:
    #         if x["id"] == shipment_id:
    #             return x["items"]
    #     return None

    # def add_shipment(self, shipment):
    #     shipment["created_at"] = self.get_timestamp()
    #     shipment["updated_at"] = self.get_timestamp()
    #     self.data.append(shipment)

    # def update_shipment(self, shipment_id, shipment):
    #     shipment["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == shipment_id:
    #             self.data[i] = shipment
    #             break

    # def update_items_in_shipment(self, shipment_id, items):
    #     from providers import data_provider
    #     shipment = self.get_shipment(shipment_id)
    #     current = shipment["items"]
    #     for x in current:
    #         found = False
    #         for y in items:
    #             if x["item_id"] == y["item_id"]:
    #                 found = True
    #                 break
    #         if not found:
    #             inventories = data_provider.fetch_inventory_pool(
    #             ).get_inventories_for_item(x["item_id"])
    #             max_ordered = -1
    #             max_inventory
    #             for z in inventories:
    #                 if z["total_ordered"] > max_ordered:
    #                     max_ordered = z["total_ordered"]
    #                     max_inventory = z
    #             max_inventory["total_ordered"] -= x["amount"]
    #             max_inventory["total_expected"] = y["total_on_hand"] + \
    #                 y["total_ordered"]
    #             data_provider.fetch_inventory_pool().update_inventory(
    #                 max_inventory["id"], max_inventory)
    #     for x in current:
    #         for y in items:
    #             if x["item_id"] == y["item_id"]:
    #                 inventories = data_provider.fetch_inventory_pool(
    #                 ).get_inventories_for_item(x["item_id"])
    #                 max_ordered = -1
    #                 max_inventory
    #                 for z in inventories:
    #                     if z["total_ordered"] > max_ordered:
    #                         max_ordered = z["total_ordered"]
    #                         max_inventory = z
    #                 max_inventory["total_ordered"] += y["amount"] - x["amount"]
    #                 max_inventory["total_expected"] = y["total_on_hand"] + \
    #                     y["total_ordered"]
    #                 data_provider.fetch_inventory_pool().update_inventory(
    #                     max_inventory["id"], max_inventory)
    #     shipment["items"] = items
    #     self.update_shipment(shipment_id, shipment)

    # def remove_shipment(self, shipment_id):
    #     for x in self.data:
    #         if x["id"] == shipment_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = SHIPMENTS
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
