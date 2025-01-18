import sqlite3
from models.base import Base


class Inventories(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Retrieve all inventories from the database.
    def get_inventories(self):
        query = "SELECT * FROM inventories"
        inventories = self.execute_query(query, fetch_all=True)
        for inventory in inventories:
            inventory["location"] = self.get_locations_for_inventory(
                inventory["id"])
        return inventories

    # Retrieve a single inventory by ID.
    def get_inventory(self, inventory_id):
        query = "SELECT * FROM inventories WHERE id = ?"
        inventory = self.execute_query(
            query, params=(inventory_id,), fetch_one=True)
        inventory["locations"] = self.get_locations_for_inventory(inventory_id)
        return inventory

    # Retrieve all inventories associated with a specific item.
    def get_inventories_for_item(self, item_id):
        query = "SELECT * FROM inventories WHERE item_id = ?"
        inventories = self.execute_query(
            query, params=(item_id,), fetch_all=True)
        for inventory in inventories:
            inventory["location"] = self.get_locations_for_inventory(
                inventory["id"])
        return inventories

    # Retrieve all locations associated with a specific inventory.
    # This method is not an endpoint and is only used inside the class
    def get_locations_for_inventory(self, inventory_id):
        query = "SELECT location_id FROM inventory_locations WHERE inventory_id = ?"
        return [location["location_id"] for location in self.execute_query(query, params=(inventory_id,), fetch_all=True)]

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
