
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

from models.suppliers import Suppliers  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

class Test_Suppliers():

    suppliersObject = Suppliers("../Test_Data/Cargohub_Test.db")
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    newSupplier = {
        "id": 0,
        "code": "SUP0001",
        "name": "Lee, Parks and Johnson",
        "address": "5989 Sullivan Drives",
        "address_extra": "Apt. 996",
        "city": "Rotterdam",
        "zip_code": "91688",
        "province": "Zuid-Holland",
        "country": "Netherlands",
        "contact_name": "Toni Barnett",
        "phonenumber": "363.541.7282x36825",
        "reference": "LPaJ-SUP0001",
        "created_at": "-",
        "updated_at": "-"
    }

    # Supplier Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/suppliers/", headers=self.headers_full, json=self.newSupplier)
        new_timestamp = self.suppliersObject.get_timestamp()
        self.newSupplier["created_at"] = new_timestamp.split('T')[0]
        self.newSupplier["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newSupplier["code"] = "SUP0002"
        self.newSupplier["city"] = "Amsterdam"
        self.newSupplier["contact_name"] = "Kevin Krul"

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=self.headers_full, json=self.newSupplier)
        self.newSupplier["updated_at"] = self.suppliersObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newSupplier

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restrictions(self):

        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/suppliers/", headers=headers_restricted, json=self.newSupplier)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=headers_restricted, json=self.newSupplier)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200

