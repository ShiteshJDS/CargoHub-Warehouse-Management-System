import pytest
import unittest
import sys
import os
import requests
import logging
import shutil
import copy
from dotenv import load_dotenv

load_dotenv()

# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from models.item_groups import ItemGroups  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

@pytest.fixture(scope="module", autouse=True)
def manage_warehouse_json_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../../data/item_groups.json")
    backup_file_path = f"{json_file_path}.backup"

    # Backup the JSON file
    shutil.copyfile(json_file_path, backup_file_path)

    yield  # Run the tests

    # Restore the JSON file from backup
    shutil.copyfile(backup_file_path, json_file_path)
    os.remove(backup_file_path)  # Clean up the backup file

class Test_ItemGroups():

    item_groupObject = ItemGroups("Test_Data/Cargohub_Test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newItemGroup = {
        "id": pow(10, 100),
        "name": "Toys",
        "description": "",
        "created_at": "-",
        "updated_at": "-"
    }

    # ItemGroup Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoints(self):

        def test_post_correct_endpoint():
            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_groups/", headers=self.headers_full, json=self.newItemGroup)
            new_timestamp = self.item_groupObject.get_timestamp()
            self.newItemGroup["created_at"] = new_timestamp.split('T')[0]
            self.newItemGroup["updated_at"] = new_timestamp.split('T')[0]
            assert responsePost.status_code == 201, "test_post_correct_endpoint"

        def test_post_existing_id_endpoint():
            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_groups", headers=self.headers_full, json=self.newItemGroup)
            assert responsePost.status_code == 403, "test_post_existing_id_endpoint"

        def test_post_missing_items_endpoint():
            missing_items_item_group = copy.deepcopy(self.newItemGroup)
            for i in ['id', 'name', 'description']:
                missing_items_item_group.pop(i)

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_groups", headers=self.headers_full, json=missing_items_item_group)
            assert responsePost.status_code == 403, "test_post_missing_items_endpoint"

        def test_post_extra_items_endpoint():
            extra_items_item_group = copy.deepcopy(self.newItemGroup)
            extra_items_item_group.update({"a": 1, "b": 2, "c": 3})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_groups", headers=self.headers_full, json=extra_items_item_group)
            assert responsePost.status_code == 403, "test_post_extra_items_endpoint"

        def test_post_wrong_types_endpoint():
            wrong_types_item_group = copy.deepcopy(self.newItemGroup)
            wrong_types_item_group.update(
                {"id": True, "name": 1, "description": [1, 2, 3]})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_groups", headers=self.headers_full, json=wrong_types_item_group)
            assert responsePost.status_code == 403, "test_post_wrong_types_endpoint"

        def test_post_empty_values_endpoint():
            empty_values_item_group = copy.deepcopy(self.newItemGroup)
            empty_values_item_group.update(
                {"name": "", "description": ""})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_groups", headers=self.headers_full, json=empty_values_item_group)
            assert responsePost.status_code == 403, "test_post_empty_values_endpoint"

        test_post_correct_endpoint()
        test_post_existing_id_endpoint()    # ?? Multiple id's
        test_post_missing_items_endpoint()  # ?? Missing items
        test_post_extra_items_endpoint()    # ?? Extra items
        test_post_wrong_types_endpoint()    # ?? Wrong item types
        test_post_empty_values_endpoint()   # ?? Empty items

    def test_put_endpoints(self):

        def test_put_correct_endpoint():
            self.newItemGroup["name"] = "Electronics"
            self.newItemGroup["description"] = "Things with wires"

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=self.headers_full, json=self.newItemGroup)
            self.newItemGroup["updated_at"] = self.item_groupObject.get_timestamp().split('T')[
                0]
            assert responsePut.status_code == 200

        def test_put_nonexistent_id_endpoint():
            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']+1}", headers=self.headers_full, json=self.newItemGroup)
            assert responsePut.status_code == 403, "test_put_nonexistent_id_endpoint"

        def test_put_missing_items_endpoint():
            missing_items_item_group = copy.deepcopy(self.newItemGroup)
            for i in ['id', 'name', 'description']:
                missing_items_item_group.pop(i)

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=self.headers_full, json=missing_items_item_group)
            assert responsePut.status_code == 403, "test_put_missing_items_endpoint"

        def test_put_extra_items_endpoint():
            extra_items_item_group = copy.deepcopy(self.newItemGroup)
            extra_items_item_group.update({"a": 1, "b": 2, "c": 3})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=self.headers_full, json=extra_items_item_group)
            assert responsePut.status_code == 403, "test_put_extra_items_endpoint"

        def test_put_wrong_types_endpoint():
            wrong_types_item_group = copy.deepcopy(self.newItemGroup)
            wrong_types_item_group.update(
                {"id": True, "name": 1, "description": [1, 2, 3]})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_group/{self.newItemGroup['id']}", headers=self.headers_full, json=wrong_types_item_group)
            assert responsePut.status_code == 403, "test_put_wrong_types_endpoint"

        def test_put_empty_values_endpoint():
            empty_values_item_group = copy.deepcopy(self.newItemGroup)
            empty_values_item_group.update(
                {"name": "", "description": ""})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=self.headers_full, json=empty_values_item_group)
            assert responsePut.status_code == 403, "test_put_empty_values_endpoint"

        test_put_correct_endpoint()
        test_put_nonexistent_id_endpoint()  # ?? Existing id's
        test_put_missing_items_endpoint()   # ?? Missing items
        test_put_extra_items_endpoint()     # ?? Extra items
        test_put_wrong_types_endpoint()     # ?? Wrong item types
        test_put_empty_values_endpoint()    # ?? Empty items

    def test_get_endpoints(self):

        def test_get_by_id_correct_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=self.headers_full)
            dict_response = responseGet.json()
            dict_response["created_at"] = dict_response["created_at"].split('T')[
                0]
            dict_response["updated_at"] = dict_response["updated_at"].split('T')[
                0]
            assert responseGet.status_code == 200, "test_get_by_id_correct_endpoint"
            assert dict_response == self.newItemGroup, "test_get_by_id_correct_endpoint"

        def test_get_all_correct_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_groups", headers=self.headers_full)
            assert responseGet.status_code == 200, "test_get_all_correct_endpoint"
            assert self.newItemGroup["id"] in [ig["id"]
                                               for ig in responseGet.json()], "test_get_all_correct_endpoint"

        def test_get_items_correct_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}/items", headers=self.headers_full)
            assert responseGet.status_code == 200, "test_get_items_correct_endpoint"
            assert len(responseGet.json()
                       ) == 0, "test_get_items_correct_endpoint"

        def test_get_by_id_nonexistent_id_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']+1}", headers=self.headers_full)
            assert responseGet.status_code == 403, "test_get_by_id_nonexistent_id_endpoint"

        def test_get_locations_nonexistent_id_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']+1}/locations", headers=self.headers_full)
            assert responseGet.status_code == 403, "test_get_locations_nonexistent_id_endpoint"

        test_get_by_id_correct_endpoint()
        test_get_all_correct_endpoint()
        test_get_items_correct_endpoint()
        test_get_by_id_nonexistent_id_endpoint()        # ?? Nonexistent id's
        test_get_locations_nonexistent_id_endpoint()    # ?? Nonexistent id's

    def test_delete_endpoints(self):

        def test_delete_correct_endpoint():
            responseDelete = requests.delete(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=self.headers_full)
            assert responseDelete.status_code == 200, "test_delete_correct_endpoint"

        def test_delete_nonexistent_id_endpoint():
            responseDelete = requests.delete(
                f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']+1}", headers=self.headers_full)
            assert responseDelete.status_code == 403, "test_delete_nonexistent_id_endpoint"

        test_delete_correct_endpoint()
        test_delete_nonexistent_id_endpoint()   # ?? Nonexistent id's

    def test_endpoint_restrictions(self):

        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/item_groups/", headers=headers_restricted, json=self.newItemGroup)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=headers_restricted, json=self.newItemGroup)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=headers_restricted)
        responseGetAll_restricted = requests.get(
            f"{BASE_URL}/api/v1/item_groups", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}", headers=headers_restricted)
        responseGetItems_restricted = requests.get(
            f"{BASE_URL}/api/v1/item_groups/{self.newItemGroup['id']}/items", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403, "Post failed"
        assert responsePut_restricted.status_code == 403, "Put failed"
        assert responseDelete_restricted.status_code == 403, "Delete failed"
        assert responseGetAll_restricted.status_code == 200, "Get All failed"
        assert responseGet_restricted.status_code == 200, "Get by id failed"
        assert responseGetItems_restricted.status_code == 200, "Get items failed"


class Test_Item_groups_Functions():

    item_groupObject = ItemGroups("Test_Data/Cargohub_Test.db")

    def test_get_item_groups(self):

        allItemGroups = self.item_groupObject.get_item_groups()
        assert allItemGroups == [
            {
                "id": 1,
                "name": "Furniture",
                "description": "",
                "created_at": "2019-09-22 15:51:07",
                "updated_at": "2022-05-18 13:49:28"
            },
            {
                "id": 2,
                "name": "Stationery",
                "description": "",
                "created_at": "1999-08-14 13:39:27",
                "updated_at": "2011-06-16 05:00:47"
            },
            {
                "id": 3,
                "name": "Clothing",
                "description": "",
                "created_at": "1975-12-14 06:58:09",
                "updated_at": "2011-12-04 21:16:55"
            }
        ], "The item_group database doesn't match the expected data"

    def test_get_item_group_with_id(self):
        item_group2 = self.item_groupObject.get_item_group(2)
        assert item_group2 == {
            "id": 2,
            "name": "Stationery",
            "description": "",
            "created_at": "1999-08-14 13:39:27",
            "updated_at": "2011-06-16 05:00:47"
        }, "The item_group with id 2 wasn't found in the item_group database"

    def test_add_item_group(self):
        new_item_group = {
            "id": 4,
            "name": "Home Decor",
            "description": "",
            "created_at": "-",
            "updated_at": "-"
        }
        self.item_groupObject.add_item_group(new_item_group)
        new_timestamp = self.item_groupObject.get_timestamp()
        new_item_group["created_at"] = new_timestamp
        new_item_group["updated_at"] = new_timestamp

        assert self.item_groupObject.get_item_group(4) == new_item_group, \
            "The new item_group wasn't saved correctly, or get_item_group doesn't function properly"

    def test_update_item_group(self):
        updated_item_group = {
            "id": 4,
            "name": "Toys",                 # <- Changed
            "description": "For kids",      # <- Changed
            "created_at": "-",
            "updated_at": "-"
        }

        self.item_groupObject.update_item_group(4, updated_item_group)
        new_timestamp = self.item_groupObject.get_timestamp()
        updated_item_group["updated_at"] = new_timestamp

        assert self.item_groupObject.get_item_group(4) == updated_item_group, \
            "The new item_group wasn't updated correctly, or get_item_group doesn't function properly."

    def test_remove_item_group(self):

        self.item_groupObject.remove_item_group(4)
        assert self.item_groupObject.get_item_group(4) == None, \
            "Item_group with ID 4 wasn't removed correctly, or get_item_group doesn't function properly."
