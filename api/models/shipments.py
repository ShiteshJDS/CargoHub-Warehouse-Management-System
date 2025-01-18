import sqlite3
from models.base import Base


class Shipments(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Retrieve all shipments from the database.#!#1#!#
    def get_shipments(self):
        query = "SELECT * FROM shipments"
        shipments = self.execute_query(query, fetch_all=True)
        for shipment in shipments:
            shipment["items"] = self.get_items_in_shipment(shipment["id"])
        return shipments

    # Retrieve a specific shipment by ID.#!#1#!#
    def get_shipment(self, shipment_id):
        query = "SELECT * FROM shipments WHERE id = ?"
        shipment = self.execute_query(
            query, params=(shipment_id,), fetch_one=True)
        shipment["items"] = self.get_items_in_shipment(shipment_id)
        return shipment

    # Retrieve all items in a specific shipment.#!#1#!#
    def get_items_in_shipment(self, shipment_id):
        query = "SELECT item_id, amount FROM shipment_items WHERE shipment_id = ?"
        return self.execute_query(query, params=(shipment_id,), fetch_all=True)

    # Add a new shipment to the database.
    def add_shipment(self, shipment):
        query = """
        INSERT INTO shipments (id, order_id, source_id, order_date, request_date, shipment_date, shipment_type, shipment_status, 
                            notes, carrier_code, carrier_description, service_code, payment_type, 
                            transfer_mode, total_package_count, total_package_weight, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        shipment["created_at"] = self.get_timestamp()
        shipment["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            shipment["id"], shipment["order_id"], shipment["source_id"], shipment["order_date"], shipment["request_date"],
            shipment["shipment_date"], shipment["shipment_type"], shipment["shipment_status"], shipment["notes"],
            shipment["carrier_code"], shipment["carrier_description"], shipment["service_code"], shipment["payment_type"],
            shipment["transfer_mode"], shipment["total_package_count"], shipment["total_package_weight"],
            shipment["created_at"], shipment["updated_at"]
        ))

        # Insert items into shipment_items table
        for item in shipment["items"]:
            self.execute_query(
                "INSERT INTO shipment_items (shipment_id, item_id, amount) VALUES (?, ?, ?)",
                params=(shipment["id"], item["item_id"], item["amount"])
            )

    # Update an existing shipment.
    def update_shipment(self, shipment_id, shipment):
        query = """
        UPDATE shipments SET order_id = ?, source_id = ?, order_date = ?, request_date = ?, shipment_date = ?, shipment_type = ?, 
                            shipment_status = ?, notes = ?, carrier_code = ?, carrier_description = ?, 
                            service_code = ?, payment_type = ?, transfer_mode = ?, total_package_count = ?, 
                            total_package_weight = ?, updated_at = ? WHERE id = ?
        """
        shipment["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            shipment["order_id"], shipment["source_id"], shipment["order_date"], shipment["request_date"],
            shipment["shipment_date"], shipment["shipment_type"], shipment["shipment_status"], shipment["notes"],
            shipment["carrier_code"], shipment["carrier_description"], shipment["service_code"], shipment["payment_type"],
            shipment["transfer_mode"], shipment["total_package_count"], shipment["total_package_weight"],
            shipment["updated_at"], shipment_id
        ))

        # Update items in shipment_items table
        self.update_items_in_shipment(shipment_id, shipment["items"])

    # Update items in a specific shipment.
    def update_items_in_shipment(self, shipment_id, items):
        delete_query = "DELETE FROM shipment_items WHERE shipment_id = ?"
        insert_query = """
        INSERT INTO shipment_items (shipment_id, item_id, amount) VALUES (?, ?, ?)
        """
        # Remove current items in the shipment
        self.execute_query(delete_query, params=(shipment_id,))
        # Add new items to the shipment
        for item in items:
            self.execute_query(insert_query, params=(
                shipment_id, item["item_id"], item["amount"]))

    # Delete a shipment and its associated items.
    def remove_shipment(self, shipment_id):
        delete_items_query = "DELETE FROM shipment_items WHERE shipment_id = ?"
        delete_shipment_query = "DELETE FROM shipments WHERE id = ?"
        self.execute_query(delete_items_query, params=(shipment_id,))
        self.execute_query(delete_shipment_query, params=(shipment_id,))

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
