import pytest

import unittest


import sys
import os
import pytest
import requests
import json


# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
os.path.join(os.path.dirname(__file__), '..')))
from models.clients import Clients



BASE_URL = "http://localhost:3000"  # Replace with your API's base URL


@pytest.fixture(scope="session", autouse=True)
def backup_and_restore_data():
    # saves the clients db in BackupJson
    # and writes it back after the pytest is done 
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../../data", "clients.json")

    with open( json_file_path, 'r') as file:
        BackupJson = json.load(file)

    yield

    with open(json_file_path, 'w') as file:
        json.dump(BackupJson, file, indent=4)

# Must run in test folder

class Test_Clients():

    ClientsObject = Clients("Test_Data/test_")


    ########## Test Endpoint ##########

    # server must be running when testing endpoints
    def test_clients_post_endpoint_success(self):

        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newClientJson = {
            "id": 100000,
            "name": "Test Name",
            "address": "Test Address",
            "city": "Test city",
            "zip_code": "Test zip_code",
            "province": "Test province",
            "country": "Test country",
            "contact_name": "Test contact_name",
            "contact_phone": "123456789",
            "contact_email": "email@email.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/clients/", headers=headers, json=newClientJson)
        assert response.status_code == 201, f"Returns {response.status_code}, Should return 201 for successful creation"

    def test_clients_post_endpoint_missing_fields(self):
        # should return bad request

        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        incompleteClientJson = {
            "id": 100001,
            "name": "Test Name",
            "country": "Test country",
            "contact_name": "Test contact_name",
            "contact_phone": "123456789",
            "contact_email": "email@email.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }


        response = requests.post(
            f"{BASE_URL}/api/v1/clients/", headers=headers, json=incompleteClientJson)
 
        getResponse = requests.get(
            f"{BASE_URL}/api/v1/clients/100001", headers=headers)
        clientFromDB =  getResponse.json()
        assert response.status_code == 400, f"Returns {response.status_code}, Should return 400 Bad Request"
        assert clientFromDB == None, "Should return None because the client shouldn't be added to DB"
        # ?? returns 201 instead of 400 Bad Request 

    def test_clients_post_endpoint_duplicate(self):
        # test if new warehouse could be created that already exists
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newClientJson = {
            "id": 100000,
            "name": "Test Name",
            "address": "Test Address",
            "city": "Test city",
            "zip_code": "Test zip_code",
            "province": "Test province",
            "country": "Test country",
            "contact_name": "Test contact_name",
            "contact_phone": "123456789",
            "contact_email": "email@email.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }

        response = requests.post(
            f"{BASE_URL}/api/v1/clients/", headers=headers, json=newClientJson)
        assert response.status_code == 409, f"Returns {response.status_code}, Should return 409 for Conflict (duplicate)"
        # ?? returns 201 instead of 409
        
    def test_clients_get_endpoint(self):
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
        expectedJson = {
            "id": 100000,
            "name": "Test Name",
            "address": "Test Address",
            "city": "Test city",
            "zip_code": "Test zip_code",
            "province": "Test province",
            "country": "Test country",
            "contact_name": "Test contact_name",
            "contact_phone": "123456789",
            "contact_email": "email@email.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }
        response = requests.get(
            f"{BASE_URL}/api/v1/clients/100000", headers=headers)
        assert response.status_code == 200, f"Returns {response.status_code}, should be 200"
        clientFromDB = response.json()
        assert clientFromDB["id"] == expectedJson["id"] and \
               clientFromDB["name"] ==  expectedJson["name"] and\
               clientFromDB["address"] == expectedJson["address"] and\
               clientFromDB["city"] == expectedJson["city"] and\
               clientFromDB["zip_code"] == expectedJson["zip_code"] and\
               clientFromDB["province"] == expectedJson["province"] and \
               clientFromDB["country"] == expectedJson["country"] and \
               clientFromDB["contact_name"] == expectedJson["contact_name"] and\
               clientFromDB["contact_phone"] == expectedJson["contact_phone"] and\
               clientFromDB["contact_email"] == expectedJson["contact_email"], f"Client in DB doesn't match expected Client"

    def test_clients_get_endpoint_non_existent(self):
        # test the get endpoint for an id that doesn't exist 
        # should return 404
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{BASE_URL}/api/v1/clients/99999", headers=headers)
        assert response.status_code == 404, f"Returns {response.status_code}, should be 404 because client doesn't exist"
        # ?? returns 200 instead of 404

    def test_clients_put_endpoint(self):
        
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newUpdatedClientJson = {
            "id": 100000,
            "name": "Test Name updated", # <- changed
            "address": "Test Address updated", # <- changed
            "city": "Test city",
            "zip_code": "Test zip_code",
            "province": "Test province",
            "country": "Test country",
            "contact_name": "Test contact_name",
            "contact_phone": "123456789",
            "contact_email": "email@email.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }

        response = requests.put(
            f"{BASE_URL}/api/v1/clients/100000", headers=headers, json=newUpdatedClientJson)
        assert response.status_code == 200, f"Returns {response.status_code}, Should be 200 for successful update"
        responseGet = requests.get(
            f"{BASE_URL}/api/v1/clients/100000", headers=headers)
        clientFromDB = responseGet.json()
        assert clientFromDB["id"] == newUpdatedClientJson["id"] and \
               clientFromDB["name"] ==  newUpdatedClientJson["name"] and\
               clientFromDB["address"] == newUpdatedClientJson["address"] and\
               clientFromDB["city"] == newUpdatedClientJson["city"] and\
               clientFromDB["zip_code"] == newUpdatedClientJson["zip_code"] and\
               clientFromDB["province"] == newUpdatedClientJson["province"] and \
               clientFromDB["country"] == newUpdatedClientJson["country"] and \
               clientFromDB["contact_name"] == newUpdatedClientJson["contact_name"] and\
               clientFromDB["contact_phone"] == newUpdatedClientJson["contact_phone"] and\
               clientFromDB["contact_email"] == newUpdatedClientJson["contact_email"], "updated Client in DB doesn't match the updated json"
    
    def test_clients_put_endpoint_non_existent(self):
        
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }

        newUpdatedClientJson = {
            "id": 100002,
            "name": "Test Name updated", # <- changed
            "address": "Test Address updated", # <- changed
            "city": "Test city",
            "zip_code": "Test zip_code",
            "province": "Test province",
            "country": "Test country",
            "contact_name": "Test contact_name",
            "contact_phone": "123456789",
            "contact_email": "email@email.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }

        response = requests.put(
            f"{BASE_URL}/api/v1/clients/100002", headers=headers, json=newUpdatedClientJson)
        assert response.status_code == 404, f"Returns {response.status_code}, Should return 404 because client doesn't exist"
        # ?? returns 200 instead of 404

    def test_clients_delete_endpoint(self):
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
        response = requests.delete(
            f"{BASE_URL}/api/v1/warehouses/9000", headers=headers)
        assert response.status_code == 200, "Returns {response.status_code}, Should be 200 for successful deletion"
        assert self.ClientsObject.get_client(9000) == None, "Client shouldn't exist in the DB"

    def test_clients_delete_endpoint_non_existent(self):
        headers = {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"
        }
        response = requests.delete(
            f"{BASE_URL}/api/v1/clients/9003", headers=headers)
        assert response.status_code == 404, f"Returns {response.status_code}, Should return 404 because client doesn't exist"
        # ?? returns 200 instead of 404

    ########## Test Client Methods ##########

    def test_get_clients(self):

        clientsInJson = self.ClientsObject.get_clients()
        assert clientsInJson == [
        {
            "id": 1,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "2010-04-28 02:22:53",
            "updated_at": "2022-02-09 20:22:35"
        },
        {
            "id": 2,
            "name": "Williams Ltd",
            "address": "2989 Flores Turnpike Suite 012",
            "city": "Lake Steve",
            "zip_code": "08092",
            "province": "Arkansas",
            "country": "United States",
            "contact_name": "Megan Hayden",
            "contact_phone": "8892853366",
            "contact_email": "qortega@example.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }
        ], "The client with ID 2 doesn't match the expected dictionary"

    def test_get_client_with_id(self):
        clientWithId2 = self.ClientsObject.get_client(2)
        assert clientWithId2 == {
            "id": 2,
            "name": "Williams Ltd",
            "address": "2989 Flores Turnpike Suite 012",
            "city": "Lake Steve",
            "zip_code": "08092",
            "province": "Arkansas",
            "country": "United States",
            "contact_name": "Megan Hayden",
            "contact_phone": "8892853366",
            "contact_email": "qortega@example.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }, "The client with id 2 doesn't match the dictionary"

    def test_add_client(self):
        newclient = {
            "id": 3, 
            "name": "New name",
            "address": "New address",
            "city": "New city",
            "zip_code": "New zip_code",
            "province": "New province" ,
            "country": "New country",
            "contact_name": "New contact_name",
            "contact_phone": "000000000",
            "contact_email": "new@email.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }
        self.ClientsObject.add_client(newclient)
        clientFromDB = self.ClientsObject.get_client(3)
        assert clientFromDB["id"] == newclient["id"] and \
               clientFromDB["name"] ==  newclient["name"] and\
               clientFromDB["address"] == newclient["address"] and\
               clientFromDB["city"] == newclient["city"] and\
               clientFromDB["zip_code"] == newclient["zip_code"] and\
               clientFromDB["province"] == newclient["province"] and \
               clientFromDB["country"] == newclient["country"] and \
               clientFromDB["contact_name"] == newclient["contact_name"] and\
               clientFromDB["contact_phone"] == newclient["contact_phone"] and\
               clientFromDB["contact_email"] == newclient["contact_email"] and\
               "The json doesn't match the created newclient dictionary , or get_client doesn't function properly"
    def test_update_client(self):
        

        newUpdatedclient = {
            "id": 3, 
            "name": "New name updated", # <- changed
            "address": "New address updated", # <- changed
            "city": "New city updated", # <- changed
            "zip_code": "New zip_code updated", # <- changed
            "province": "New province" ,
            "country": "New country",
            "contact_name": "New contact_name",
            "contact_phone": "000000000",
            "contact_email": "new@email.net",
            "created_at": "1973-02-24 07:36:32",
            "updated_at": "2014-06-20 17:46:19"
        }

        self.ClientsObject.update_client(3, newUpdatedclient)
        clientFromDB = self.ClientsObject.get_client(3)
        assert clientFromDB["id"] == newUpdatedclient["id"] and \
               clientFromDB["name"] ==  newUpdatedclient["name"] and\
               clientFromDB["address"] == newUpdatedclient["address"] and\
               clientFromDB["city"] == newUpdatedclient["city"] and\
               clientFromDB["zip_code"] == newUpdatedclient["zip_code"] and\
               clientFromDB["province"] == newUpdatedclient["province"] and \
               clientFromDB["country"] == newUpdatedclient["country"] and \
               clientFromDB["contact_name"] == newUpdatedclient["contact_name"] and\
               clientFromDB["contact_phone"] == newUpdatedclient["contact_phone"] and\
               clientFromDB["contact_email"] == newUpdatedclient["contact_email"] and\
               "The JSON response doesn't match the updated newUpdatedclient dictionary, or get_client doesn't function properly."

    def test_remove_client(self):

        self.ClientsObject.remove_client(3)
        assert self.ClientsObject.get_client(3) == None, \
        "Client with ID 3 still exists in the database, or get_client doesn't function properly."
