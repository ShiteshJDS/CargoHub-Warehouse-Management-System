# from models.warehouses import Warehouses
import pytest

import unittest

# from api.models.warehouses import Warehouses
import sys
import os
import pytest
import requests
import logging


# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
os.path.join(os.path.dirname(__file__), '..')))
from models.warehouses import Warehouses
from main import StartWebAPI


BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

class Test_Warehouses():

    warehousesObject = Warehouses("Test_Data/test_")


    ########## Test Endpoint ##########

    # server must be running when testing endpoints
    
    def test_correct_get_endpoint(self):
        # StartWebAPI()
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        response = requests.get(
            f"{BASE_URL}/api/v1/warehouses/1", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"id": 1,
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
                                   "created_at":
                                   "1983-04-13 04:59:55",
                                   "updated_at":
                                   "2007-02-08 20:11:00"
                                   }  # Replace with your expected response
        

    def test_post_endpoint(self):
        
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
        assert response.status_code == 201

        # delete the created warehouse

        deleteHeader = {
            "API_KEY": "a1b2c3d4e5"
        }
        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/warehouses/{newWarehouseJson['id']}", headers=deleteHeader)
        assert responseDelete.status_code == 200


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
        ], "The warehouse with ID 2 doesn't match the expected dictionary"

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
               warehouseFromDB["name"] ==  newWarehouse["name"] and\
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
               warehouseFromDB["name"] ==  newUpdatedWarehouse["name"] and\
               warehouseFromDB["address"] == newUpdatedWarehouse["address"] and\
               warehouseFromDB["zip"] == newUpdatedWarehouse["zip"] and\
               warehouseFromDB["province"] == newUpdatedWarehouse["province"] and \
               warehouseFromDB["country"] == newUpdatedWarehouse["country"] and \
               warehouseFromDB["contact"] == newUpdatedWarehouse["contact"] ,\
               "The JSON response doesn't match the updated newUpdatedWarehouse dictionary, or get_warehouse doesn't function properly."

    def test_remove_warehouse(self):

        self.warehousesObject.remove_warehouse(3)
        assert self.warehousesObject.get_warehouse(3) == None, \
        "Warehouse with ID 3 still exists in the database, or get_warehouse doesn't function properly."
