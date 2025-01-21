import pytest
import sys
import os
import requests
from dotenv import load_dotenv

load_dotenv()
# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')))

from models.clients import Clients  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL


# Client Endpoint Testing (server must be running when testing endpoints)
@pytest.fixture(scope="module", autouse=True)
def cleanup_clients():
    yield
    # Cleanup code
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
    ids = [10000, 10001, 10002, 10003, 10004, 10005]
    for client_id in ids:
        response_delete = requests.delete(
            f"{BASE_URL}/api/v1/clients/{client_id}", headers=headers_full)
        print(
            f"Cleanup response for client {client_id}: {response_delete.status_code}")


def GetObjectFromDB(id):
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    responseGet = requests.get(
        f"{BASE_URL}/api/v1/clients/{id}", headers=headers_full)

    if responseGet.status_code == 200 and responseGet.content:
        responseJson = responseGet.json()
        # set the created_at and updated_at to "-"
        responseJson["created_at"] = "-"
        responseJson["updated_at"] = "-"
        return responseJson, responseGet.status_code
    else:
        return None, responseGet.status_code


def GetJsonClientPostObjects(json_string):
    json_objects_dictionary = {
        "PostCorrect":
        {
            "id": 10000,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "-",
            "updated_at": "-"
        },

        "PostExistingID":
        {
            "id": 10000,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "-",
            "updated_at": "-"
        },

        "PostMissingItems":
        {
            "id": 10001,
            # "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            # "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            # "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            # "created_at": "-",
            "updated_at": "-"
        },

        "PostExtraItems":
        {
            "id": 10002,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "-",
            "updated_at": "-",
            "a": 1,
            "b": [2, 5, 7],
            "c": True
        },

        "PostWrongTypes":
        {
            "id": 10003,
            "name": True,
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": [1, 4, "list"],
            "province": "Colorado",
            "country": "United States",
            "contact_name": {"a": 1},
            "contact_phone": "242.732.3483x2573",
            "contact_email": None,
            "created_at": "-",
            "updated_at": False
        },

        "PostEmptyValues":
        {
            "id": 10004,
            "name": "",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "",
            "province": "Colorado",
            "country": "",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "",
            "created_at": "-",
            "updated_at": "",
        }

    }
    return json_objects_dictionary[json_string]


@pytest.mark.parametrize("objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse", [
                        ("PostCorrect", 201, 200, "PostCorrect"),
                        ("PostExistingID", 409, 200, "PostCorrect"),
                        ("PostMissingItems", 400, 404, None),
                        ("PostExtraItems", 400, 404, None),
                        ("PostWrongTypes", 400, 404, None),
                        ("PostEmptyValues", 400, 404, None)])
def test_post_endpoints_func(objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse):
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
    clientObject = GetJsonClientPostObjects(objectKey)
    responsePost = requests.post(
        f"{BASE_URL}/api/v1/clients", headers=headers_full, json=clientObject)

    assert responsePost.status_code == expectedStatusCode, f"{objectKey}, Returns {responsePost.status_code}, Expected {expectedStatusCode}"

    responseJson, status_code = GetObjectFromDB(clientObject["id"])
    assert status_code == expectedGetStatusCode
    if expectedGetResponse == None:
        assert responseJson == None
    else:
        assert responseJson == GetJsonClientPostObjects(
            expectedGetResponse), "Response does not match expected response"


def GetJsonClientGetObjects(json_string):
    json_objects_dictionary = {
        "GetCorrect":
        {
            "id": 10000,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "-",
            "updated_at": "-"
        },
        "GetNonExistent":
        {
            "id": 100000,
            "name": "a",
            "address": "a",
            "city": "a",
            "zip_code": "a",
            "province": "a",
            "country": "a",
            "contact_name": "a",
            "contact_phone": "a",
            "contact_email": "a",
            "created_at": "-",
            "updated_at": "-"
        },
        "GetWrongType":
        {
            "id": "b",
            "name": "b",
            "address": "b",
            "city": "b",
            "zip_code": "b",
            "province": "b",
            "country": "b",
            "contact_name": "b",
            "contact_phone": "b",
            "contact_email": "b",
            "created_at": "-",
            "updated_at": "-"
        }
    }
    return json_objects_dictionary[json_string]


@pytest.mark.parametrize("objectKey, expectedStatusCode, expectedGetResponse", [
                        ("GetCorrect", 200, "GetCorrect"),
                        ("GetNonExistent", 404, None),
                        ("GetWrongType", 400, None)
])
def test_get_endpoints_func(objectKey, expectedStatusCode, expectedGetResponse):

    expectedClientObject = GetJsonClientGetObjects(objectKey)
    responseJson, statusCode = GetObjectFromDB(expectedClientObject["id"])
    assert statusCode == expectedStatusCode, f"{objectKey}, Returns {statusCode}, Expected {expectedStatusCode}"
    if expectedGetResponse == None:
        assert responseJson == None
    else:
        assert responseJson == GetJsonClientGetObjects(expectedGetResponse)


def GetJsonClientPutObjects(jsonString):

    jsonobjects = {
        "PutCorrect":
        {
            "id": 10000,
            "name": "Raymond",                      # Changed
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28311",                    # Changed
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Krul",           # Changed
            "contact_phone": "242.732.3483x2555",   # Changed
            "contact_email": "robertcharles@example.net",
            "created_at": "-",
            "updated_at": "-"
        },
        "PutNonExistentId":
        {
            "id": 10000,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "-",
            "updated_at": "-"
        },
        "PutMissingItems":
        {
            "id": 10000,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            # "country": "United States",
            # "contact_name": "Bryan Clark",
            # "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "-",
            "updated_at": "-"
        },
        "PutExtraItems":
        {
            "id": 10000,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "a": 1,
            "b": True,
            "c": [],
            "created_at": "-",
            "updated_at": "-"
        },
        "PutWrongTypes":
        {
            "id": 10000,
            "name": "Raymond Inc",
            "address": None,
            "city": "Pierceview",
            "zip_code": "28301",
            "province": True,
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": 4,
            "contact_email": "robertcharles@example.net",
            "created_at": "-",
            "updated_at": []
        },
        "PutEmptyValues":
        {
            "id": 10000,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "",
            "zip_code": "28301",
            "province": "",
            "country": "United States",
            "contact_name": "",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "",
            "created_at": "-",
            "updated_at": ""
        }
    }
    return jsonobjects[jsonString]


@pytest.mark.parametrize("objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse", [
                        ("PutCorrect", 200, 200, "PutCorrect"),
                        ("PutNonExistentId", 404, 404, None),
                        ("PutMissingItems", 400, 200, "PutCorrect"),
                        ("PutExtraItems", 400, 200, "PutCorrect"),
                        ("PutWrongTypes", 400, 200, "PutCorrect"),
                        ("PutEmptyValues", 400, 200, "PutCorrect")])
def test_put_endpoints_func(objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse):
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
    clientObject = GetJsonClientPutObjects(objectKey)
    responsePut = requests.put(
        f"{BASE_URL}/api/v1/clients/{clientObject['id']}", headers=headers_full, json=clientObject)

    assert responsePut.status_code == expectedStatusCode, f"{objectKey}, Returns {responsePut.status_code}, Expected {expectedStatusCode}"

    responseJson, status_code = GetObjectFromDB(clientObject["id"])

    assert status_code == expectedGetStatusCode
    if expectedGetResponse == None:
        assert responseJson == None, "Response does not match expected response NONE"
    else:
        assert responseJson == GetJsonClientPutObjects(
            expectedGetResponse), "Response does not match expected response"


def delete_id(jsonString):
    ids = {"DeleteCorrect": 10000, "DeleteNonExistentId": 100004}
    return ids[jsonString]


@pytest.mark.parametrize("TestName, expectedStatusCode, expectedGetStatusCode", [
                        ("DeleteCorrect", 200, 404),
                        ("DeleteNonExistentId", 404, 404)])
def test_delete_endpoint(TestName, expectedStatusCode, expectedGetStatusCode):
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }

    deleteId = delete_id(TestName)
    responseDelete = requests.delete(
        f"{BASE_URL}/api/v1/clients/{deleteId}", headers=headers_full)
    assert responseDelete.status_code == expectedStatusCode, f"{TestName}, Returns: {responseDelete.status_code}, Expected: {expectedStatusCode}"

    # responseJson, status_code = GetObjectFromDB(delete_id)
    # assert status_code == expectedGetStatusCode, f"{TestName}, Returns: {status_code}, Expected: {expectedGetStatusCode}"


def test_endpoint_restrictions():

    headers_restricted = {
        "API_KEY": os.getenv("API_KEY_2"),
        "Content-Type": "application/json"
    }

    clientObject = GetJsonClientPostObjects("PostCorrect")

    responsePost_restricted = requests.post(
        f"{BASE_URL}/api/v1/clients", headers=headers_restricted, json=clientObject)
    responsePut_restricted = requests.put(
        f"{BASE_URL}/api/v1/clients/{clientObject['id']}", headers=headers_restricted, json=clientObject)
    responseDelete_restricted = requests.delete(
        f"{BASE_URL}/api/v1/clients/{clientObject['id']}", headers=headers_restricted)
    responseGetAll_restricted = requests.get(
        f"{BASE_URL}/api/v1/clients", headers=headers_restricted)
    responseGet_restricted = requests.get(
        f"{BASE_URL}/api/v1/clients/{clientObject['id']}", headers=headers_restricted)
    responseGetLocations_restricted = requests.get(
        f"{BASE_URL}/api/v1/clients/{clientObject['id']}/orders", headers=headers_restricted)

    assert responsePost_restricted.status_code == 403, "Post failed"
    assert responsePut_restricted.status_code == 403, "Put failed"
    assert responseDelete_restricted.status_code == 403, "Delete failed"

    assert responseGetAll_restricted.status_code == 200, "Get All failed"
    assert responseGet_restricted.status_code == 200, "Get by id failed"
    assert responseGetLocations_restricted.status_code == 200, "Get locations failed"
