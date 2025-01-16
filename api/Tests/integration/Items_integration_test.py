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

from models.items import Items

BASE_URL = "http://localhost:3000"

class Test_Items():

    itemsObject = Items("../Test_Data/Cargohub_Test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newItem = {
        "uid": "P999999",
        "code": "sjQ23408K",
        "description": "Face-to-face clear-thinking complexity",
        "short_description": "must",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
        "created_at": "-",
        "updated_at": "-"
    }

    incorrectItem = {
        "description": "Face-to-face clear-thinking complexity",
        "short_description": "must",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
        "created_at": "-",
        "updated_at": "-"
    }



    # Test endpoints for Items

    def test_post_correct_endpoint(self):
        responsePost = requests.post(
            f"{BASE_URL}/api/v1/items/", headers=self.headers_full, json=self.newItem)
        new_timestamp = self.itemsObject.get_timestamp()
        self.newItem["created_at"] = new_timestamp.split('T')[0]
        self.newItem["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201, "Correct item should return 201"
    
    def test_post_empty_item_endpoint(self):
        responsePost = requests.post(
            f"{BASE_URL}/api/v1/items/", headers=self.headers_full, json={})
        assert responsePost.status_code == 400, "Empty item should return 400"
    # ?? The test currently gives the Response code 201, which is incorrect. The test should return 400 as the item is empty.

    def test_post_missing_item_endpoint(self):
        responsePost = requests.post(
            f"{BASE_URL}/api/v1/items/", headers=self.headers_full, json=self.incorrectItem)
        assert responsePost.status_code == 400, "Missing item should return 400"
    # ?? The test currently gives the Response code 201, which is incorrect. The test should return 400 as the item is missing the UID.
    
    def test_post_duplicate_endpoint(self):
        responsePost = requests.post(
            f"{BASE_URL}/api/v1/items/", headers=self.headers_full, json=self.newItem)
        new_timestamp = self.itemsObject.get_timestamp()
        self.newItem["created_at"] = new_timestamp.split('T')[0]
        self.newItem["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 409, "Item already exists, should return 409"
    # ?? The test currently gives the Response code 201, which is incorrect. The test should return 409 as the item already exists.

    def test_get_correct_endpoint(self):
        responseGet = requests.get(
            f"{BASE_URL}/api/v1/items/P999999", headers=self.headers_full)
        json = responseGet.json()
        assert json["uid"] == self.newItem["uid"] and \
            json["code"] ==  self.newItem["code"] and\
            json["description"] == self.newItem["description"] and\
            json["short_description"] == self.newItem["short_description"] and\
            json["upc_code"] == self.newItem["upc_code"] and\
            json["model_number"] == self.newItem["model_number"] and \
            json["commodity_code"] == self.newItem["commodity_code"] and \
            json["item_line"] == self.newItem["item_line"] and\
            json["item_group"] == self.newItem["item_group"] and\
            json["item_type"] == self.newItem["item_type"] and\
            json["unit_purchase_quantity"] == self.newItem["unit_purchase_quantity"] and\
            json["unit_order_quantity"] == self.newItem["unit_order_quantity"] and\
            json["pack_order_quantity"] == self.newItem["pack_order_quantity"] and\
            json["supplier_id"] == self.newItem["supplier_id"] and\
            json["supplier_code"] == self.newItem["supplier_code"] and\
            json["supplier_part_number"] == self.newItem["supplier_part_number"]
            
        assert responseGet.status_code == 200, "Correct item should return 200"
        
    def test_put_correct_endpoint(self):
        self.newItem["item_line"] = 12
        self.newItem["item_group"] = 74
        self.newItem["item_type"] = 15

        responsePut = requests.put(f"{BASE_URL}/api/v1/items/P999999", headers=self.headers_full, json=self.newItem)

        responseGet = requests.get(f"{BASE_URL}/api/v1/items/P999999", headers=self.headers_full)
        json = responseGet.json()
        assert json["uid"] == self.newItem["uid"] and \
            json["code"] ==  self.newItem["code"] and\
            json["description"] == self.newItem["description"] and\
            json["short_description"] == self.newItem["short_description"] and\
            json["upc_code"] == self.newItem["upc_code"] and\
            json["model_number"] == self.newItem["model_number"] and \
            json["commodity_code"] == self.newItem["commodity_code"] and \
            json["item_line"] == self.newItem["item_line"] and\
            json["item_group"] == self.newItem["item_group"] and\
            json["item_type"] == self.newItem["item_type"] and\
            json["unit_purchase_quantity"] == self.newItem["unit_purchase_quantity"] and\
            json["unit_order_quantity"] == self.newItem["unit_order_quantity"] and\
            json["pack_order_quantity"] == self.newItem["pack_order_quantity"] and\
            json["supplier_id"] == self.newItem["supplier_id"] and\
            json["supplier_code"] == self.newItem["supplier_code"] and\
            json["supplier_part_number"] == self.newItem["supplier_part_number"] , "Item should be updated"
        assert responsePut.status_code == 200, "Correct item should return 200"

    # def test_put_empty_item_endpoint(self):
    #     responsePut = requests.put(f"{BASE_URL}/api/v1/items/P999999", headers=self.headers_full, json={})
    #     assert responsePut.status_code == 400, "Empty item should return 400"

    # def test_put_missing_item_endpoint(self):
    #     responsePut = requests.put(f"{BASE_URL}/api/v1/items/P999999", headers=self.headers_full, json=self.incorrectItem)
    #     assert responsePut.status_code == 400, "Missing item should return 400"

    def test_delete_correct_endpoint(self):
        responseDelete = requests.delete(f"{BASE_URL}/api/v1/items/P999999", headers=self.headers_full)
        assert responseDelete.status_code == 200, "Correct item should return 200"