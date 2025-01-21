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

from models.locations import Locations  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

class Test_Locations():

    locationObject = Locations("../Test_Data/Cargohub_Test.db")

    # Location Method Testing

    # def test_get_locations(self):

    #     allLocations = self.locationObject.get_locations()
    #     assert allLocations == [
    #         {
    #             "id": 1,
    #             "warehouse_id": 1,
    #             "code": "A.1.0",
    #             "name": "Row: A, Rack: 1, Shelf: 0",
    #             "created_at": "1992-05-15 03:21:32",
    #             "updated_at": "1992-05-15 03:21:32"
    #         },
    #         {
    #             "id": 2,
    #             "warehouse_id": 1,
    #             "code": "A.1.1",
    #             "name": "Row: A, Rack: 1, Shelf: 1",
    #             "created_at": "1992-05-15 03:21:32",
    #             "updated_at": "1992-05-15 03:21:32"
    #         },
    #         {
    #             "id": 3,
    #             "warehouse_id": 2,
    #             "code": "A.2.0",
    #             "name": "Row: A, Rack: 2, Shelf: 0",
    #             "created_at": "1992-05-15 03:21:32",
    #             "updated_at": "1992-05-15 03:21:32"
    #         }
    #     ], "The location database doesn't match the expected data"

    def test_get_location_with_id(self):
        location2 = self.locationObject.get_location(2)
        assert location2 == {
            "id": 2,
            "warehouse_id": 1,
            "code": "A.1.1",
            "name": "Row: A, Rack: 1, Shelf: 1",
            "created_at": "1992-05-15 03:21:32",
            "updated_at": "1992-05-15 03:21:32"
        }, "The location with id 2 wasn't found in the location database"

    def test_get_locations_in_warehouse(self):
        all_warehouse1_locations = self.locationObject.get_locations_in_warehouse(1)
        expected_locations = [
            {
                "id": 1,
                "warehouse_id": 1,
                "code": "A.1.0",
                "name": "Row: A, Rack: 1, Shelf: 0",
                "created_at": "1992-05-15 03:21:32",
                "updated_at": "1992-05-15 03:21:32"
            },
            {
                "id": 2,
                "warehouse_id": 1,
                "code": "A.1.1",
                "name": "Row: A, Rack: 1, Shelf: 1",
                "created_at": "1992-05-15 03:21:32",
                "updated_at": "1992-05-15 03:21:32"
            }
        ]
        assert all(location in all_warehouse1_locations for location in expected_locations), \
            "The locations inside warehouse 1 don't match the expected data"

    def test_add_location(self):
        new_location = {
            "id": 34534,
            "warehouse_id": 1,
            "code": "A.12.1",
            "name": "Row: A, Rack: 12, Shelf: 1",
            "created_at": "-",
            "updated_at": "-"
        }
        self.locationObject.add_location(new_location)
        new_timestamp = self.locationObject.get_timestamp()
        new_location["created_at"] = new_timestamp
        new_location["updated_at"] = new_timestamp

        saved_location = self.locationObject.get_location(34534)
        saved_location.pop("created_at", None)
        saved_location.pop("updated_at", None)
        new_location.pop("created_at", None)
        new_location.pop("updated_at", None)
        assert saved_location == new_location, \
            "The new location wasn't saved correctly, or get_location doesn't function properly"

    def test_update_location(self):
        updated_location = {
            "id": 34534,
            "warehouse_id": 2,                      # <- Changed
            "code": "A.12.2",                       # <- Changed
            "name": "Row: A, Rack: 12, Shelf: 2",   # <- Changed
            "created_at": "1992-05-15 03:21:32",
            "updated_at": "-"
        }

        self.locationObject.update_location(34534, updated_location)
        new_timestamp = self.locationObject.get_timestamp()
        updated_location["updated_at"] = new_timestamp

        saved_location = self.locationObject.get_location(34534)
        saved_location.pop("created_at", None)
        saved_location.pop("updated_at", None)
        updated_location.pop("created_at", None)
        updated_location.pop("updated_at", None)
        assert saved_location == updated_location, \
            "The new location wasn't updated correctly, or get_location doesn't function properly."

    def test_remove_location(self):
        # Assert that the Location exists before removal
        assert self.locationObject.get_location(34534) is not None, \
            "Location with ID 34534 does not exist before removal"

        self.locationObject.remove_location(34534)
        assert self.locationObject.get_location(34534) == None, \
            "Location with ID 34534 wasn't removed correctly, or get_location doesn't function properly."
