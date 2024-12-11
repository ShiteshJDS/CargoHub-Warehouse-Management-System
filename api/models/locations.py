# import json
import sqlite3
from models.base import Base

# LOCATIONS = []


class Locations(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Helper method to interact with the database.
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()

    # Retrieve all locations from the database.
    def get_locations(self):
        query = "SELECT * FROM locations"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a specific location by ID.
    def get_location(self, location_id):
        query = "SELECT * FROM locations WHERE id = ?"
        return self.execute_query(query, params=(location_id,), fetch_one=True)

    # Retrieve all locations in a specific warehouse.
    def get_locations_in_warehouse(self, warehouse_id):
        query = "SELECT * FROM locations WHERE warehouse_id = ?"
        return self.execute_query(query, params=(warehouse_id,), fetch_all=True)

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
