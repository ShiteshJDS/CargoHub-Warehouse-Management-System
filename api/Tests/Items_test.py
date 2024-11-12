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

from models.items import Items

BASE_URL = "http://localhost:3000"


class Test_Items():

    itemsObject = Items("Test_Data/test_")
    headers_full = {
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
    }

    def test_get_items(self):
        items = self.itemsObject.get_items()
        assert len(items) == 4
        assert items[0]["uid"] == "P000001", "UID is not correct"
        assert items[0] == {
        "uid": "P000001",
        "code": "sjQ23408K",
        "description": "Face-to-face clear-thinking complexity",
        "short_description": "must",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
        "created_at": "2015-02-19 16:08:24",
        "updated_at": "2015-09-26 06:37:56"
    }, "Item is not correct"


    def test_get_item(self):
        item = self.itemsObject.get_item("P000002")
        assert item is not None
        assert item["code"] == "nyg48736S"
        assert item == {
        "uid": "P000002",
        "code": "nyg48736S",
        "description": "Focused transitional alliance",
        "short_description": "may",
        "upc_code": "9733132830047",
        "model_number": "ck-109684-VFb",
        "commodity_code": "y-20588-owy",
        "item_line": 69,
        "item_group": 85,
        "item_type": 39,
        "unit_purchase_quantity": 10,
        "unit_order_quantity": 15,
        "pack_order_quantity": 23,
        "supplier_id": 57,
        "supplier_code": "SUP312",
        "supplier_part_number": "j-10730-ESk",
        "created_at": "2020-05-31 16:00:08",
        "updated_at": "2020-11-08 12:49:21"
    }
    
    def test_get_items_for_item_line(self):
        items = self.itemsObject.get_items_for_item_line(54)
        assert len(items) == 1
        assert items[0] == {
        "uid": "P000003",
        "code": "QVm03739H",
        "description": "Cloned actuating artificial intelligence",
        "short_description": "we",
        "upc_code": "3722576017240",
        "model_number": "aHx-68Q4",
        "commodity_code": "t-541-F0g",
        "item_line": 54,
        "item_group": 88,
        "item_type": 42,
        "unit_purchase_quantity": 30,
        "unit_order_quantity": 17,
        "pack_order_quantity": 11,
        "supplier_id": 2,
        "supplier_code": "SUP237",
        "supplier_part_number": "r-920-z2C",
        "created_at": "1994-06-02 06:38:40",
        "updated_at": "1999-10-13 01:10:32"
    }
