
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

from models.orders import Orders  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

class Test_Orders():

    orderObject = Orders("../Test_Data/Cargohub_Test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newOrder = {
        "id": 0,
        "source_id": 33,
        "order_date": "2019-04-03T11:33:15Z",
        "request_date": "2019-04-07T11:33:15Z",
        "reference": "ORD00001",
        "reference_extra": "Bedreven arm straffen bureau.",
        "order_status": "Delivered",
        "notes": "Voedsel vijf vork heel.",
        "shipping_notes": "Buurman betalen plaats bewolkt.",
        "picking_notes": "Ademen fijn volgorde scherp aardappel op leren.",
        "warehouse_id": 18,
        "ship_to": None,
        "bill_to": None,
        "shipment_id": 1,
        "total_amount": 9905.13,
        "total_discount": 150.77,
        "total_tax": 372.72,
        "total_surcharge": 77.6,
        "created_at": "-",
        "updated_at": "-",
        "items": [
            {
                "item_id": "P007435",
                "amount": 23
            },
            {
                "item_id": "P009557",
                "amount": 1
            },
            {
                "item_id": "P009553",
                "amount": 50
            },
            {
                "item_id": "P010015",
                "amount": 16
            },
            {
                "item_id": "P002084",
                "amount": 33
            },
            {
                "item_id": "P009663",
                "amount": 18
            },
            {
                "item_id": "P010125",
                "amount": 18
            },
            {
                "item_id": "P005768",
                "amount": 26
            },
            {
                "item_id": "P004051",
                "amount": 1
            },
            {
                "item_id": "P005026",
                "amount": 29
            },
            {
                "item_id": "P000726",
                "amount": 22
            },
            {
                "item_id": "P008107",
                "amount": 47
            },
            {
                "item_id": "P001598",
                "amount": 32
            },
            {
                "item_id": "P002855",
                "amount": 20
            },
            {
                "item_id": "P010404",
                "amount": 30
            },
            {
                "item_id": "P010446",
                "amount": 6
            },
            {
                "item_id": "P001517",
                "amount": 9
            },
            {
                "item_id": "P009265",
                "amount": 2
            },
            {
                "item_id": "P001108",
                "amount": 20
            },
            {
                "item_id": "P009110",
                "amount": 18
            },
            {
                "item_id": "P009686",
                "amount": 13
            }
        ]
    }

    # Order Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/orders/", headers=self.headers_full, json=self.newOrder)
        new_timestamp = self.orderObject.get_timestamp()
        self.newOrder["created_at"] = new_timestamp.split('T')[0]
        self.newOrder["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newOrder["order_status"] = "Pending"
        self.newOrder["total_tax"] = 400.00
        self.newOrder["items"][0]["amount"] = 40

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=self.headers_full, json=self.newOrder)
        self.newOrder["updated_at"] = self.orderObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newOrder

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restriction(self):
        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/orders/", headers=headers_restricted, json=self.newOrder)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=headers_restricted, json=self.newOrder)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200