
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

from models.warehouses import Warehouses
BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


class Test_Warehouses():

    warehousesObject = Warehouses("Test_Data/test_")
    headers_full = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
    
    newWarehouse = {
        "id": 0,
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

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/warehouses/", headers=self.headers_full, json=self.newWarehouse)
        new_timestamp = self.warehousesObject.get_timestamp()
        self.newWarehouse["created_at"] = new_timestamp.split('T')[0]
        self.newWarehouse["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):
        
        self.newWarehouse["code"] = "Y4ZYNL57"
        self.newWarehouse["city"] = "Rotterdam"
        self.newWarehouse["contact"]["phone"] = "(079) 0318253"

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full, json=self.newWarehouse)
        self.newWarehouse["updated_at"] = self.warehousesObject.get_timestamp().split('T')[0]
        assert responsePut.status_code == 200
   
    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newWarehouse

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restrictions(self):

        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(f"{BASE_URL}/api/v1/warehouses/", headers=headers_restricted, json=self.newWarehouse)
        responsePut_restricted = requests.put(f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=headers_restricted, json=self.newWarehouse)
        responseDelete_restricted = requests.delete(f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(f"{BASE_URL}/api/v1/warehouses/{self.newWarehouse['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403        
        assert responsePut_restricted.status_code == 403        
        assert responseDelete_restricted.status_code == 403       
        assert responseGet_restricted.status_code == 200

    # Warehouse Method Testing

    def test_get_warehouses(self):

        allWarehouses = self.warehousesObject.get_warehouses()
        assert allWarehouses == [{
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

        self.warehousesObject.get_warehouse(4)
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
        assert self.warehousesObject.get_warehouse(4) == None, \
            "Warehouse with ID 4 wasn't removed correctly, or get_warehouse doesn't function properly."
