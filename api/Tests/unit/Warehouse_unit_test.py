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
sys.path.insert(0, os.path.abspath(
os.path.join(os.path.dirname(__file__), '..', '..')))
from models.warehouses import Warehouses  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

class Test_Warehouses_Functions():

    warehousesObject = Warehouses("../Test_Data/cargohub_test.db")
    
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
            "id": 100,
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
        warehouseFromDB = self.warehousesObject.get_warehouse(100)
        
        new_warehouse.pop("created_at", None)
        new_warehouse.pop("updated_at", None)

        warehouseFromDB.pop("created_at", None)
        warehouseFromDB.pop("updated_at", None)

        assert new_warehouse == warehouseFromDB, "The new warehouse wasn't saved correctly or get_warehouse doesn't function properly"

    def test_update_warehouse(self):
        updatedWarehouse = {
            "id": 100,
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

        self.warehousesObject.update_warehouse(100, updatedWarehouse)
        updatedWarehouseFromDB = self.warehousesObject.get_warehouse(100)
        
        updatedWarehouse.pop("created_at", None)
        updatedWarehouse.pop("updated_at", None)

        updatedWarehouseFromDB.pop("created_at", None)
        updatedWarehouseFromDB.pop("updated_at", None)


        assert updatedWarehouse == updatedWarehouseFromDB, \
            "The new warehouse wasn't updated correctly, or get_warehouse doesn't function properly."
        # assert updated_warehouse == updatedWarehouseFromDB, \
        #     "The new warehouse wasn't updated correctly, or get_warehouse doesn't function properly."

    def test_remove_warehouse(self):
        assert self.warehousesObject.get_warehouse(100) is not None, \
        "warehouse wasnt added correctly, add_warehouse doesn't function properly."

        self.warehousesObject.remove_warehouse(100)
        assert self.warehousesObject.get_warehouse(100) is None, \
            "Warehouse with ID 4 wasn't removed correctly, or get_warehouse doesn't function properly."