import sqlite3
from models.base import Base


class Clients(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Retrieve all clients from the database.#!#1#!#
    def get_clients(self):
        query = "SELECT * FROM clients"
        return self.execute_query(query, fetch_all=True)

    # Retrieve a single client by ID.#!#1#!#
    def get_client(self, client_id):
        query = "SELECT * FROM clients WHERE id = ?"
        return self.execute_query(query, params=(client_id,), fetch_one=True)

    # Add a new client to the database.
    def add_client(self, client):
        query = """
        INSERT INTO clients (id, name, address, city, zip_code, province, country, 
                             contact_name, contact_phone, contact_email, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        client['created_at'] = self.get_timestamp()
        client['updated_at'] = self.get_timestamp()
        self.execute_query(query, params=(
            client['id'], client['name'], client['address'], client['city'], client['zip_code'],
            client['province'], client['country'], client['contact_name'], client['contact_phone'],
            client['contact_email'], client['created_at'], client['updated_at']
        ))

    # Update an existing client.
    def update_client(self, client_id, client):
        query = """
        UPDATE clients SET name = ?, address = ?, city = ?, zip_code = ?, province = ?, 
                           country = ?, contact_name = ?, contact_phone = ?, contact_email = ?, 
                           updated_at = ? WHERE id = ?
        """
        client['updated_at'] = self.get_timestamp()
        self.execute_query(query, params=(
            client['name'], client['address'], client['city'], client['zip_code'],
            client['province'], client['country'], client['contact_name'], client['contact_phone'],
            client['contact_email'], client['updated_at'], client_id
        ))

    # Delete a client from the database.
    def remove_client(self, client_id):
        query = "DELETE FROM clients WHERE id = ?"
        self.execute_query(query, params=(client_id,))
