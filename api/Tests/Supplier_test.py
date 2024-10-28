
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

from models.suppliers import Suppliers
BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


class Test_Suppliers():

    suppliersObject = Suppliers("Test_Data/test_")
    headers_full = {
            "API_KEY": "a1b2c3d4e5",
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
        self.newSupplier["updated_at"] = self.suppliersObject.get_timestamp().split('T')[0]
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

        responsePost_restricted = requests.post(f"{BASE_URL}/api/v1/suppliers/", headers=headers_restricted, json=self.newSupplier)
        responsePut_restricted = requests.put(f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=headers_restricted, json=self.newSupplier)
        responseDelete_restricted = requests.delete(f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(f"{BASE_URL}/api/v1/suppliers/{self.newSupplier['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403        
        assert responsePut_restricted.status_code == 403        
        assert responseDelete_restricted.status_code == 403       
        assert responseGet_restricted.status_code == 200

    # Supplier Method Testing

    def test_get_suppliers(self):

        allSuppliers = self.suppliersObject.get_suppliers()
        assert allSuppliers == [
            {
        "id": 1,
        "code": "SUP0001",
        "name": "Lee, Parks and Johnson",
        "address": "5989 Sullivan Drives",
        "address_extra": "Apt. 996",
        "city": "Port Anitaburgh",
        "zip_code": "91688",
        "province": "Illinois",
        "country": "Czech Republic",
        "contact_name": "Toni Barnett",
        "phonenumber": "363.541.7282x36825",
        "reference": "LPaJ-SUP0001",
        "created_at": "1971-10-20 18:06:17",
        "updated_at": "1985-06-08 00:13:46"
    },
    {
        "id": 2,
        "code": "SUP0002",
        "name": "Holden-Quinn",
        "address": "576 Christopher Roads",
        "address_extra": "Suite 072",
        "city": "Amberbury",
        "zip_code": "16105",
        "province": "Illinois",
        "country": "Saint Martin",
        "contact_name": "Kathleen Vincent",
        "phonenumber": "001-733-291-8848x3542",
        "reference": "H-SUP0002",
        "created_at": "1995-12-18 03:05:46",
        "updated_at": "2019-11-10 22:11:12"
    },
    {
        "id": 3,
        "code": "SUP0003",
        "name": "White and Sons",
        "address": "1761 Shepard Valley",
        "address_extra": "Suite 853",
        "city": "Aguilarton",
        "zip_code": "63918",
        "province": "Wyoming",
        "country": "Ghana",
        "contact_name": "Jason Hudson",
        "phonenumber": "001-910-585-6962x8307",
        "reference": "WaS-SUP0003",
        "created_at": "2010-06-14 02:32:58",
        "updated_at": "2019-06-16 19:29:49"
    }
    ], "The supplier database doesn't match the expected data"

    def test_get_supplier_with_id(self):
        supplier2 = self.suppliersObject.get_supplier(2)
        assert supplier2 == {
            "id": 2,
            "code": "SUP0002",
            "name": "Holden-Quinn",
            "address": "576 Christopher Roads",
            "address_extra": "Suite 072",
            "city": "Amberbury",
            "zip_code": "16105",
            "province": "Illinois",
            "country": "Saint Martin",
            "contact_name": "Kathleen Vincent",
            "phonenumber": "001-733-291-8848x3542",
            "reference": "H-SUP0002",
            "created_at": "1995-12-18 03:05:46",
            "updated_at": "2019-11-10 22:11:12"
        }, "The supplier with id 2 wasn't found in the supplier database"

    def test_add_supplier(self):
        new_supplier = {
            "id": 4,
            "code": "SUP0004",
            "name": "Byrd PLC",
            "address": "73232 Sanchez Garden Apt. 490",
            "address_extra": "Apt. 159",
            "city": "Jacobbury",
            "zip_code": "48760",
            "province": "Michigan",
            "country": "Palestinian Territory",
            "contact_name": "Ashley Campbell",
            "phonenumber": "+1-590-938-6960",
            "reference": "BP-SUP0482",
            "created_at": "-",
            "updated_at": "-"
        }
        self.suppliersObject.add_supplier(new_supplier)
        new_timestamp = self.suppliersObject.get_timestamp()
        new_supplier["created_at"] = new_timestamp
        new_supplier["updated_at"] = new_timestamp

        self.suppliersObject.get_supplier(4)
        assert self.suppliersObject.get_supplier(4) == new_supplier, \
            "The new supplier wasn't saved correctly, or get_supplier doesn't function properly"

    def test_update_supplier(self):

        updated_supplier = {
            "id": 4,
            "code": "SUP0004",
            "name": "Byrd PLC",
            "address": "73232 Sanchez Garden Apt. 490",
            "address_extra": "Apt. 159",
            "city": "Rotterdam",                      # <- Changed
            "zip_code": "48760",
            "province": "Zuid-Holland",                      # <- Changed
            "country": "Netherlands",                      # <- Changed
            "contact_name": "Ashley Campbell",
            "phonenumber": "+1-590-938-6960",
            "reference": "BP-SUP0482",
            "created_at": "1982-04-04 12:06:17",
            "updated_at": "-"
        }

        self.suppliersObject.update_supplier(4, updated_supplier)
        new_timestamp = self.suppliersObject.get_timestamp()
        updated_supplier["updated_at"] = new_timestamp

        assert self.suppliersObject.get_supplier(4) == updated_supplier, \
            "The database wasn't updated correctly, or get_supplier doesn't function properly."

    def test_remove_supplier(self):

        self.suppliersObject.remove_supplier(4)
        assert self.suppliersObject.get_supplier(4) == None, \
            "Supplier with ID 4 wasn't removed correctly, or get_supplier doesn't function properly"
