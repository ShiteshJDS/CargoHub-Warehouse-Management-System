import pytest
import unittest
import sys
import os
import requests
import logging
import shutil
from dotenv import load_dotenv

load_dotenv()

# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

from models.items import Items

BASE_URL = "http://localhost:3000"

class Test_Items():

    itemsObject = Items("../Test_Data/Cargohub_Test.db")

    # Test methods for Items

    # def test_get_items(self):
    #     items = self.itemsObject.get_items()
    #     assert len(items) == 4
    #     assert items[0]["uid"] == "P000001", "UID is not correct"
    #     assert items[0] == {
    #     "uid": "P000001",
    #     "code": "sjQ23408K",
    #     "description": "Face-to-face clear-thinking complexity",
    #     "short_description": "must",
    #     "upc_code": "6523540947122",
    #     "model_number": "63-OFFTq0T",
    #     "commodity_code": "oTo304",
    #     "item_line": 11,
    #     "item_group": 73,
    #     "item_type": 14,
    #     "unit_purchase_quantity": 47,
    #     "unit_order_quantity": 13,
    #     "pack_order_quantity": 11,
    #     "supplier_id": 34,
    #     "supplier_code": "SUP423",
    #     "supplier_part_number": "E-86805-uTM",
    #     "created_at": "2015-02-19 16:08:24",
    #     "updated_at": "2015-09-26 06:37:56"
    # }, "Item is not correct"


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
        testing_items_lines = [
  {
    "uid": "P000003",
    "code": "QVm03739H",
    "description": "Cloned actuating artificial intelligence",
    "short_description": "we",
    "upc_code": "3722576017240",
    "model_number": "aHx-68Q4",
    "commodity_code": "t-541-F0g",
    "item_line_id": 54,
    "item_group_id": 88,
    "item_type_id": 42,
    "unit_purchase_quantity": 30,
    "unit_order_quantity": 17,
    "pack_order_quantity": 11,
    "supplier_id": 2,
    "supplier_code": "SUP237",
    "supplier_part_number": "r-920-z2C",
    "created_at": "1994-06-02 06:38:40",
    "updated_at": "1999-10-13 01:10:32"
  },
  {
    "uid": "P000119",
    "code": "ttu69299d",
    "description": "Synergized encompassing software",
    "short_description": "reduce",
    "upc_code": "8206426218773",
    "model_number": "UqG716",
    "commodity_code": "GOg-40v6",
    "item_line_id": 54,
    "item_group_id": 17,
    "item_type_id": 24,
    "unit_purchase_quantity": 42,
    "unit_order_quantity": 11,
    "pack_order_quantity": 14,
    "supplier_id": 39,
    "supplier_code": "SUP578",
    "supplier_part_number": "60-KPGwB2o",
    "created_at": "1989-06-17 03:30:54",
    "updated_at": "2000-08-01 16:22:51"
  }]
        assert all(item in items for item in testing_items_lines)

    def test_get_items_for_item_group(self):
        items = self.itemsObject.get_items_for_item_group(85)
        testing_item_groups = [
  {
    "uid": "P000002",
    "code": "nyg48736S",
    "description": "Focused transitional alliance",
    "short_description": "may",
    "upc_code": "9733132830047",
    "model_number": "ck-109684-VFb",
    "commodity_code": "y-20588-owy",
    "item_line_id": 69,
    "item_group_id": 85,
    "item_type_id": 39,
    "unit_purchase_quantity": 10,
    "unit_order_quantity": 15,
    "pack_order_quantity": 23,
    "supplier_id": 57,
    "supplier_code": "SUP312",
    "supplier_part_number": "j-10730-ESk",
    "created_at": "2020-05-31 16:00:08",
    "updated_at": "2020-11-08 12:49:21"
  },
  {
    "uid": "P000010",
    "code": "gVK34692I",
    "description": "Synchronized 24hour Graphical User Interface",
    "short_description": "science",
    "upc_code": "8196931578335",
    "model_number": "zM-482907-nIu",
    "commodity_code": "p-69292-Xkv",
    "item_line_id": 47,
    "item_group_id": 85,
    "item_type_id": 75,
    "unit_purchase_quantity": 22,
    "unit_order_quantity": 6,
    "pack_order_quantity": 21,
    "supplier_id": 11,
    "supplier_code": "SUP641",
    "supplier_part_number": "lAE447",
    "created_at": "2022-08-05 02:46:34",
    "updated_at": "2023-09-07 04:10:46"
  }]
        assert all(item in items for item in testing_item_groups)

    def test_get_items_for_item_type(self):
        items = self.itemsObject.get_items_for_item_type(40)
        testing_item_types = [
  {
    "uid": "P000004",
    "code": "zdN19039A",
    "description": "Pre-emptive asynchronous throughput",
    "short_description": "take",
    "upc_code": "9668154959486",
    "model_number": "pZ-7816",
    "commodity_code": "IFq-47R1",
    "item_line_id": 58,
    "item_group_id": 23,
    "item_type_id": 40,
    "unit_purchase_quantity": 21,
    "unit_order_quantity": 20,
    "pack_order_quantity": 20,
    "supplier_id": 34,
    "supplier_code": "SUP140",
    "supplier_part_number": "T-210-I4M",
    "created_at": "2005-08-23 00:48:17",
    "updated_at": "2017-04-29 15:25:25"
  },
  {
    "uid": "P000041",
    "code": "MZn96040u",
    "description": "Pre-emptive bandwidth-monitored Local Area Network",
    "short_description": "bit",
    "upc_code": "2133803706676",
    "model_number": "puF-39S0",
    "commodity_code": "Kt-823309-sAa",
    "item_line_id": 83,
    "item_group_id": 50,
    "item_type_id": 40,
    "unit_purchase_quantity": 3,
    "unit_order_quantity": 7,
    "pack_order_quantity": 11,
    "supplier_id": 20,
    "supplier_code": "SUP813",
    "supplier_part_number": "Ss-1109",
    "created_at": "2020-05-19 01:44:53",
    "updated_at": "2020-06-19 20:23:58"
  }]
        assert all(item in items for item in testing_item_types)
        
    def test_get_items_for_supplier(self):
        items = self.itemsObject.get_items_for_supplier(34)
        testing_suppliers = [
  {
    "uid": "P000001",
    "code": "sjQ23408K",
    "description": "Face-to-face clear-thinking complexity",
    "short_description": "must",
    "upc_code": "6523540947122",
    "model_number": "63-OFFTq0T",
    "commodity_code": "oTo304",
    "item_line_id": 11,
    "item_group_id": 73,
    "item_type_id": 14,
    "unit_purchase_quantity": 47,
    "unit_order_quantity": 13,
    "pack_order_quantity": 11,
    "supplier_id": 34,
    "supplier_code": "SUP423",
    "supplier_part_number": "E-86805-uTM",
    "created_at": "2015-02-19 16:08:24",
    "updated_at": "2015-09-26 06:37:56"
  },
  {
    "uid": "P000004",
    "code": "zdN19039A",
    "description": "Pre-emptive asynchronous throughput",
    "short_description": "take",
    "upc_code": "9668154959486",
    "model_number": "pZ-7816",
    "commodity_code": "IFq-47R1",
    "item_line_id": 58,
    "item_group_id": 23,
    "item_type_id": 40,
    "unit_purchase_quantity": 21,
    "unit_order_quantity": 20,
    "pack_order_quantity": 20,
    "supplier_id": 34,
    "supplier_code": "SUP140",
    "supplier_part_number": "T-210-I4M",
    "created_at": "2005-08-23 00:48:17",
    "updated_at": "2017-04-29 15:25:25"
  }]
        assert all(item in items for item in testing_suppliers)


    def test_add_item(self):
        item = {
        "uid": "P111721",
        "code": "zdN19039A",
        "description": "Pre-emptive asynchronous throughput",
        "short_description": "take",
        "upc_code": "9668154959486",
        "model_number": "pZ-7816",
        "commodity_code": "IFq-47R1",
        "item_line": 58,
        "item_group": 23,
        "item_type": 40,
        "unit_purchase_quantity": 21,
        "unit_order_quantity": 20,
        "pack_order_quantity": 20,
        "supplier_id": 34,
        "supplier_code": "SUP140",
        "supplier_part_number": "T-210-I4M",
        "created_at": "-",
        "updated_at": "-"
    }
        self.itemsObject.add_item(item)
        items = self.itemsObject.get_items()
        assert len(items) == 11721
        assert items[11720] == item
    
    def test_update_item(self):
        item = {
        "uid": "P111721",
        "code": "zdN19039A",
        "description": "Pre-emptive asynchronous throughput",
        "short_description": "take",
        "upc_code": "9668154959486",
        "model_number": "pZ-7816",
        "commodity_code": "IFq-47R1",
        "item_line": 59,
        "item_group": 23,
        "item_type": 41,
        "unit_purchase_quantity": 21,
        "unit_order_quantity": 20,
        "pack_order_quantity": 20,
        "supplier_id": 34,
        "supplier_code": "SUP140",
        "supplier_part_number": "T-210-I4M",
        "created_at": "2005-08-23 00:48:17",
        "updated_at": "2017-04-29 15:25:25"
    }
        self.itemsObject.update_item("P111721", item)
        items = item = self.itemsObject.get_item("P111721")
        assert item == items
    
    def test_remove_item(self):
        item = self.itemsObject.get_item("P111721")
        assert item is not None, "Item with UID P111721 does not exist"

        self.itemsObject.remove_item("P111721")
        items = self.itemsObject.get_items()
        assert len(items) == 11720