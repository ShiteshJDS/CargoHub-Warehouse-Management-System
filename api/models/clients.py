# import json
import sqlite3
from models.base import Base

# CLIENTS = []


class Clients(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # A method to interact with the database.
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params or [])
            conn.commit()
            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()

    # Retrieve all clients from the database.
    def get_clients(self):
        query = "SELECT * FROM clients"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a single client by ID.
    def get_client(self, client_id):
        query = "SELECT * FROM clients WHERE id = ?"
        return self.execute_query(query, params=(client_id,), fetch_one=True)



    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "clients.json"
    #     self.load(is_debug)

    # def get_clients(self):
    #     return self.data

    # def get_client(self, client_id):
    #     for x in self.data:
    #         if x["id"] == client_id:
    #             return x
    #     return None

    # def add_client(self, client):
    #     client["created_at"] = self.get_timestamp()
    #     client["updated_at"] = self.get_timestamp()
    #     self.data.append(client)

    # def update_client(self, client_id, client):
    #     client["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == client_id:
    #             self.data[i] = client
    #             break

    # def remove_client(self, client_id):
    #     for x in self.data:
    #         if x["id"] == client_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = CLIENTS
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
