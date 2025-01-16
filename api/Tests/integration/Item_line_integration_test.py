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
    os.path.join(os.path.dirname(__file__), '..', '..')))

from models.item_lines import ItemLines  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

class Test_ItemLines():

    item_lineObject = ItemLines("../Test_Data/Cargohub_Test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newItemLine = {
        "id": pow(10, 100),
        "name": "Sports Gear",
        "description": "",
        "created_at": "-",
        "updated_at": "-"
    }
    # ItemGroup Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoints(self):

        def test_post_correct_endpoint():
            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_lines/", headers=self.headers_full, json=self.newItemLine)
            new_timestamp = self.item_lineObject.get_timestamp()
            self.newItemLine["created_at"] = new_timestamp.split('T')[0]
            self.newItemLine["updated_at"] = new_timestamp.split('T')[0]
            assert responsePost.status_code == 201, "test_post_correct_endpoint"

        def test_post_existing_id_endpoint():
            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_lines", headers=self.headers_full, json=self.newItemLine)
            assert responsePost.status_code == 403, "test_post_existing_id_endpoint"

        def test_post_missing_items_endpoint():
            missing_items_item_group = copy.deepcopy(self.newItemLine)
            for i in ['id', 'name', 'description']:
                missing_items_item_group.pop(i)

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_lines", headers=self.headers_full, json=missing_items_item_group)
            assert responsePost.status_code == 403, "test_post_missing_items_endpoint"

        def test_post_extra_items_endpoint():
            extra_items_item_group = copy.deepcopy(self.newItemLine)
            extra_items_item_group.update({"a": 1, "b": 2, "c": 3})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_lines", headers=self.headers_full, json=extra_items_item_group)
            assert responsePost.status_code == 403, "test_post_extra_items_endpoint"

        def test_post_wrong_types_endpoint():
            wrong_types_item_group = copy.deepcopy(self.newItemLine)
            wrong_types_item_group.update(
                {"id": True, "name": 1, "description": [1, 2, 3]})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_lines", headers=self.headers_full, json=wrong_types_item_group)
            assert responsePost.status_code == 403, "test_post_wrong_types_endpoint"

        def test_post_empty_values_endpoint():
            empty_values_item_group = copy.deepcopy(self.newItemLine)
            empty_values_item_group.update(
                {"name": "", "description": ""})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/item_lines", headers=self.headers_full, json=empty_values_item_group)
            assert responsePost.status_code == 403, "test_post_empty_values_endpoint"

        test_post_correct_endpoint()
        test_post_existing_id_endpoint()    # ?? Multiple id's
        test_post_missing_items_endpoint()  # ?? Missing items
        test_post_extra_items_endpoint()    # ?? Extra items
        test_post_wrong_types_endpoint()    # ?? Wrong item types
        test_post_empty_values_endpoint()   # ?? Empty items

    def test_put_endpoints(self):

        def test_put_correct_endpoint():
            self.newItemLine["name"] = "Tech Gadgets"
            self.newItemLine["description"] = "Things with wires"

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full, json=self.newItemLine)
            self.newItemLine["updated_at"] = self.item_lineObject.get_timestamp().split('T')[
                0]
            assert responsePut.status_code == 200

        def test_put_nonexistent_id_endpoint():
            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']+1}", headers=self.headers_full, json=self.newItemLine)
            assert responsePut.status_code == 403, "test_put_nonexistent_id_endpoint"

        def test_put_missing_items_endpoint():
            missing_items_item_group = copy.deepcopy(self.newItemLine)
            for i in ['id', 'name', 'description']:
                missing_items_item_group.pop(i)

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full, json=missing_items_item_group)
            assert responsePut.status_code == 403, "test_put_missing_items_endpoint"

        def test_put_extra_items_endpoint():
            extra_items_item_group = copy.deepcopy(self.newItemLine)
            extra_items_item_group.update({"a": 1, "b": 2, "c": 3})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full, json=extra_items_item_group)
            assert responsePut.status_code == 403, "test_put_extra_items_endpoint"

        def test_put_wrong_types_endpoint():
            wrong_types_item_group = copy.deepcopy(self.newItemLine)
            wrong_types_item_group.update(
                {"id": True, "name": 1, "description": [1, 2, 3]})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_group/{self.newItemLine['id']}", headers=self.headers_full, json=wrong_types_item_group)
            assert responsePut.status_code == 403, "test_put_wrong_types_endpoint"

        def test_put_empty_values_endpoint():
            empty_values_item_group = copy.deepcopy(self.newItemLine)
            empty_values_item_group.update(
                {"name": "", "description": ""})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full, json=empty_values_item_group)
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
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full)
            dict_response = responseGet.json()
            dict_response["created_at"] = dict_response["created_at"].split('T')[
                0]
            dict_response["updated_at"] = dict_response["updated_at"].split('T')[
                0]
            assert responseGet.status_code == 200, "test_get_by_id_correct_endpoint"
            assert dict_response == self.newItemLine, "test_get_by_id_correct_endpoint"

        def test_get_all_correct_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_lines", headers=self.headers_full)
            assert responseGet.status_code == 200, "test_get_all_correct_endpoint"
            assert self.newItemLine["id"] in [ig["id"]
                                              for ig in responseGet.json()], "test_get_all_correct_endpoint"

        def test_get_items_correct_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}/items", headers=self.headers_full)
            assert responseGet.status_code == 200, "test_get_items_correct_endpoint"
            assert len(responseGet.json()
                       ) == 0, "test_get_items_correct_endpoint"

        def test_get_by_id_nonexistent_id_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']+1}", headers=self.headers_full)
            assert responseGet.status_code == 403, "test_get_by_id_nonexistent_id_endpoint"

        def test_get_locations_nonexistent_id_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']+1}/locations", headers=self.headers_full)
            assert responseGet.status_code == 403, "test_get_locations_nonexistent_id_endpoint"

        test_get_by_id_correct_endpoint()
        test_get_all_correct_endpoint()
        test_get_items_correct_endpoint()
        test_get_by_id_nonexistent_id_endpoint()        # ?? Nonexistent id's
        test_get_locations_nonexistent_id_endpoint()    # ?? Nonexistent id's

    def test_delete_endpoints(self):

        def test_delete_correct_endpoint():
            responseDelete = requests.delete(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=self.headers_full)
            assert responseDelete.status_code == 200, "test_delete_correct_endpoint"

        def test_delete_nonexistent_id_endpoint():
            responseDelete = requests.delete(
                f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']+1}", headers=self.headers_full)
            assert responseDelete.status_code == 403, "test_delete_nonexistent_id_endpoint"

        test_delete_correct_endpoint()
        test_delete_nonexistent_id_endpoint()   # ?? Nonexistent id's

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
        responseGetAll_restricted = requests.get(
            f"{BASE_URL}/api/v1/item_lines", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}", headers=headers_restricted)
        responseGetItems_restricted = requests.get(
            f"{BASE_URL}/api/v1/item_lines/{self.newItemLine['id']}/items", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403, "Post failed"
        assert responsePut_restricted.status_code == 403, "Put failed"
        assert responseDelete_restricted.status_code == 403, "Delete failed"
        assert responseGetAll_restricted.status_code == 200, "Get All failed"
        assert responseGet_restricted.status_code == 200, "Get by id failed"
        assert responseGetItems_restricted.status_code == 200, "Get items failed"
