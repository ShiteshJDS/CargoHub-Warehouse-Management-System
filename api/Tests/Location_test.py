
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
    os.path.join(os.path.dirname(__file__), '..')))

from models.locations import Locations  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

@pytest.fixture(scope="module", autouse=True)
def manage_warehouse_json_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../../data/locations.json")
    backup_file_path = f"{json_file_path}.backup"

    # Backup the JSON file
    shutil.copyfile(json_file_path, backup_file_path)

    yield  # Run the tests

    # Restore the JSON file from backup
    shutil.copyfile(backup_file_path, json_file_path)
    os.remove(backup_file_path)  # Clean up the backup file

class Test_Locations():

    locationObject = Locations("Test_Data/Cargohub_Test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newLocation = {
        "id": 0,
        "warehouse_id": 1,
        "code": "C.15.0",
        "name": "Row: C, Rack: 15, Shelf: 0",
        "created_at": "-",
        "updated_at": "-"
    }

    # Location Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/locations/", headers=self.headers_full, json=self.newLocation)
        new_timestamp = self.locationObject.get_timestamp()
        self.newLocation["created_at"] = new_timestamp.split('T')[0]
        self.newLocation["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newLocation["warehouse_id"] = 4
        self.newLocation["code"] = "C.15.1"
        self.newLocation["name"] = "Row: C, Rack: 15, Shelf: 1"

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/locations/{self.newLocation['id']}", headers=self.headers_full, json=self.newLocation)
        self.newLocation["updated_at"] = self.locationObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/locations/{self.newLocation['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newLocation

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/locations/{self.newLocation['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restrictions(self):

        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/locations/", headers=headers_restricted, json=self.newLocation)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/locations/{self.newLocation['id']}", headers=headers_restricted, json=self.newLocation)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/locations/{self.newLocation['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/locations/{self.newLocation['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200

    # Location Method Testing

    def test_get_locations(self):

        allLocations = self.locationObject.get_locations()
        assert allLocations == [
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
            },
            {
                "id": 3,
                "warehouse_id": 2,
                "code": "A.2.0",
                "name": "Row: A, Rack: 2, Shelf: 0",
                "created_at": "1992-05-15 03:21:32",
                "updated_at": "1992-05-15 03:21:32"
            }
        ], "The location database doesn't match the expected data"

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
        all_warehouse1_locations = self.locationObject.get_locations_in_warehouse(
            1)
        assert all_warehouse1_locations == [
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
        ], "The locations inside warehouse 1 don't match the expected data"

    def test_add_location(self):
        new_location = {
            "id": 4,
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

        assert self.locationObject.get_location(4) == new_location, \
            "The new location wasn't saved correctly, or get_location doesn't function properly"

    def test_update_location(self):
        updated_location = {
            "id": 4,
            "warehouse_id": 2,                      # <- Changed
            "code": "A.12.2",                       # <- Changed
            "name": "Row: A, Rack: 12, Shelf: 2",   # <- Changed
            "created_at": "1992-05-15 03:21:32",
            "updated_at": "-"
        }

        self.locationObject.update_location(4, updated_location)
        new_timestamp = self.locationObject.get_timestamp()
        updated_location["updated_at"] = new_timestamp

        assert self.locationObject.get_location(4) == updated_location, \
            "The new location wasn't updated correctly, or get_location doesn't function properly."

    def test_remove_location(self):

        self.locationObject.remove_location(4)
        assert self.locationObject.get_location(4) == None, \
            "Location with ID 4 wasn't removed correctly, or get_location doesn't function properly."
