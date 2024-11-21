# from models.warehouses import Warehouses
from models.warehouses import Warehouses
import pytest

import unittest

# from api.models.warehouses import Warehouses
import sys
import os
import pytest
import requests
import json


# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder
@pytest.fixture(scope="session", autouse=True)
def backup_and_restore_data():
    # saves the warehouse db in BackupJson
    # and writes it back after the pytest is done
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../../data", "warehouses.json")

    with open( json_file_path, 'r') as file:
        BackupJson = json.load(file)


    yield


    with open(json_file_path, 'w') as file:
        json.dump(BackupJson, file, indent=4)


class Test_Warehouses():

    warehousesObject = Warehouses("Test_Data/test_")

   
    ########## Test Endpoint ##########

    # server must be running when testing endpoints

    def test_warehouses_post_endpoint_success(self):

        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newWarehouseJson = {
            "id": 9000,
            "code": "ABCDEFGHIJKLM",
            "name": "TestName",
            "address": "TestAddress",
            "zip": "TestZip",
            "city": "TestCity",
            "province": "TestProvince",
            "country": "TestCountry",
            "contact":
            {
                "name": "TestContactName",
                    "phone": "TestPhoneNumber",
                    "email": "TestEmail"
            },
                "created_at":
                "1983-04-13 04:59:55",
                "updated_at":
                "2007-02-08 20:11:00"
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/warehouses/", headers=headers, json=newWarehouseJson)
        assert response.status_code == 201, f"Returns {response.status_code}, Should return 201 for successful creation"

        getResponse = requests.get(
            f"{BASE_URL}/api/v1/warehouses/9000", headers=headers)
        warehouseFromDB =  getResponse.json()
        assert warehouseFromDB["id"] == newWarehouseJson["id"] and \
            warehouseFromDB["code"] == newWarehouseJson["code"] and\
            warehouseFromDB["name"] == newWarehouseJson["name"] and\
            warehouseFromDB["address"] == newWarehouseJson["address"] and\
            warehouseFromDB["zip"] == newWarehouseJson["zip"] and\
            warehouseFromDB["province"] == newWarehouseJson["province"] and \
            warehouseFromDB["country"] == newWarehouseJson["country"] and \
            warehouseFromDB["contact"] == newWarehouseJson ["contact"], ""

    def test_warehouse_post_endpoint_missing_fields(self):
        # should return bad request
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        incompleteWarehouseJson = {
            "id": 9001,
            "name": "TestName",
            "address": "TestAddress",
            "zip": "TestZip",
            "city": "TestCity",
            "province": "TestProvince",
            "country": "TestCountry",
            "contact": {
                "name": "TestContactName",
                "phone": "TestPhoneNumber",
                "email": "TestEmail"
            },
            "created_at": "1983-04-13 04:59:55",
            "updated_at": "2007-02-08 20:11:00"
            
        }


        response = requests.post(
            f"{BASE_URL}/api/v1/warehouses/", headers=headers, json=incompleteWarehouseJson)
        

        getResponse = requests.get(
            f"{BASE_URL}/api/v1/warehouses/9001", headers=headers)
        warehouseFromDB =  getResponse.json()
        assert response.status_code == 400, f"Returns {response.status_code}, Should return 400 Bad Request"
        assert warehouseFromDB == None, "Should return None because the client shouldn't be added to DB"
        # ?? returns 201 instead of 400 Bad Request 

    def test_warehouse_post_endpoint_duplicate(self):
        # test if new warehouse could be created that already exists

        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newWarehouseJson = {
            "id": 9000,
            "code": "ABCDEFGHIJKLM",
            "name": "TestName",
            "address": "TestAddress",
            "zip": "TestZip",
            "city": "TestCity",
            "province": "TestProvince",
            "country": "TestCountry",
            "contact":
            {
                "name": "TestContactName",
                    "phone": "TestPhoneNumber",
                    "email": "TestEmail"
            },
                "created_at":
                "1983-04-13 04:59:55",
                "updated_at":
                "2007-02-08 20:11:00"
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/warehouses/", headers=headers, json=newWarehouseJson)
        assert response.status_code == 409, f"Returns {response.status_code}, Should return 409 for Conflict (duplicate)"
        # ?? returns 201 instead of 409

    def test_warehouses_get_endpoint(self):
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
        expectedJson = {
            "id": 9000,
            "code": "ABCDEFGHIJKLM",
            "name": "TestName",
            "address": "TestAddress",
            "zip": "TestZip",
            "city": "TestCity",
            "province": "TestProvince",
            "country": "TestCountry",
            "contact":
            {
                "name": "TestContactName",
                    "phone": "TestPhoneNumber",
                    "email": "TestEmail"
            },
                "created_at":
                "1983-04-13 04:59:55",
                "updated_at":
                "2007-02-08 20:11:00"
        }
        response = requests.get(
            f"{BASE_URL}/api/v1/warehouses/9000", headers=headers)
        
        warehouseFromDB = response.json()
        
        assert warehouseFromDB["id"] == expectedJson["id"] and \
            warehouseFromDB["code"] == expectedJson["code"] and\
            warehouseFromDB["name"] == expectedJson["name"] and\
            warehouseFromDB["address"] == expectedJson["address"] and\
            warehouseFromDB["zip"] == expectedJson["zip"] and\
            warehouseFromDB["province"] == expectedJson["province"] and \
            warehouseFromDB["country"] == expectedJson["country"] and \
            warehouseFromDB["contact"] == expectedJson ["contact"], f"Client in DB doesn't match expected Client"
        assert response.status_code == 200, f"Returns {response.status_code}, should be 200"

    def test_warehouses_get_endpoint_non_existent(self):
        # test the get endpoint for an id that doesn't exist
        # should return 404
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{BASE_URL}/api/v1/warehouses/99999", headers=headers)
        assert response.status_code == 404, f"Returns {response.status_code}, should be 404 because warehouse doesn't exist"
        # ?? returns 200 instead of 404

    def test_warehouses_put_endpoint(self):

        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newUpdatedWarehouseJson = {
            "id": 9000,
            "code": "ABCDEFGHIJKLM2",  # <- changed
            "name": "TestName2",
            "address": "TestAddress2",
            "zip": "TestZip2",
            "city": "TestCity2",
            "province": "TestProvince2",
            "country": "TestCountry2",
            "contact":
            {
                "name": "TestContactName2",
                    "phone": "TestPhoneNumber2",
                    "email": "TestEmail2"
            },
                "created_at":
                "1983-04-13 04:59:55",
                "updated_at":
                "2007-02-08 20:11:00"
        }

        response = requests.put(
            f"{BASE_URL}/api/v1/warehouses/9000", headers=headers, json=newUpdatedWarehouseJson)
        
        getResponse = requests.get(
            f"{BASE_URL}/api/v1/warehouses/9000", headers=headers)
        warehouseFromDB =  getResponse.json()
        assert response.status_code == 200, f"Returns {response.status_code}, Should be 200 for successful update"
        assert warehouseFromDB["id"] == newUpdatedWarehouseJson["id"] and \
            warehouseFromDB["code"] == newUpdatedWarehouseJson["code"] and\
            warehouseFromDB["name"] == newUpdatedWarehouseJson["name"] and\
            warehouseFromDB["address"] == newUpdatedWarehouseJson["address"] and\
            warehouseFromDB["zip"] == newUpdatedWarehouseJson["zip"] and\
            warehouseFromDB["province"] == newUpdatedWarehouseJson["province"] and \
            warehouseFromDB["country"] == newUpdatedWarehouseJson["country"] and \
            warehouseFromDB["contact"] == newUpdatedWarehouseJson ["contact"], "updated Client in DB doesn't match the updated json"

    def test_warehouses_put_endpoint_non_existent(self):
        # testing update warehouse that doesn't exist
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newUpdatedWarehouseJson = {
            "id": 99999,
            "code": "XXXXXXX",  # <- changed
            "name": "TestName2",
            "address": "TestAddress2",
            "zip": "TestZip2",
            "city": "TestCity2",
            "province": "TestProvince2",
            "country": "TestCountry2",
            "contact":
            {
                "name": "TestContactName2",
                    "phone": "TestPhoneNumber2",
                    "email": "TestEmail2"
            },
                "created_at":
                "1983-04-13 04:59:55",
                "updated_at":
                "2007-02-08 20:11:00"
        }

        response = requests.put(
            f"{BASE_URL}/api/v1/warehouses/9000", headers=headers, json=newUpdatedWarehouseJson)
        assert response.status_code == 404, f"Returns {response.status_code}, Should return 404 because client doesn't exist"
        # ?? returns 200 instead of 404

    def test_warehouses_delete_endpoint(self):
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
        response = requests.delete(
            f"{BASE_URL}/api/v1/warehouses/9000", headers=headers)
        assert response.status_code == 200, "Returns {response.status_code}, Should be 200 for successful deletion"
        assert self.warehousesObject.get_warehouse(9000) == None, "Client shouldn't exist in the DB"

    def test_warehouses_delete_endpoint_non_existent(self):
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
        response = requests.delete(
            f"{BASE_URL}/api/v1/warehouses/9002", headers=headers)
        assert response.status_code == 404, f"Returns {response.status_code}, Should return 404 because client doesn't exist"
        # ?? returns 200 instead of 404

    ########## Test Warehouses Methods ##########

    def test_get_warehouses(self):

        warehousesInJson = self.warehousesObject.get_warehouses()
        assert warehousesInJson == [
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
            }
        ], "The warehouse in json doesn't match the expected dictionary"

    def test_get_warehouse_with_id(self):
        warehouseWithId2 = self.warehousesObject.get_warehouse(2)
        assert warehouseWithId2 == {
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
        }, "The warehouse with id 2 doesn't match the dictionary"

    def test_add_warehouse(self):
        newWarehouse = {
            "id": 3,
            "code": "VCKINLLK",
            "name": "Naaldwijk distribution hub",
            "address": "Izesteeg 807",
            "zip": "1636 KI", "city": "Naaldwijk",
            "province": "Utrecht",
            "country": "NL",
            "contact":
                {"name": "Frederique van Wallaert",
                 "phone": "(009) 4870289", "email":
                 "jelle66@example.net"
                 },
            "created_at": "2001-05-11 10:43:52",
            "updated_at": "2017-12-19 14:32:38"
        }
        self.warehousesObject.add_warehouse(newWarehouse)
        warehouseFromDB = self.warehousesObject.get_warehouse(3)
        assert warehouseFromDB["id"] == newWarehouse["id"] and \
            warehouseFromDB["code"] == newWarehouse["code"] and\
            warehouseFromDB["name"] == newWarehouse["name"] and\
            warehouseFromDB["address"] == newWarehouse["address"] and\
            warehouseFromDB["zip"] == newWarehouse["zip"] and\
            warehouseFromDB["province"] == newWarehouse["province"] and \
            warehouseFromDB["country"] == newWarehouse["country"] and \
            warehouseFromDB["contact"] == newWarehouse["contact"], \
            "The json doesn't match the created newWarehouse dictionary , or get_warehouse doesn't function properly"

    def test_update_warehouse(self):

        newUpdatedWarehouse = {
            "id": 3,
            "code": "ABCDEFG",
            "name": "Rotterdam distribution hub",
            "address": "Izesteeg 807",
            "zip": "1636 KI", "city": "Rotterdam",
            "province": "Zuid-Holland",
            "country": "NL",
            "contact":
                {"name": "Fred van Wallaert",
                 "phone": "(009) 123456789",
                 "email": "jelle77@example.net"
                 },
            "created_at": "2001-05-11 10:43:52",
            "updated_at": "2017-12-19 14:32:38"
        }

        self.warehousesObject.update_warehouse(3, newUpdatedWarehouse)
        warehouseFromDB = self.warehousesObject.get_warehouse(3)
        assert warehouseFromDB["id"] == newUpdatedWarehouse["id"] and \
            warehouseFromDB["code"] == newUpdatedWarehouse["code"] and\
            warehouseFromDB["name"] == newUpdatedWarehouse["name"] and\
            warehouseFromDB["address"] == newUpdatedWarehouse["address"] and\
            warehouseFromDB["zip"] == newUpdatedWarehouse["zip"] and\
            warehouseFromDB["province"] == newUpdatedWarehouse["province"] and \
            warehouseFromDB["country"] == newUpdatedWarehouse["country"] and \
            warehouseFromDB["contact"] == newUpdatedWarehouse["contact"], \
            "The JSON response doesn't match the updated newUpdatedWarehouse dictionary, or get_warehouse doesn't function properly."

    def test_remove_warehouse(self):

        self.warehousesObject.remove_warehouse(3)
        assert self.warehousesObject.get_warehouse(3) == None, \
            "Warehouse with ID 3 still exists in the database, or get_warehouse doesn't function properly."
