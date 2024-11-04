
import pytest
import unittest
import sys
import os
import requests
import logging


# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from models.item_lines import ItemLines  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


class Test_ItemLines():

    item_lineObject = ItemLines("Test_Data/test_")
    headers_full = {
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
    }

    newItemLine = {
        "id": -1,
        "name": "Sports Gear",
        "description": "",
        "created_at": "-",
        "updated_at": "-"
    }

    # ItemLine Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/item_lines/", headers=self.headers_full, json=self.newItemLine)
        new_timestamp = self.item_lineObject.get_timestamp()
        self.newItemLine["created_at"] = new_timestamp.split('T')[0]
        self.newItemLine["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newItemLine["name"] = "Electronics"
        self.newItemLine["description"] = "Things with wires"

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full, json=self.newItemLine)
        self.newItemLine["updated_at"] = self.item_lineObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newItemLine

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restrictions(self):

        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/item_lines/", headers=headers_restricted, json=self.newItemLine)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=headers_restricted, json=self.newItemLine)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200

    # ItemLines Method Testing

    def test_get_item_lines(self):

        allItemLines = self.item_lineObject.get_item_lines()
        assert allItemLines == [
            {
                "id": 1,
                "name": "Home Appliances",
                "description": "",
                "created_at": "1979-01-16 07:07:50",
                "updated_at": "2024-01-05 23:53:25"
            },
            {
                "id": 2,
                "name": "Office Supplies",
                "description": "",
                "created_at": "2009-07-18 08:13:40",
                "updated_at": "2020-01-12 14:32:49"
            },
            {
                "id": 3,
                "name": "Fashion",
                "description": "",
                "created_at": "1990-01-04 22:40:49",
                "updated_at": "2003-05-17 08:21:43"
            }
        ], "The item_line database doesn't match the expected data"

    def test_get_item_line_with_id(self):
        item_line2 = self.item_lineObject.get_item_line(2)
        assert item_line2 == {
            "id": 2,
            "name": "Office Supplies",
            "description": "",
            "created_at": "2009-07-18 08:13:40",
            "updated_at": "2020-01-12 14:32:49"
        }, "The item_line with id 2 wasn't found in the item_line database"

    def test_add_item_line(self):
        new_item_line = {
            "id": 4,
            "name": "Home Decor",
            "description": "",
            "created_at": "-",
            "updated_at": "-"
        }
        self.item_lineObject.add_item_line(new_item_line)
        new_timestamp = self.item_lineObject.get_timestamp()
        new_item_line["created_at"] = new_timestamp
        new_item_line["updated_at"] = new_timestamp

        assert self.item_lineObject.get_item_line(4) == new_item_line, \
            "The new item_line wasn't saved correctly, or get_item_line doesn't function properly"

    def test_update_item_line(self):
        updated_item_line = {
            "id": 4,
            "name": "Toys",                 # <- Changed
            "description": "For kids",      # <- Changed
            "created_at": "-",
            "updated_at": "-"
        }

        self.item_lineObject.update_item_line(4, updated_item_line)
        new_timestamp = self.item_lineObject.get_timestamp()
        updated_item_line["updated_at"] = new_timestamp

        assert self.item_lineObject.get_item_line(4) == updated_item_line, \
            "The new item_line wasn't updated correctly, or get_item_line doesn't function properly."

    def test_remove_item_line(self):

        self.item_lineObject.remove_item_line(4)
        assert self.item_lineObject.get_item_line(4) == None, \
            "Item_line with ID 4 wasn't removed correctly, or get_item_line doesn't function properly."
