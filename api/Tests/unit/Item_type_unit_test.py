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

from models.item_types import ItemTypes  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

class Test_Item_Types_Functions():

    item_typeObject = ItemTypes("../Test_Data/Cargohub_Test.db")

    # def test_get_item_types(self):

    #     allItemTypes = self.item_typeObject.get_item_types()
    #     assert allItemTypes == [
    #         {
    #             "id": 1,
    #             "name": "Desktop",
    #             "description": "",
    #             "created_at": "1993-07-28 13:43:32",
    #             "updated_at": "2022-05-12 08:54:35"
    #         },
    #         {
    #             "id": 2,
    #             "name": "Tablet",
    #             "description": "",
    #             "created_at": "1977-05-01 00:05:04",
    #             "updated_at": "2001-04-14 02:41:59"
    #         },
    #         {
    #             "id": 3,
    #             "name": "Smartphone",
    #             "description": "",
    #             "created_at": "2014-08-23 03:26:57",
    #             "updated_at": "2017-09-20 11:51:15"
    #         }
    #     ], "The item_type database doesn't match the expected data"

    def test_get_item_type_with_id(self):
        item_type2 = self.item_typeObject.get_item_type(2)
        assert item_type2 == {
            "id": 2,
            "name": "Tablet",
            "description": "",
            "created_at": "1977-05-01 00:05:04",
            "updated_at": "2001-04-14 02:41:59"
        }, "The item_type with id 2 wasn't found in the item_type database"

    def test_add_item_type(self):
        new_item_type = {
            "id": 4,
            "name": "Home Decor",
            "description": "",
            "created_at": "-",
            "updated_at": "-"
        }
        self.item_typeObject.add_item_type(new_item_type)
        new_timestamp = self.item_typeObject.get_timestamp()
        new_item_type["created_at"] = new_timestamp
        new_item_type["updated_at"] = new_timestamp

        assert self.item_typeObject.get_item_type(4) == new_item_type, \
            "The new item_type wasn't saved correctly, or get_item_type doesn't function properly"

    def test_update_item_type(self):
        updated_item_type = {
            "id": 4,
            "name": "Toys",                 # <- Changed
            "description": "For kids",      # <- Changed
            "created_at": "-",
            "updated_at": "-"
        }

        self.item_typeObject.update_item_type(4, updated_item_type)
        new_timestamp = self.item_typeObject.get_timestamp()
        updated_item_type["updated_at"] = new_timestamp

        assert self.item_typeObject.get_item_type(4) == updated_item_type, \
            "The new item_type wasn't updated correctly, or get_item_type doesn't function properly."

    def test_remove_item_type(self):

        self.item_typeObject.remove_item_type(4)
        assert self.item_typeObject.get_item_type(4) == None, \
            "Item_type with ID 4 wasn't removed correctly, or get_item_type doesn't function properly."