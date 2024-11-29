
import pytest
import unittest
import sys
import os
import requests
import logging
import shutil

# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from models.item_types import ItemTypes  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

@pytest.fixture(scope="module", autouse=True)
def manage_warehouse_json_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../../data/item_types.json")
    backup_file_path = f"{json_file_path}.backup"

    # Backup the JSON file
    shutil.copyfile(json_file_path, backup_file_path)

    yield  # Run the tests

    # Restore the JSON file from backup
    shutil.copyfile(backup_file_path, json_file_path)
    os.remove(backup_file_path)  # Clean up the backup file

class Test_ItemTypes():

    item_typeObject = ItemTypes("Test_Data/test_")
    headers_full = {
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
    }

    newItemType = {
        "id": -1,
        "name": "Calculator",
        "description": "",
        "created_at": "-",
        "updated_at": "-"
    }

    # ItemType Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/item_types/", headers=self.headers_full, json=self.newItemType)
        new_timestamp = self.item_typeObject.get_timestamp()
        self.newItemType["created_at"] = new_timestamp.split('T')[0]
        self.newItemType["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newItemType["name"] = "Electronics"
        self.newItemType["description"] = "Things with wires"

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/item_types/{self.newItemType['id']}", headers=self.headers_full, json=self.newItemType)
        self.newItemType["updated_at"] = self.item_typeObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/item_types/{self.newItemType['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newItemType

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/item_types/{self.newItemType['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restrictions(self):

        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/item_types/", headers=headers_restricted, json=self.newItemType)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/item_types/{self.newItemType['id']}", headers=headers_restricted, json=self.newItemType)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/item_types/{self.newItemType['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/item_types/{self.newItemType['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200

    # ItemType Method Testing

    def test_get_item_types(self):

        allItemTypes = self.item_typeObject.get_item_types()
        assert allItemTypes == [
            {
                "id": 1,
                "name": "Desktop",
                "description": "",
                "created_at": "1993-07-28 13:43:32",
                "updated_at": "2022-05-12 08:54:35"
            },
            {
                "id": 2,
                "name": "Tablet",
                "description": "",
                "created_at": "1977-05-01 00:05:04",
                "updated_at": "2001-04-14 02:41:59"
            },
            {
                "id": 3,
                "name": "Smartphone",
                "description": "",
                "created_at": "2014-08-23 03:26:57",
                "updated_at": "2017-09-20 11:51:15"
            }
        ], "The item_type database doesn't match the expected data"

    def test_get_item_type_with_id(self):
        item_type2 = self.item_typeObject.get_item_type(2)
        assert item_type2 == {
            "id": 2,
            "name": "Tablet",
            "description": "",
            "created_at": "1977-05-01 00:05:04",
            "updated_at": "2001-04-14 02:41:59"
        }, "The item_type with id 2 wasn't found in the item_type database"

    def test_add_item_type(self):
        new_item_type = {
            "id": 4,
            "name": "Home Decor",
            "description": "",
            "created_at": "-",
            "updated_at": "-"
        }
        self.item_typeObject.add_item_type(new_item_type)
        new_timestamp = self.item_typeObject.get_timestamp()
        new_item_type["created_at"] = new_timestamp
        new_item_type["updated_at"] = new_timestamp

        assert self.item_typeObject.get_item_type(4) == new_item_type, \
            "The new item_type wasn't saved correctly, or get_item_type doesn't function properly"

    def test_update_item_type(self):
        updated_item_type = {
            "id": 4,
            "name": "Toys",                 # <- Changed
            "description": "For kids",      # <- Changed
            "created_at": "-",
            "updated_at": "-"
        }

        self.item_typeObject.update_item_type(4, updated_item_type)
        new_timestamp = self.item_typeObject.get_timestamp()
        updated_item_type["updated_at"] = new_timestamp

        assert self.item_typeObject.get_item_type(4) == updated_item_type, \
            "The new item_type wasn't updated correctly, or get_item_type doesn't function properly."

    def test_remove_item_type(self):

        self.item_typeObject.remove_item_type(4)
        assert self.item_typeObject.get_item_type(4) == None, \
            "Item_type with ID 4 wasn't removed correctly, or get_item_type doesn't function properly."
