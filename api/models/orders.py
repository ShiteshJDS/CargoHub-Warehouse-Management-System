# import json
import sqlite3
from models.base import Base

# ORDERS = []


class Orders(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Retrieve all orders from the database.
    def get_orders(self):
        query = "SELECT * FROM orders"
        orders = self.execute_query(query, fetch_all=True)
        return [self.format_order(order) for order in orders]

    # Retrieve a specific order by ID.
    def get_order(self, order_id):
        query = "SELECT * FROM orders WHERE id = ?"
        order = self.execute_query(query, params=(order_id,), fetch_one=True)
        if order:
            order_dict = self.format_order(order)
            order_dict["items"] = self.get_items_in_order(order_id)
            return order_dict
        return None

    # Retrieve all items in a specific order.
    def get_items_in_order(self, order_id):
        query = "SELECT item_id, amount FROM order_items WHERE order_id = ?"
        items = self.execute_query(query, params=(order_id,), fetch_all=True)
        return [{"item_id": item[0], "amount": item[1]} for item in items]

    # Format order as a dictionary.
    def format_order(self, order):
        return {
            "id": order[0],
            "source_id": order[1],
            "order_date": order[2],
            "request_date": order[3],
            "reference": order[4],
            "reference_extra": order[5],
            "order_status": order[6],
            "notes": order[7],
            "shipping_notes": order[8],
            "picking_notes": order[9],
            "warehouse_id": order[10],
            "ship_to": order[11],
            "bill_to": order[12],
            "shipment_id": order[13],
            "total_amount": order[14],
            "total_discount": order[15],
            "total_tax": order[16],
            "total_surcharge": order[17],
            "created_at": order[18],
            "updated_at": order[19]
        }

    # Retrieve all orders associated with a specific shipment.
    def get_orders_in_shipment(self, shipment_id):
        query = "SELECT id FROM orders WHERE shipment_id = ?"
        return [row[0] for row in self.execute_query(query, params=(shipment_id,), fetch_all=True)]

    # Retrieve all orders for a specific client.
    def get_orders_for_client(self, client_id):
        query = "SELECT * FROM orders WHERE ship_to = ? OR bill_to = ?"
        orders = self.execute_query(query, params=(client_id, client_id), fetch_all=True)
        formatted_orders = []
        for order in orders:
            order_dict = self.format_order(order)
            order_dict["items"] = self.get_items_in_order(order[0])
            formatted_orders.append(order_dict)
        return formatted_orders

    # Add a new order to the database.
    def add_order(self, order):
        query = """
        INSERT INTO orders (id, source_id, order_date, request_date, reference, reference_extra, order_status, 
                            notes, shipping_notes, picking_notes, warehouse_id, ship_to, bill_to, shipment_id, 
                            total_amount, total_discount, total_tax, total_surcharge, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        query2 = "INSERT INTO order_items (order_id, item_id, amount) VALUES (?, ?, ?)"

        order["created_at"] = self.get_timestamp()
        order["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            order["id"], order["source_id"], order["order_date"], order["request_date"], order["reference"],
            order["reference_extra"], order["order_status"], order["notes"], order["shipping_notes"],
            order["picking_notes"], order["warehouse_id"], order["ship_to"], order["bill_to"],
            order["shipment_id"], order["total_amount"], order["total_discount"], order["total_tax"],
            order["total_surcharge"], order["created_at"], order["updated_at"]
        ))

        for item in order["items"]:
            self.execute_query(query2, params=(order["id"], item["item_id"], item["amount"]))

    def update_order(self, order_id, order):
        # Update order details in the orders table
        query = """
        UPDATE orders SET source_id = ?, order_date = ?, request_date = ?, reference = ?, reference_extra = ?, 
                        order_status = ?, notes = ?, shipping_notes = ?, picking_notes = ?, warehouse_id = ?, 
                        ship_to = ?, bill_to = ?, shipment_id = ?, total_amount = ?, total_discount = ?, 
                        total_tax = ?, total_surcharge = ?, updated_at = ? WHERE id = ?
        """
        order["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            order["source_id"], order["order_date"], order["request_date"], order["reference"], order["reference_extra"],
            order["order_status"], order["notes"], order["shipping_notes"], order["picking_notes"],
            order["warehouse_id"], order["ship_to"], order["bill_to"], order["shipment_id"], order["total_amount"],
            order["total_discount"], order["total_tax"], order["total_surcharge"], order["updated_at"], order_id
        ))

        # Update the items in the order_items table
        if "items" in order:
            # Delete existing items for the order
            delete_items_query = "DELETE FROM order_items WHERE order_id = ?"
            self.execute_query(delete_items_query, params=(order_id,))

            # Insert updated items
            insert_items_query = "INSERT INTO order_items (order_id, item_id, amount) VALUES (?, ?, ?)"
            for item in order["items"]:
                self.execute_query(insert_items_query, params=(order_id, item["item_id"], item["amount"]))


    # Update items in an existing order.
    def update_items_in_order(self, order_id, items):
        delete_query = "DELETE FROM order_items WHERE order_id = ?"
        insert_query = """
        INSERT INTO order_items (order_id, item_id, amount) VALUES (?, ?, ?)
        """
        self.execute_query(delete_query, params=(order_id,))
        for item in items:
            self.execute_query(insert_query, params=(order_id, item["item_id"], item["amount"]))

    # Update orders associated with a shipment.
    def update_orders_in_shipment(self, shipment_id, orders):
        update_query = "UPDATE orders SET shipment_id = ?, order_status = ? WHERE id = ?"
        for order_id in orders:
            self.execute_query(update_query, params=(shipment_id, "Packed", order_id))

        reset_query = "UPDATE orders SET shipment_id = -1, order_status = 'Scheduled' WHERE shipment_id = ? AND id NOT IN ({})"
        if orders:
            placeholders = ", ".join("?" for _ in orders)
            reset_query = reset_query.format(placeholders)
            self.execute_query(reset_query, params=(shipment_id, *orders))
        else:
            self.execute_query(reset_query.format("NULL"), params=(shipment_id,))

    # Delete an order by ID.
    def remove_order(self, order_id):
        delete_items_query = "DELETE FROM order_items WHERE order_id = ?"
        delete_order_query = "DELETE FROM orders WHERE id = ?"
        self.execute_query(delete_items_query, params=(order_id,))
        self.execute_query(delete_order_query, params=(order_id,))

    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "orders.json"
    #     self.load(is_debug)

    # def get_orders(self):
    #     return self.data

    # def get_order(self, order_id):
    #     for x in self.data:
    #         if x["id"] == order_id:
    #             return x
    #     return None

    # def get_items_in_order(self, order_id):
    #     for x in self.data:
    #         if x["id"] == order_id:
    #             return x["items"]
    #     return None

    # def get_orders_in_shipment(self, shipment_id):
    #     result = []
    #     for x in self.data:
    #         if x["shipment_id"] == shipment_id:
    #             result.append(x["id"])
    #     return result

    # def get_orders_for_client(self, client_id):
    #     result = []
    #     for x in self.data:
    #         if x["ship_to"] == client_id or x["bill_to"] == client_id:
    #             result.append(x)
    #     return result

    # def add_order(self, order):
    #     order["created_at"] = self.get_timestamp()
    #     order["updated_at"] = self.get_timestamp()
    #     self.data.append(order)

    # def update_order(self, order_id, order):
    #     order["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == order_id:
    #             self.data[i] = order
    #             break

    # def update_items_in_order(self, order_id, items):
    #     from providers import data_provider
    #     order = self.get_order(order_id)
    #     current = order["items"]
    #     for x in current:
    #         found = False
    #         for y in items:
    #             if x["item_id"] == y["item_id"]:
    #                 found = True
    #                 break
    #         if not found:
    #             inventories = data_provider.fetch_inventory_pool(
    #             ).get_inventories_for_item(x["item_id"])
    #             min_ordered = 1_000_000_000_000_000_000
    #             min_inventory
    #             for z in inventories:
    #                 if z["total_allocated"] > min_ordered:
    #                     min_ordered = z["total_allocated"]
    #                     min_inventory = z
    #             min_inventory["total_allocated"] -= x["amount"]
    #             min_inventory["total_expected"] = y["total_on_hand"] + \
    #                 y["total_ordered"]
    #             data_provider.fetch_inventory_pool().update_inventory(
    #                 min_inventory["id"], min_inventory)
    #     for x in current:
    #         for y in items:
    #             if x["item_id"] == y["item_id"]:
    #                 inventories = data_provider.fetch_inventory_pool(
    #                 ).get_inventories_for_item(x["item_id"])
    #                 min_ordered = 1_000_000_000_000_000_000
    #                 min_inventory
    #                 for z in inventories:
    #                     if z["total_allocated"] < min_ordered:
    #                         min_ordered = z["total_allocated"]
    #                         min_inventory = z
    #             min_inventory["total_allocated"] += y["amount"] - x["amount"]
    #             min_inventory["total_expected"] = y["total_on_hand"] + \
    #                 y["total_ordered"]
    #             data_provider.fetch_inventory_pool().update_inventory(
    #                 min_inventory["id"], min_inventory)
    #     order["items"] = items
    #     self.update_order(order_id, order)

    # def update_orders_in_shipment(self, shipment_id, orders):
    #     packed_orders = self.get_orders_in_shipment(shipment_id)
    #     for x in packed_orders:
    #         if x not in orders:
    #             order = self.get_order(x)
    #             order["shipment_id"] = -1
    #             order["order_status"] = "Scheduled"
    #             self.update_order(x, order)
    #     for x in orders:
    #         order = self.get_order(x)
    #         order["shipment_id"] = shipment_id
    #         order["order_status"] = "Packed"
    #         self.update_order(x, order)

    # def remove_order(self, order_id):
    #     for x in self.data:
    #         if x["id"] == order_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = ORDERS
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
