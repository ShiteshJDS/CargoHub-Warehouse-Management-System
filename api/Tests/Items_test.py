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


