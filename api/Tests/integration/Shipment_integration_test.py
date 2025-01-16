
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

from models.shipments import Shipments  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

@pytest.fixture(scope="module", autouse=True)
def manage_warehouse_json_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../../data/shipments.json")
    backup_file_path = f"{json_file_path}.backup"

    # Backup the JSON file
    shutil.copyfile(json_file_path, backup_file_path)

    yield  # Run the tests

    # Restore the JSON file from backup
    shutil.copyfile(backup_file_path, json_file_path)
    os.remove(backup_file_path)  # Clean up the backup file

class Test_Shipments():

    shipmentObject = Shipments("../Test_Data/Cargohub_Test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newShipment = {
        "id": 0,
        "order_id": 2979,
        "source_id": 14,
        "order_date": "1990-05-14",
        "request_date": "1990-05-16",
        "shipment_date": "1990-05-18",
        "shipment_type": "I",
        "shipment_status": "Pending",
        "notes": "Schrijven eis kap houden gemak.",
        "carrier_code": "UPS",
        "carrier_description": "United Parcel Service",
        "service_code": "NextDay",
        "payment_type": "Automatic",
        "transfer_mode": "Ground",
        "total_package_count": 29,
        "total_package_weight": 273.78,
        "created_at": "-",
        "updated_at": "-",
        "items": [
            {
                "item_id": "P005900",
                "amount": 37
            },
            {
                "item_id": "P009650",
                "amount": 50
            },
            {
                "item_id": "P005215",
                "amount": 43
            },
            {
                "item_id": "P006029",
                "amount": 33
            },
            {
                "item_id": "P004916",
                "amount": 15
            },
            {
                "item_id": "P005210",
                "amount": 49
            },
            {
                "item_id": "P005954",
                "amount": 24
            },
            {
                "item_id": "P008475",
                "amount": 28
            },
            {
                "item_id": "P005563",
                "amount": 43
            },
            {
                "item_id": "P004387",
                "amount": 39
            },
            {
                "item_id": "P003905",
                "amount": 18
            },
            {
                "item_id": "P004197",
                "amount": 2
            },
            {
                "item_id": "P009214",
                "amount": 5
            },
            {
                "item_id": "P006997",
                "amount": 33
            },
            {
                "item_id": "P001093",
                "amount": 25
            },
            {
                "item_id": "P008432",
                "amount": 13
            },
            {
                "item_id": "P001658",
                "amount": 13
            },
            {
                "item_id": "P004518",
                "amount": 1
            },
            {
                "item_id": "P004551",
                "amount": 25
            },
            {
                "item_id": "P009852",
                "amount": 36
            },
            {
                "item_id": "P001524",
                "amount": 41
            },
            {
                "item_id": "P007633",
                "amount": 45
            },
            {
                "item_id": "P003571",
                "amount": 29
            },
            {
                "item_id": "P008751",
                "amount": 46
            }
        ]
    }

    # Shipment Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/shipments/", headers=self.headers_full, json=self.newShipment)
        new_timestamp = self.shipmentObject.get_timestamp()
        self.newShipment["created_at"] = new_timestamp.split('T')[0]
        self.newShipment["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newShipment["order_date"] = "2024-05-16"
        self.newShipment["payment_type"] = "Cash"
        self.newShipment["items"][0]["amount"] = 40

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=self.headers_full, json=self.newShipment)
        self.newShipment["updated_at"] = self.shipmentObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newShipment

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restriction(self):
        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/shipments/", headers=headers_restricted, json=self.newShipment)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=headers_restricted, json=self.newShipment)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200