
import pytest
import unittest
import sys
import os
import pytest
import requests
import logging


# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from models.transfers import Transfers
BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


class Test_Transfers():

    transferObject = Transfers("Test_Data/test_")

    headers_full = {
            "API_KEY": "a1b2c3d4e5",
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

        response = requests.post(
            f"{BASE_URL}/api/v1/transfers/", headers=self.headers_full, json=self.newTransfer)
        new_timestamp = self.transferObject.get_timestamp()
        self.newTransfer["created_at"] = new_timestamp.split('T')[0]
        self.newTransfer["updated_at"] = new_timestamp.split('T')[0]
        self.newTransfer["transfer_status"] = "Scheduled"
        assert response.status_code == 201

    def test_get_endpoint(self):

        response = requests.get(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=self.headers_full)
        assert response.status_code == 200

        dict_response = response.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newTransfer

    def test_update_endpoint(self):
        
        self.newTransfer["reference"] = "TH269240"
        self.newTransfer["transfer_status"] = "Scheduled"
        self.newTransfer["items"][0]["amount"] = 10

        response = requests.put(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=self.headers_full, json=self.newTransfer)
        self.newTransfer["updated_at"] = self.transferObject.split('T')[0]
        assert response.status_code == 200




    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/transfers/{self.newTransfer['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

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
        ], "The transfer with ID 2 doesn't match the expected dictionary"

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
        }, "The transfer with id 2 doesn't match the dictionary"

    def test_get_items_in_transfer(self):
        items_in_transfer2 = self.transferObject.get_items_in_transfer(2)
        assert items_in_transfer2[0] == {
            "item_id": "P007435",
            "amount": 23
        }, "The items inside the transfer with id 2 don't match the dictionary"

    def test_add_transfer(self):
        new_transfer = {
            "id": 99,
            "reference": "TR119216",
            "transfer_from": None,
            "transfer_to": 769,
            "transfer_status": "-",     # <- Will be autofilled
            "created_at": "-",          # <- Will be autofilled
            "updated_at": "-",          # <- Will be autofilled
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

        assert self.transferObject.get_transfer(99) == new_transfer, \
            "The json doesn't match the created new_transfer dictionary , or get_transfer doesn't function properly"

    def test_update_transfer(self):
        updated_transfer = {
            "id": 99,
            "reference": "TR119217",    # <- Changed
            "transfer_from": None,
            "transfer_to": 780,         # <- Changed
            "transfer_status": "Completed",
            "created_at": "2001-01-03T15:24:53Z",
            "updated_at": "-",           # <- Will be autofilled
            "items": [
                {
                    "item_id": "P002698",
                    "amount": 40         # <- Changed
                }
            ]
        }

        self.transferObject.update_transfer(99, updated_transfer)
        new_timestamp = self.transferObject.get_timestamp()
        updated_transfer["updated_at"] = new_timestamp

        assert self.transferObject.get_transfer(99) == updated_transfer, \
            "The JSON response doesn't match the updated_transfer dictionary, or get_transfer doesn't function properly."

    def test_remove_transfer(self):

        self.transferObject.remove_transfer(99)

        assert self.transferObject.get_transfer(99) == None, \
            "Transfer with ID 99 still exists in the database, or get_transfer doesn't function properly."
