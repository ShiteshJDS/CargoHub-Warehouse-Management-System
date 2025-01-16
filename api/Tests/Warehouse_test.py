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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.warehouses import Warehouses  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder
@pytest.fixture(scope="module", autouse=True)
def manage_warehouse_db_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_file_path = os.path.join(current_dir, "../Test_Data/cargohub_test.db")
    backup_file_path = f"{db_file_path}.backup"

    # Backup the database file
    shutil.copyfile(db_file_path, backup_file_path)

    yield  # Run the tests

    # Restore the database file from backup
    shutil.copyfile(backup_file_path, db_file_path)
    os.remove(backup_file_path)  # Clean up the backup file

class Test_Warehouses_Endpoints():

    warehousesObject = Warehouses("api/Tests/Test_Data/cargohub_test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newWarehouse = {
        "id": pow(10, 100),
        "code": "YQZZNL56",
        "name": "Heemskerk cargo hub",
        "address": "Karlijndreef 281",
        "zip": "4002 AS",
        "city": "Heemskerk",
        "province": "Friesland",
        "country": "NL",
        "contact":
        {
            "name": "Fem Keijzer",
            "phone": "(078) 0013363",
            "email": "blamore@example.net"
        },
        "created_at": "-",
        "updated_at": "-"
    }

    # Warehouse Endpoint Testing (server must be running when testing endpoints)
    def test_post_endpoints(self):

        def test_post_correct_endpoint():
            responsePost = requests.post(
                f"{BASE_URL}/api/v1/warehouses", headers=self.headers_full, json=self.newWarehouse)
            new_timestamp = self.warehousesObject.get_timestamp()
            self.newWarehouse["created_at"] = new_timestamp.split('T')[0]
            self.newWarehouse["updated_at"] = new_timestamp.split('T')[0]
            assert responsePost.status_code == 201, "test_post_correct_endpoint"

        def test_post_existing_id_endpoint():
            responsePost = requests.post(
                f"{BASE_URL}/api/v1/warehouses", headers=self.headers_full, json=self.newWarehouse)
            assert responsePost.status_code == 403, "test_post_existing_id_endpoint"

        def test_post_missing_items_endpoint():
            missing_items_warehouse = copy.deepcopy(self.newWarehouse)
            for i in ['id', 'code', 'city']:
                missing_items_warehouse.pop(i)

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/warehouses", headers=self.headers_full, json=missing_items_warehouse)
            assert responsePost.status_code == 403, "test_post_missing_items_endpoint"

        def test_post_extra_items_endpoint():
            extra_items_warehouse = copy.deepcopy(self.newWarehouse)
            extra_items_warehouse.update({"a": 1, "b": 2, "c": 3})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/warehouses", headers=self.headers_full, json=extra_items_warehouse)
            assert responsePost.status_code == 403, "test_post_extra_items_endpoint"

        def test_post_wrong_types_endpoint():
            wrong_types_warehouse = copy.deepcopy(self.newWarehouse)
            wrong_types_warehouse.update(
                {"id": True, "code": [1, 2, 3], "city": 1})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/warehouses", headers=self.headers_full, json=wrong_types_warehouse)
            assert responsePost.status_code == 403, "test_post_wrong_types_endpoint"

        def test_post_empty_values_endpoint():
            empty_values_warehouse = copy.deepcopy(self.newWarehouse)
            empty_values_warehouse.update(
                {"code": "", "zip": "", "city": ""})

            responsePost = requests.post(
                f"{BASE_URL}/api/v1/warehouses", headers=self.headers_full, json=empty_values_warehouse)
            assert responsePost.status_code == 403, "test_post_empty_values_endpoint"

        test_post_correct_endpoint()
        test_post_existing_id_endpoint()    # ?? Multiple id's
        test_post_missing_items_endpoint()  # ?? Missing items
        test_post_extra_items_endpoint()    # ?? Extra items
        test_post_wrong_types_endpoint()    # ?? Wrong item types
        test_post_empty_values_endpoint()   # ?? Empty items

    def test_put_endpoints(self):

        def test_put_correct_endpoint():
            self.newWarehouse.update({"code": "Y4ZYNL57", "city": "Rotterdam", "contact": {
                                     "name": "Kevin Krul", "phone": "(079) 0318253", "email": "kevin@example.net"}})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full, json=self.newWarehouse)
            self.newWarehouse["updated_at"] = self.warehousesObject.get_timestamp().split('T')[0]
            assert responsePut.status_code == 200, "test_put_correct_endpoint"

        def test_put_nonexistent_id_endpoint():
            responsePut = requests.put(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']+1}", headers=self.headers_full, json=self.newWarehouse)
            assert responsePut.status_code == 403, "test_put_nonexistent_id_endpoint"

        def test_put_missing_items_endpoint():
            missing_items_warehouse = copy.deepcopy(self.newWarehouse)
            for i in ['id', 'code', 'city']:
                missing_items_warehouse.pop(i)

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full, json=missing_items_warehouse)
            assert responsePut.status_code == 403, "test_put_missing_items_endpoint"

        def test_put_extra_items_endpoint():
            extra_items_warehouse = copy.deepcopy(self.newWarehouse)
            extra_items_warehouse.update({"a": 1, "b": 2, "c": 3})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full, json=extra_items_warehouse)
            assert responsePut.status_code == 403, "test_put_extra_items_endpoint"

        def test_put_wrong_types_endpoint():
            wrong_types_warehouse = copy.deepcopy(self.newWarehouse)
            wrong_types_warehouse.update(
                {"id": True, "code": [1, 2, 3], "city": 1})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full, json=wrong_types_warehouse)
            assert responsePut.status_code == 403, "test_put_wrong_types_endpoint"

        def test_put_empty_values_endpoint():
            empty_values_warehouse = copy.deepcopy(self.newWarehouse)
            empty_values_warehouse.update(
                {"code": "", "zip": "", "city": ""})

            responsePut = requests.put(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full, json=empty_values_warehouse)
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
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full)
            dict_response = responseGet.json()
            dict_response["created_at"] = dict_response["created_at"].split('T')[0]
            dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
            assert responseGet.status_code == 200, "test_get_by_id_correct_endpoint"
            assert dict_response == self.newWarehouse, "test_get_by_id_correct_endpoint"

        def test_get_all_correct_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/warehouses", headers=self.headers_full)
            assert responseGet.status_code == 200, "test_get_all_correct_endpoint"
            assert self.newWarehouse["id"] in [w["id"] for w in responseGet.json()], "test_get_all_correct_endpoint"

        def test_get_locations_correct_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}/locations", headers=self.headers_full)
            assert responseGet.status_code == 200, "test_get_locations_correct_endpoint"
            assert len(responseGet.json()) == 0, "test_get_locations_correct_endpoint"

        def test_get_by_id_nonexistent_id_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']+1}", headers=self.headers_full)
            assert responseGet.status_code == 403, "test_get_by_id_nonexistent_id_endpoint"

        def test_get_locations_nonexistent_id_endpoint():
            responseGet = requests.get(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']+1}/locations", headers=self.headers_full)
            assert responseGet.status_code == 403, "test_get_locations_nonexistent_id_endpoint"

        test_get_by_id_correct_endpoint()
        test_get_all_correct_endpoint()
        test_get_locations_correct_endpoint()
        test_get_by_id_nonexistent_id_endpoint()        # ?? Nonexistent id's
        test_get_locations_nonexistent_id_endpoint()    # ?? Nonexistent id's

    def test_delete_endpoints(self):

        def test_delete_correct_endpoint():
            responseDelete = requests.delete(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full)
            assert responseDelete.status_code == 200, "test_delete_correct_endpoint"

        def test_delete_nonexistent_id_endpoint():
            responseDelete = requests.delete(
                f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']+1}", headers=self.headers_full)
            assert responseDelete.status_code == 403, "test_delete_nonexistent_id_endpoint"

        test_delete_correct_endpoint()
        test_delete_nonexistent_id_endpoint()   # ?? Nonexistent id's

    def test_endpoint_restrictions(self):

        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/warehouses", headers=headers_restricted, json=self.newWarehouse)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=headers_restricted, json=self.newWarehouse)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=headers_restricted)
        responseGetAll_restricted = requests.get(
            f"{BASE_URL}/api/v1/warehouses", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=headers_restricted)
        responseGetLocations_restricted = requests.get(
            f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}/locations", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403, "Post failed"
        assert responsePut_restricted.status_code == 403, "Put failed"
        assert responseDelete_restricted.status_code == 403, "Delete failed"

        assert responseGetAll_restricted.status_code == 200, "Get All failed"
        assert responseGet_restricted.status_code == 200, "Get by id failed"
        assert responseGetLocations_restricted.status_code == 200, "Get locations failed"


class Test_Warehouses_Functions():

    warehousesObject = Warehouses("api/Tests/Test_Data/cargohub_test.db")

    def test_get_warehouses(self):

        allWarehouses = self.warehousesObject.get_warehouses()
        assert allWarehouses == [
            {
                "id": 1,
                "code": "YQZZNL56",
                "name": "Heemskerk cargo hub",
                "address": "Karlijndreef 281",
                "zip": "4002 AS",
                "city": "Heemskerk",
                "province": "Friesland",
                "country": "NL",
                "contact": {
                    "name": "Fem Keijzer",
                    "phone": "(078) 0013363",
                    "email": "blamore@example.net"
                },
                "created_at": "1983-04-13 04:59:55",
                "updated_at": "2007-02-08 20:11:00"
            },
            {
                "id": 2,
                "code": "GIOMNL90",
                "name": "Petten longterm hub",
                "address": "Owenweg 731",
                "zip": "4615 RB",
                "city": "Petten",
                "province": "Noord-Holland",
                "country": "NL",
                "contact": {
                    "name": "Maud Adryaens",
                    "phone": "+31836 752702",
                    "email": "nickteunissen@example.com"
                },
                "created_at": "2008-02-22 19:55:39",
                "updated_at": "2009-08-28 23:15:50"
            },
            {
                "id": 3,
                "code": "VCKINLLK",
                "name": "Naaldwijk distribution hub",
                "address": "Izesteeg 807",
                "zip": "1636 KI",
                "city": "Naaldwijk",
                "province": "Utrecht",
                "country": "NL",
                "contact": {
                    "name": "Frederique van Wallaert",
                    "phone": "(009) 4870289",
                    "email": "jelle66@example.net"
                },
                "created_at": "2001-05-11 10:43:52",
                "updated_at": "2017-12-19 14:32:38"
            }
        ], "The warehouse database doesn't match the expected data"

    def test_get_warehouse_with_id(self):
        warehouse2 = self.warehousesObject.get_warehouse(2)
        assert warehouse2 == {
            "id": 2,
            "code": "GIOMNL90",
            "name": "Petten longterm hub",
            "address": "Owenweg 731",
            "zip": "4615 RB",
            "city": "Petten",
            "province": "Noord-Holland",
            "country": "NL",
            "contact": {
                "name": "Maud Adryaens",
                "phone": "+31836 752702",
                "email": "nickteunissen@example.com"
            },
            "created_at": "2008-02-22 19:55:39",
            "updated_at": "2009-08-28 23:15:50"
        }, "The warehouse with id 2 wasn't found in the warehouse database"

    def test_add_warehouse(self):
        new_warehouse = {
            "id": 4,
            "code": "VCKINLLK",
            "name": "Naaldwijk distribution hub",
            "address": "Izesteeg 807",
            "zip": "1636 KI",
            "city": "Naaldwijk",
            "province": "Utrecht",
            "country": "NL",
            "contact": {
                "name": "Frederique van Wallaert",
                "phone": "(009) 4870289",
                "email": "jelle66@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        }
        self.warehousesObject.add_warehouse(new_warehouse)
        new_timestamp = self.warehousesObject.get_timestamp()
        new_warehouse["created_at"] = new_timestamp
        new_warehouse["updated_at"] = new_timestamp

        assert self.warehousesObject.get_warehouse(4) == new_warehouse, \
            "The new warehouse wasn't saved correctly, or get_warehouse doesn't function properly"

    def test_update_warehouse(self):
        updated_warehouse = {
            "id": 4,
            "code": "ABCDEFG",                          # <- Changed
            "name": "Rotterdam distribution hub",       # <- Changed
            "address": "Izesteeg 807",
            "zip": "1636 KI",
            "city": "Rotterdam",                        # <- Changed
            "province": "Zuid-Holland",
            "country": "NL",
            "contact": {
                "name": "Fred van Wallaert",            # <- Changed
                "phone": "(009) 123456789",             # <- Changed
                "email": "jelle77@example.net"          # <- Changed
            },
            "created_at": "2001-05-11 10:43:52",
            "updated_at": "-"
        }

        self.warehousesObject.update_warehouse(4, updated_warehouse)
        new_timestamp = self.warehousesObject.get_timestamp()
        updated_warehouse["updated_at"] = new_timestamp

        assert self.warehousesObject.get_warehouse(4) == updated_warehouse, \
            "The new warehouse wasn't updated correctly, or get_warehouse doesn't function properly."

    def test_remove_warehouse(self):

        self.warehousesObject.remove_warehouse(4)
        assert self.warehousesObject.get_warehouse(4) is None, \
            "Warehouse with ID 4 wasn't removed correctly, or get_warehouse doesn't function properly."