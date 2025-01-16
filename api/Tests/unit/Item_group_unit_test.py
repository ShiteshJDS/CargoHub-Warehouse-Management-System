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
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

from models.item_groups import ItemGroups  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

class Test_Item_groups_Functions():

    item_groupObject = ItemGroups("../Test_Data/Cargohub_Test.db")

    def test_get_item_groups(self):

        allItemGroups = self.item_groupObject.get_item_groups()
        assert allItemGroups == [
            {
                "id": 1,
                "name": "Furniture",
                "description": "",
                "created_at": "2019-09-22 15:51:07",
                "updated_at": "2022-05-18 13:49:28"
            },
            {
                "id": 2,
                "name": "Stationery",
                "description": "",
                "created_at": "1999-08-14 13:39:27",
                "updated_at": "2011-06-16 05:00:47"
            },
            {
                "id": 3,
                "name": "Clothing",
                "description": "",
                "created_at": "1975-12-14 06:58:09",
                "updated_at": "2011-12-04 21:16:55"
            }
        ], "The item_group database doesn't match the expected data"

    def test_get_item_group_with_id(self):
        item_group2 = self.item_groupObject.get_item_group(2)
        assert item_group2 == {
            "id": 2,
            "name": "Stationery",
            "description": "",
            "created_at": "1999-08-14 13:39:27",
            "updated_at": "2011-06-16 05:00:47"
        }, "The item_group with id 2 wasn't found in the item_group database"

    def test_add_item_group(self):
        new_item_group = {
            "id": 4,
            "name": "Home Decor",
            "description": "",
            "created_at": "-",
            "updated_at": "-"
        }
        self.item_groupObject.add_item_group(new_item_group)
        new_timestamp = self.item_groupObject.get_timestamp()
        new_item_group["created_at"] = new_timestamp
        new_item_group["updated_at"] = new_timestamp

        assert self.item_groupObject.get_item_group(4) == new_item_group, \
            "The new item_group wasn't saved correctly, or get_item_group doesn't function properly"

    def test_update_item_group(self):
        updated_item_group = {
            "id": 4,
            "name": "Toys",                 # <- Changed
            "description": "For kids",      # <- Changed
            "created_at": "-",
            "updated_at": "-"
        }

        self.item_groupObject.update_item_group(4, updated_item_group)
        new_timestamp = self.item_groupObject.get_timestamp()
        updated_item_group["updated_at"] = new_timestamp

        assert self.item_groupObject.get_item_group(4) == updated_item_group, \
            "The new item_group wasn't updated correctly, or get_item_group doesn't function properly."

    def test_remove_item_group(self):

        self.item_groupObject.remove_item_group(4)
        assert self.item_groupObject.get_item_group(4) == None, \
            "Item_group with ID 4 wasn't removed correctly, or get_item_group doesn't function properly."