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
    os.path.join(os.path.dirname(__file__), '..', '..')))

from models.transfers import Transfers  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

class Test_Transfers():

    transferObject = Transfers("../Test_Data/Cargohub_Test.db")
    # Transfer Method Testing

    # def test_get_transfers(self):

    #     allTransfers = self.transferObject.get_transfers()
    #     assert allTransfers == [
    #         {
    #             "id": 1,
    #             "reference": "TR00001",
    #             "transfer_from": None,
    #             "transfer_to": 9229,
    #             "transfer_status": "Completed",
    #             "created_at": "2000-03-11T13:11:14Z",
    #             "updated_at": "2000-03-12T16:11:14Z",
    #             "items": [
    #                 {
    #                     "item_id": "P007435",
    #                     "amount": 23
    #                 }
    #             ]
    #         },
    #         {
    #             "id": 2,
    #             "reference": "TR00002",
    #             "transfer_from": 9229,
    #             "transfer_to": 9284,
    #             "transfer_status": "Completed",
    #             "created_at": "2017-09-19T00:33:14Z",
    #             "updated_at": "2017-09-20T01:33:14Z",
    #             "items": [
    #                 {
    #                     "item_id": "P007435",
    #                     "amount": 23
    #                 }
    #             ]
    #         },
    #         {
    #             "id": 3,
    #             "reference": "TR00003",
    #             "transfer_from": None,
    #             "transfer_to": 9199,
    #             "transfer_status": "Completed",
    #             "created_at": "2000-03-11T13:11:14Z",
    #             "updated_at": "2000-03-12T14:11:14Z",
    #             "items": [
    #                 {
    #                     "item_id": "P009557",
    #                     "amount": 1
    #                 }
    #             ]
    #         }
    #     ], "The transfer database doesn't match the expected data"

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
            "id": 119241,
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

        self.transferObject.add_transfer(new_transfer)
        new_timestamp = self.transferObject.get_timestamp()
        new_transfer["created_at"] = new_timestamp
        new_transfer["updated_at"] = new_timestamp
        new_transfer["transfer_status"] = "Scheduled"

        saved_transfer = self.transferObject.get_transfer(119241)
        assert saved_transfer is not None, "The new transfer ID 119241 wasn't saved correctly, or get_transfer doesn't function properly"

        # Remove the created_at and updated_at fields for comparison
        saved_transfer.pop("created_at", None)
        saved_transfer.pop("updated_at", None)
        new_transfer.pop("created_at", None)
        new_transfer.pop("updated_at", None)

        assert saved_transfer == new_transfer, "The new transfer ID 119241 wasn't saved correctly, or get_transfer doesn't function properly"
    
    def test_update_transfer(self):
        updated_transfer = {
            "id": 119241,
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

        self.transferObject.update_transfer(119241, updated_transfer)
        new_timestamp = self.transferObject.get_timestamp()
        updated_transfer["updated_at"] = new_timestamp

        saved_transfer = self.transferObject.get_transfer(119241)
        saved_transfer.pop("created_at", None)
        saved_transfer.pop("updated_at", None)
        updated_transfer.pop("created_at", None)
        updated_transfer.pop("updated_at", None)

        assert saved_transfer == updated_transfer, \
            "The new transfer with ID 119241 wasn't updated correctly, or get_transfer doesn't function properly."

    def test_remove_transfer(self):
        # Assert that the transfer exists before removal
        assert self.transferObject.get_transfer(119241) is not None, \
            "Transfer with ID 119241 does not exist before removal"

        self.transferObject.remove_transfer(119241)
        assert self.transferObject.get_transfer(119241) is None, \
            "Transfer with ID 119241 wasn't removed correctly, or get_transfer doesn't function properly"