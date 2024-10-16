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

from api.models.warehouses import Warehouses

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL


class Test_Warehouses():

    warehousesObject = Warehouses("./Tests/Test_Data/test_")

    def test_correct_get_endpoint(self):
        
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
        ]

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
        }
