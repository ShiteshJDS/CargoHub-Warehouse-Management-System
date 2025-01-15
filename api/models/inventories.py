import sqlite3
from models.base import Base

class Inventories(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    def row_to_dict(self, row):
        return {
            "id": row[0],
            "item_id": row[1],
            "description": row[2],
            "item_reference": row[3],
            "total_on_hand": row[4],
            "total_expected": row[5],
            "total_ordered": row[6],
            "total_allocated": row[7],
            "total_available": row[8],
            "created_at": row[9],
            "updated_at": row[10]
        }

    # Retrieve all inventories from the database.
    def get_inventories(self):
        query = "SELECT * FROM inventories"
        rows = self.execute_query(query, fetch_all=True)
        return [self.row_to_dict(row) for row in rows]

    # Retrieve a single inventory by ID.
    def get_inventory(self, inventory_id):
        query = "SELECT * FROM inventories WHERE id = ?"
        row = self.execute_query(query, params=(inventory_id,), fetch_one=True)
        return self.row_to_dict(row) if row else None

    # Retrieve all inventories associated with a specific item.
    def get_inventories_for_item(self, item_id):
        query = "SELECT * FROM inventories WHERE item_id = ?"
        rows = self.execute_query(query, params=(item_id,), fetch_all=True)
        return [self.row_to_dict(row) for row in rows]

    # Retrieve total inventory details for a specific item.
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
