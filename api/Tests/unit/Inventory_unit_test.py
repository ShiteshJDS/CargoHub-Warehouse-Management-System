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

from models.inventories import Inventories  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


class Test_Inventories():

    inventoryObject = Inventories("../Test_Data/Cargohub_Test.db")

    def test_get_inventory_with_id(self):
        inventory2 = self.inventoryObject.get_inventory(2)
        assert inventory2 == {
            "id": 2,
            "item_id": "P000002",
            "description": "Focused transitional alliance",
            "item_reference": "nyg48736S",
            "total_on_hand": 194,
            "total_expected": 0,
            "total_ordered": 139,
            "total_allocated": 0,
            "total_available": 55,
            "created_at": "2020-05-31 16:00:08",
            "updated_at": "2020-11-08 12:49:21",
            "locations": [
                19800,
                23653,
                3068,
                3334,
                20477,
                20524,
                17579,
                2271,
                2293,
                22717
            ]
        }, "The inventory with id 2 wasn't found in the inventory database"

    def test_get_inventories_for_item(self):
        all_inventories = self.inventoryObject.get_inventories_for_item(
            "P000002")
        print("Returned inventories:", all_inventories)
        expected_inventories = [
            {
                "id": 2,
                "item_id": "P000002",
                "description": "Focused transitional alliance",
                "item_reference": "nyg48736S",
                "total_on_hand": 194,
                "total_expected": 0,
                "total_ordered": 139,
                "total_allocated": 0,
                "total_available": 55,
                "created_at": "2020-05-31 16:00:08",
                "updated_at": "2020-11-08 12:49:21",
                "locations": [
                    19800,
                    23653,
                    3068,
                    3334,
                    20477,
                    20524,
                    17579,
                    2271,
                    2293,
                    22717
                ]
            }
        ]
        assert all(expected_inventory in all_inventories for expected_inventory in expected_inventories), \
            "The inventories for item 2 don't match the expected data"

    def test_get_locations_for_inventory(self):
        inventory_locations = self.inventoryObject.get_locations_for_inventory(
            2)
        expected_locations = [
            19800,
            23653,
            3068,
            3334,
            20477,
            20524,
            17579,
            2271,
            2293,
            22717
        ]
        assert inventory_locations == expected_locations, \
            "The locations for inventory 2 don't match the expected data"

    def test_get_inventory_totals_for_items(self):
        item_totals = self.inventoryObject.get_inventory_totals_for_item(
            "P000006")
        expected_item_totals = {
            "total_expected": 0,
            "total_ordered": 110,
            "total_allocated": 40,
            "total_available": 44
        }
        assert item_totals == expected_item_totals, \
            "The item totals for item 6 don't match the expected data"

    def test_add_inventory(self):
        new_inventory = {
            "id": 11721,
            "item_id": "P011721",
            "description": "new boring python",
            "item_reference": "rst32512T",
            "total_on_hand": 117,
            "total_expected": 0,
            "total_ordered": 139,
            "total_allocated": 0,
            "total_available": 50,
            "created_at": "-",
            "updated_at": "-",
            "locations": [
                10023,
                21533,
                308,
                334,
                2472,
                2054,
                1579,
                221,
                2233,
                2217
            ]
        }
        self.inventoryObject.add_inventory(new_inventory)
        new_timestamp = self.inventoryObject.get_timestamp()
        new_inventory["created_at"] = new_timestamp
        new_inventory["updated_at"] = new_timestamp

        saved_inventory = self.inventoryObject.get_inventory(11721)
        saved_inventory.pop("created_at", None)
        saved_inventory.pop("updated_at", None)
        new_inventory.pop("created_at", None)
        new_inventory.pop("updated_at", None)
        assert saved_inventory == new_inventory, \
            "The new inventory wasn't saved correctly, or get_inventory doesn't function properly"

    def test_update_inventory(self):
        updated_inventory = {
            "id": 11721,
            "item_id": "P011721",
            "description": "new placeholder python",     # <- Changed
            "item_reference": "rst32512T",
            "total_on_hand": 217,                        # <- Changed
            "total_expected": 0,
            "total_ordered": 139,
            "total_allocated": 0,
            "total_available": 51,                       # <- Changed
            "created_at": "-",
            "updated_at": "-",
            "locations": [
                10023,
                21533,
                310,                                     # <- Changed
                334,
                2472,
                2054,
                1571,                                    # <- Changed
                221,
                2231,                                    # <- Changed
                2217
            ]
        }

        self.inventoryObject.update_inventory(11721, updated_inventory)
        new_timestamp = self.inventoryObject.get_timestamp()
        updated_inventory["updated_at"] = new_timestamp

        saved_location = self.inventoryObject.get_inventory(11721)
        saved_location.pop("created_at", None)
        saved_location.pop("updated_at", None)
        updated_inventory.pop("created_at", None)
        updated_inventory.pop("updated_at", None)
        assert saved_location == updated_inventory, \
            "The new inventory wasn't updated correctly, or get_inventory doesn't function properly."

    def test_remove_inventory(self):
        # Assert that the Location exists before removal
        assert self.inventoryObject.get_inventory(11721) is not None, \
            "Inventory with ID 11721 does not exist before removal"

        self.inventoryObject.remove_inventory(11721)
        assert self.inventoryObject.get_inventory(11721) == None, \
            "Inventory with ID 11721 wasn't removed correctly, or get_inventory doesn't function properly."
