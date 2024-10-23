import pytest
import unittest
import sys
import os
import pytest
import requests
import logging

# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.transfers import Transfers

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL


class Test_Transfers():

    transferObject = Transfers("api/Tests/Test_Data/test_")

    def test_correct_get_endpoint(self):

        headers_full = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        response = requests.get(
            f"{BASE_URL}/api/v1/transfers/1", headers=headers_full)
        assert response.status_code == 200
        assert response.json() == {
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
        }

    def test_post_endpoint(self):

        headers_full = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newTransferJson = {
            "id": 999999,
            "reference": "TR119240",
            "transfer_from": None,
            "transfer_to": 9203,
            "transfer_status": "Completed",
            "created_at": "1999-11-28T14:01:57Z",
            "updated_at": "1999-11-29T19:01:57Z",
            "items": [
                {
                    "item_id": "P001288",
                    "amount": 19
                }
            ]
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/transfers/", headers=headers_full, json=newTransferJson)
        assert response.status_code == 201

        # delete the created transfer

        deleteHeader = {
            "API_KEY": "a1b2c3d4e5"
        }
        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/transfers/{newTransferJson['id']}", headers=deleteHeader)
        assert responseDelete.status_code == 200

   ###############   Transfer Method Testing   ###############

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
        ], "test_get_transfers failed"

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
        }, "test_get_transfer_with_id failed"

    def test_get_items_in_transfer(self):
        items_in_transfer2 = self.transferObject.get_items_in_transfer(2)
        assert items_in_transfer2[0] == {
            "item_id": "P007435",
            "amount": 23
        }, "test_get_items_in_transfer failed"

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

        assert self.transferObject.get_transfer(99) == {
            "id": 99,
            "reference": "TR119216",
            "transfer_from": None,
            "transfer_to": 769,
            "transfer_status": "Scheduled",
            "created_at": f"{new_timestamp}",
            "updated_at": f"{new_timestamp}",
            "items": [
                {
                    "item_id": "P002698",
                    "amount": 35
                }
            ]
        }, "test_add_transfer failed"

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

        assert self.transferObject.get_transfer(99) == {
            "id": 99,
            "reference": "TR119217",  # <- Changed
            "transfer_from": None,
            "transfer_to": 780,  # <- Changed
            "transfer_status": "Completed",
            "created_at": "2001-01-03T15:24:53Z",
            "updated_at": f"{new_timestamp}",
            "items": [
                {
                    "item_id": "P002698",
                    "amount": 40  # <- Changed
                }
            ]
        }, "test_update_transfer failed"

    def test_remove_transfer(self):

        self.transferObject.remove_transfer(99)

        assert self.transferObject.get_transfer(
            99) == None, "test_remove_transfer failed"
