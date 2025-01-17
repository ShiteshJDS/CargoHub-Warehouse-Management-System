# import json
import sqlite3
from models.base import Base

# LOCATIONS = []


class Locations(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Format location as a dictionary.
    def format_location(self, location):
        return {
            "id": location[0],
            "warehouse_id": location[1],
            "code": location[2],
            "name": location[3],
            "created_at": location[4],
            "updated_at": location[5]
        }

    # Retrieve all locations from the database.
    def get_locations(self):
        query = "SELECT * FROM locations"
        locations = self.execute_query(query, fetch_all=True)
        return [self.format_location(location) for location in locations]

    # Retrieve a specific location by ID.
    def get_location(self, location_id):
        query = "SELECT * FROM locations WHERE id = ?"
        location = self.execute_query(query, params=(location_id,), fetch_one=True)
        if location:
            return self.format_location(location)
        return None

    # Retrieve all locations in a specific warehouse.
    def get_locations_in_warehouse(self, warehouse_id):
        query = "SELECT * FROM locations WHERE warehouse_id = ?"
        locations = self.execute_query(query, params=(warehouse_id,), fetch_all=True)
        return [self.format_location(location) for location in locations]

    # Add a new location to the database.
    def add_location(self, location):
        """Add a new location to the database."""
        query = """
        INSERT INTO locations (id, warehouse_id, code, name, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?)
        """
        location["created_at"] = self.get_timestamp()
        location["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            location["id"], location["warehouse_id"], location["code"], location["name"],
            location["created_at"], location["updated_at"]
        ))

    # Update an existing location.
    def update_location(self, location_id, location):
        query = """
        UPDATE locations SET warehouse_id = ?, code = ?, name = ?, updated_at = ? 
        WHERE id = ?
        """
        location["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            location["warehouse_id"], location["code"], location["name"],
            location["updated_at"], location_id
        ))

    # Delete a location by ID.
    def remove_location(self, location_id):
        query = "DELETE FROM locations WHERE id = ?"
        self.execute_query(query, params=(location_id,))


    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "locations.json"
    #     self.load(is_debug)

    # def get_locations(self):
    #     return self.data

    # def get_location(self, location_id):
    #     for x in self.data:
    #         if x["id"] == location_id:
    #             return x
    #     return None

    # def get_locations_in_warehouse(self, warehouse_id):
    #     result = []
    #     for x in self.data:
    #         if x["warehouse_id"] == warehouse_id:
    #             result.append(x)
    #     return result

    # def add_location(self, location):
    #     location["created_at"] = self.get_timestamp()
    #     location["updated_at"] = self.get_timestamp()
    #     self.data.append(location)

    # def update_location(self, location_id, location):
    #     location["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == location_id:
    #             self.data[i] = location
    #             break

    # def remove_location(self, location_id):
    #     for x in self.data:
    #         if x["id"] == location_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = LOCATIONS
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
