
import pytest
import unittest
import sys
import os
import requests
import logging
import shutil
from dotenv import load_dotenv

load_dotenv()

# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from models.transfers import Transfers  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

@pytest.fixture(scope="module", autouse=True)
def manage_warehouse_json_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../../data/transfers.json")
    backup_file_path = f"{json_file_path}.backup"

    # Backup the JSON file
    shutil.copyfile(json_file_path, backup_file_path)

    yield  # Run the tests

    # Restore the JSON file from backup
    shutil.copyfile(backup_file_path, json_file_path)
    os.remove(backup_file_path)  # Clean up the backup file

class Test_Transfers():

    transferObject = Transfers("Test_Data/Cargohub_Test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newTransfer = {
        "id": 0,
        "reference": "TR119240",
        "transfer_from": None,
        "transfer_to": 9203,
        "transfer_status": "-",
        "created_at": "-",
        "updated_at": "-",
        "items": [
            {
                "item_id": "P001288",
                "amount": 19
            }
        ]
    }

    # Transfer Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/transfers/", headers=self.headers_full, json=self.newTransfer)
        new_timestamp = self.transferObject.get_timestamp()
        self.newTransfer["created_at"] = new_timestamp.split('T')[0]
        self.newTransfer["updated_at"] = new_timestamp.split('T')[0]
        self.newTransfer["transfer_status"] = "Scheduled"
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newTransfer["reference"] = "TH269240"
        self.newTransfer["transfer_status"] = "Completed"
        self.newTransfer["items"][0]["amount"] = 10

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=self.headers_full, json=self.newTransfer)
        self.newTransfer["updated_at"] = self.transferObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newTransfer

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restriction(self):
        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/transfers/", headers=headers_restricted, json=self.newTransfer)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=headers_restricted, json=self.newTransfer)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200

    # Transfer Method Testing

    def test_get_transfers(self):

        allTransfers = self.transferObject.get_transfers()
        assert allTransfers == [
            {
                "id": 1,
                "reference": "TR00001",
                "transfer_from": None,
                "transfer_to": 9229,
                "transfer_status": "Completed",
                "created_at": "2000-03-11T13:11:14Z",
                "updated_at": "2000-03-12T16:11:14Z",
                "items": [
                    {
                        "item_id": "P007435",
                        "amount": 23
                    }
                ]
            },
            {
                "id": 2,
                "reference": "TR00002",
                "transfer_from": 9229,
                "transfer_to": 9284,
                "transfer_status": "Completed",
                "created_at": "2017-09-19T00:33:14Z",
                "updated_at": "2017-09-20T01:33:14Z",
                "items": [
                    {
                        "item_id": "P007435",
                        "amount": 23
                    }
                ]
            },
            {
                "id": 3,
                "reference": "TR00003",
                "transfer_from": None,
                "transfer_to": 9199,
                "transfer_status": "Completed",
                "created_at": "2000-03-11T13:11:14Z",
                "updated_at": "2000-03-12T14:11:14Z",
                "items": [
                    {
                        "item_id": "P009557",
                        "amount": 1
                    }
                ]
            }
        ], "The transfer database doesn't match the expected data"

    def test_get_transfer_with_id(self):
        transfer2 = self.transferObject.get_transfer(2)
        assert transfer2 == {
            "id": 2,
            "reference": "TR00002",
            "transfer_from": 9229,
            "transfer_to": 9284,
            "transfer_status": "Completed",
            "created_at": "2017-09-19T00:33:14Z",
            "updated_at": "2017-09-20T01:33:14Z",
            "items": [
                {
                    "item_id": "P007435",
                    "amount": 23
                }
            ]
        }, "The transfer with id 2 wasn't found in the transfer database"

    def test_get_items_in_transfer(self):
        items_in_transfer2 = self.transferObject.get_items_in_transfer(2)
        assert items_in_transfer2 == [
            {
                "item_id": "P007435",
                "amount": 23
            }
        ], "The items inside the transfer with id 2 don't match the expected data"

    def test_add_transfer(self):
        new_transfer = {
            "id": 4,
            "reference": "TR119216",
            "transfer_from": None,
            "transfer_to": 769,
            "transfer_status": "-",
            "created_at": "-",
            "updated_at": "-",
            "items": [
                {
                    "item_id": "P002698",
                    "amount": 35
                }
            ]
        }

        self.transferObject.add_transfer(new_transfer)
        new_timestamp = self.transferObject.get_timestamp()
        new_transfer["created_at"] = new_timestamp
        new_transfer["updated_at"] = new_timestamp
        new_transfer["transfer_status"] = "Scheduled"

        assert self.transferObject.get_transfer(4) == new_transfer, \
            "The new transfer wasn't saved correctly, or get_transfer doesn't function properly"

    def test_update_transfer(self):
        updated_transfer = {
            "id": 4,
            "reference": "TR119217",    # <- Changed
            "transfer_from": None,
            "transfer_to": 780,         # <- Changed
            "transfer_status": "Completed",
            "created_at": "2001-01-03T15:24:53Z",
            "updated_at": "-",
            "items": [
                {
                    "item_id": "P002698",
                    "amount": 40         # <- Changed
                }
            ]
        }

        self.transferObject.update_transfer(4, updated_transfer)
        new_timestamp = self.transferObject.get_timestamp()
        updated_transfer["updated_at"] = new_timestamp

        assert self.transferObject.get_transfer(4) == updated_transfer, \
            "The new transfer wasn't updated correctly, or get_transfer doesn't function properly."

    def test_remove_transfer(self):

        self.transferObject.remove_transfer(4)
        assert self.transferObject.get_transfer(4) == None, \
            "Transfer with ID 99 wasn't removed correctly, or get_transfer doesn't function properly"
