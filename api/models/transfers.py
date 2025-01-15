# import json
import sqlite3
from models.base import Base

# TRANSFERS = []


class Transfers(Base):
    def __init__(self, db_path):
        self.db_path = db_path

    # Retrieve all transfers from the database
    def get_transfers(self):
        query = "SELECT * FROM transfers"
        transfers = self.execute_query(query, fetch_all=True)
        transfers_list = []
        for transfer in transfers:
            transfer_dict = {
                "id": transfer[0],
                "reference": transfer[1],
                "transfer_from": transfer[2],
                "transfer_to": transfer[3],
                "transfer_status": transfer[4],
                "created_at": transfer[5],
                "updated_at": transfer[6],
                "items": self.get_items_in_transfer(transfer[0])
            }
            transfers_list.append(transfer_dict)
        return transfers_list

    # Retrieve a specific transfer by ID
    def get_transfer(self, transfer_id):
        query = "SELECT * FROM transfers WHERE id = ?"
        transfer = self.execute_query(query, params=(transfer_id,), fetch_one=True)
        if transfer:
            transfer_dict = {
                "id": transfer[0],
                "reference": transfer[1],
                "transfer_from": transfer[2],
                "transfer_to": transfer[3],
                "transfer_status": transfer[4],
                "created_at": transfer[5],
                "updated_at": transfer[6],
                "items": self.get_items_in_transfer(transfer_id)
            }
            return transfer_dict
        return None

    # Retrieve all items in a specific transfer
    def get_items_in_transfer(self, transfer_id):
        query = "SELECT * FROM transfer_items WHERE transfer_id = ?"
        items = self.execute_query(query, params=(transfer_id,), fetch_all=True)
        items_list = [{"item_id": item[2], "amount": item[3]} for item in items]
        return items_list

    # Add a new item to a transfer
    def add_transfer(self, transfer):
        query = """
        INSERT INTO transfers (id, reference, transfer_from, transfer_to, transfer_status, created_at, updated_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        transfer["transfer_status"] = "Scheduled"
        transfer["created_at"] = self.get_timestamp()
        transfer["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            transfer["id"], transfer["reference"], transfer["transfer_from"], transfer["transfer_to"],
            transfer["transfer_status"], transfer["created_at"], transfer["updated_at"]
        ))

    # Update an existing transfer
    def update_transfer(self, transfer_id, transfer):
        query = """
        UPDATE transfers SET reference = ?, transfer_from = ?, transfer_to = ?, transfer_status = ?, 
                             updated_at = ? WHERE id = ?
        """
        transfer["updated_at"] = self.get_timestamp()
        self.execute_query(query, params=(
            transfer["reference"], transfer["transfer_from"], transfer["transfer_to"],
            transfer["transfer_status"], transfer["updated_at"], transfer_id
        ))

    # Delete a transfer and its associated items
    def remove_transfer(self, transfer_id):
        delete_items_query = "DELETE FROM transfer_items WHERE transfer_id = ?"
        delete_transfer_query = "DELETE FROM transfers WHERE id = ?"
        self.execute_query(delete_items_query, params=(transfer_id,))
        self.execute_query(delete_transfer_query, params=(transfer_id,))


    # def __init__(self, root_path, is_debug=False):
    #     self.data_path = root_path + "transfers.json"
    #     self.load(is_debug)

    # def get_transfers(self):
    #     return self.data

    # def get_transfer(self, transfer_id):
    #     for x in self.data:
    #         if x["id"] == transfer_id:
    #             return x
    #     return None

    # def get_items_in_transfer(self, transfer_id):
    #     for x in self.data:
    #         if x["id"] == transfer_id:
    #             return x["items"]
    #     return None

    # def add_transfer(self, transfer):
    #     transfer["transfer_status"] = "Scheduled"
    #     transfer["created_at"] = self.get_timestamp()
    #     transfer["updated_at"] = self.get_timestamp()
    #     self.data.append(transfer)

    # def update_transfer(self, transfer_id, transfer):
    #     transfer["updated_at"] = self.get_timestamp()
    #     for i in range(len(self.data)):
    #         if self.data[i]["id"] == transfer_id:
    #             self.data[i] = transfer
    #             break

    # def remove_transfer(self, transfer_id):
    #     for x in self.data:
    #         if x["id"] == transfer_id:
    #             self.data.remove(x)

    # def load(self, is_debug):
    #     if is_debug:
    #         self.data = TRANSFERS
    #     else:
    #         f = open(self.data_path, "r")
    #         self.data = json.load(f)
    #         f.close()

    # def save(self):
    #     f = open(self.data_path, "w")
    #     json.dump(self.data, f)
    #     f.close()
