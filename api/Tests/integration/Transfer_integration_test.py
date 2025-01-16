
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