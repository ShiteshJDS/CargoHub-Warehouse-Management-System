# import json
import sqlite3
from models.base import Base

# ITEMS = []


class Items(Base):
    def __init__(self, db_path):
        self.db_path = db_path
        self.tablename = "items"

    # Retrieve all items from the database
    def get_items(self):
        query = "SELECT * FROM items"
        items = self.execute_query(query, fetch_all=True)
        return [self.format_item(item) for item in items]

    # Retrieve a single item by UID
    def get_item(self, item_id):
        query = "SELECT * FROM items WHERE uid = ?"
        item = self.execute_query(query, params=(item_id,), fetch_one=True)
        return self.format_item(item) if item else None

    # Format item as a dictionary
    def format_item(self, item):
        return {
            "uid": item[0],
            "code": item[1],
            "description": item[2],
            "short_description": item[3],
            "upc_code": item[4],
            "model_number": item[5],
            "commodity_code": item[6],
            "item_line": item[7],
            "item_group": item[8],
            "item_type": item[9],
            "unit_purchase_quantity": item[10],
            "unit_order_quantity": item[11],
            "pack_order_quantity": item[12],
            "supplier_id": item[13],
            "supplier_code": item[14],
            "supplier_part_number": item[15],
            "created_at": item[16],
            "updated_at": item[17]
        }

    # Retrieve all inventories for a specific item
    def get_inventories_for_item(self, item_id):
        query = "SELECT * FROM inventories WHERE item_id = ?"
        inventories = self.execute_query(
            query, params=(item_id,), fetch_all=True)
        return [self.format_inventory(inventory) for inventory in inventories]

    # Retrieve total inventory details for a specific item
    def get_inventory_totals_for_item(self, item_id):
        query = """
        SELECT SUM(total_expected) AS total_expected,
               SUM(total_ordered) AS total_ordered,
               SUM(total_allocated) AS total_allocated,
               SUM(total_available) AS total_available
        FROM inventories WHERE item_id = ?
        """
        row = self.execute_query(query, params=(item_id,), fetch_one=True)
        if row:
            return {
                "total_expected": row[0],
                "total_ordered": row[1],
                "total_allocated": row[2],
                "total_available": row[3]
            }
        return None

    # Format inventory as a dictionary
    def format_inventory(self, inventory):
        return {
            "id": inventory[0],
            "item_id": inventory[1],
            "description": inventory[2],
            "item_reference": inventory[3],
            # Assuming locations are stored as a list in the database
            "locations": inventory[4],
            "total_on_hand": inventory[5],
            "total_expected": inventory[6],
            "total_ordered": inventory[7],
            "total_allocated": inventory[8],
            "total_available": inventory[9],
            "created_at": inventory[10],
            "updated_at": inventory[11]
        }

    # Retrieve items associated with a specific item line
    def get_items_for_item_line(self, item_line_id):
        query = "SELECT * FROM items WHERE item_line_id = ?"
        result = self.execute_query(
            query, params=(item_line_id,), fetch_all=True)
        return self.query_to_dict(result)

    # Retrieve items associated with a specific item group
    def get_items_for_item_group(self, item_group_id):
        query = "SELECT * FROM items WHERE item_group_id = ?"
        result = self.execute_query(
            query, params=(item_group_id,), fetch_all=True)
        return self.query_to_dict(result)

    # Retrieve items associated with a specific item type
    def get_items_for_item_type(self, item_type_id):
        query = "SELECT * FROM items WHERE item_type_id = ?"
        result = self.execute_query(
            query, params=(item_type_id,), fetch_all=True)
        return self.query_to_dict(result)

    # Retrieve items associated with a specific supplier
    def get_items_for_supplier(self, supplier_id):
        query = "SELECT * FROM items WHERE supplier_id = ?"
        result = self.execute_query(
            query, params=(supplier_id,), fetch_all=True)
        return self.query_to_dict(result)

    # Add a new item to the database.
    def add_item(self, item):
        query = """
        INSERT INTO items (uid, code, description, short_description, upc_code, model_number, 
                           commodity_code, item_line_id, item_group_id, item_type_id, 
                           unit_purchase_quantity, unit_order_quantity, pack_order_quantity, 
                           supplier_id, supplier_code, supplier_part_number, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        item["created_at"] = self.get_timestamp()
        item["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            item["uid"], item["code"], item["description"], item["short_description"], item["upc_code"], 
            item["model_number"], item["commodity_code"], item["item_line"], item["item_group"], 
            item["item_type"], item["unit_purchase_quantity"], item["unit_order_quantity"],
            item["pack_order_quantity"], item["supplier_id"], item["supplier_code"], 
            item["supplier_part_number"], item["created_at"], item["updated_at"]
        ))

    # Update an existing item.
    def update_item(self, item_id, item):
        query = """
        UPDATE items SET code = ?, description = ?, short_description = ?, upc_code = ?, model_number = ?, 
                         commodity_code = ?, item_line = ?, item_group = ?, item_type = ?, 
                         unit_purchase_quantity = ?, unit_order_quantity = ?, pack_order_quantity = ?, 
                         supplier_id = ?, supplier_code = ?, supplier_part_number = ?, updated_at = ? 
        WHERE uid = ?
        """
        item["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            item["code"], item["description"], item["short_description"], item["upc_code"], item["model_number"],
            item["commodity_code"], item["item_line"], item["item_group"], item["item_type"],
            item["unit_purchase_quantity"], item["unit_order_quantity"], item["pack_order_quantity"],
            item["supplier_id"], item["supplier_code"], item["supplier_part_number"], item["updated_at"], item_id
        ))

    # Delete an item by UID.
    def remove_item(self, item_id):
        query = "DELETE FROM items WHERE uid = ?"
        self.execute_query(query, params=(item_id,))

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
