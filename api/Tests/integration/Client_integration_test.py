import pytest

import unittest


import sys
import os
import pytest
import requests
import json
from dotenv import load_dotenv

load_dotenv()

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

    ClientsObject = Clients("Test_Data/Cargohub_Test.db")


    ########## Test Endpoint ##########

    # server must be running when testing endpoints
    def test_clients_post_endpoint_success(self):

        headers = {
            "API_KEY": os.getenv("API_KEY_1"),
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
            "API_KEY": os.getenv("API_KEY_1"),
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
            "API_KEY": os.getenv("API_KEY_1"),
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
            "API_KEY": os.getenv("API_KEY_1"),
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
            "API_KEY": os.getenv("API_KEY_1"),
            "Content-Type": "application/json"
        }
        response = requests.get(
            f"{BASE_URL}/api/v1/clients/99999", headers=headers)
        assert response.status_code == 404, f"Returns {response.status_code}, should be 404 because client doesn't exist"
        # ?? returns 200 instead of 404

    def test_clients_put_endpoint(self):
        
        headers = {
            "API_KEY": os.getenv("API_KEY_1"),
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
            "API_KEY": os.getenv("API_KEY_1"),
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
            "API_KEY": os.getenv("API_KEY_1"),
            "Content-Type": "application/json"
        }
        response = requests.delete(
            f"{BASE_URL}/api/v1/warehouses/9000", headers=headers)
        assert response.status_code == 200, "Returns {response.status_code}, Should be 200 for successful deletion"
        assert self.ClientsObject.get_client(9000) == None, "Client shouldn't exist in the DB"

    def test_clients_delete_endpoint_non_existent(self):
        headers = {
            "API_KEY": os.getenv("API_KEY_1"),
            "Content-Type": "application/json"
        }
        response = requests.delete(
            f"{BASE_URL}/api/v1/clients/9003", headers=headers)
        assert response.status_code == 404, f"Returns {response.status_code}, Should return 404 because client doesn't exist"
        # ?? returns 200 instead of 404