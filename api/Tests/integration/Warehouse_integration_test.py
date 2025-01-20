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

from models.warehouses import Warehouses  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


# Warehouse Endpoint Testing (server must be running when testing endpoints)

def GetObjectFromDB(id):
    headers_full = {
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
    }

    responseGet = requests.get(
        f"{BASE_URL}/api/v1/warehouses/{id}", headers=headers_full)
    
    # Print the response status code and content for debugging
    print(f"Response status code: {responseGet.status_code}")
    print(f"Response content: {responseGet.content}")

    if responseGet.status_code == 200 and responseGet.content:
        responseJson = responseGet.json()
        # set the created_at and updated_at to "-"
        responseJson["created_at"] = "-"
        responseJson["updated_at"] = "-"
        return responseJson, responseGet.status_code
    else:
        return None, responseGet.status_code

def GetJsonWarehousePostObjects(json_string):
    json_objects_dictionary = { 
        "PostCorrect" : 
        {
            "id": 10000,
            "code": "YQZZNL56",
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": "Heemskerk",
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Fem Keijzer",
                "phone": "(078) 0013363",
                "email": "blamore@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },

        "PostExistingID" :
        {
            "id": 10000,
            "code": "YQZZNL56",
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": "Heemskerk",
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Fem Keijzer",
                "phone": "(078) 0013363",
                "email": "blamore@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },
        
        "PostMissingItems" :
        {
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Fem Keijzer",
                "phone": "(078) 0013363",
                "email": "blamore@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },

        "PostExtraItems" :
        {
            "id": 10001,
            "code": "YQZZNL56",
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": "Heemskerk",
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Fem Keijzer",
                "phone": "(078) 0013363",
                "email": "blamore@example.net"
            },
            "created_at": "-",
            "updated_at": "-",
            "a" : 1,
            "b" : 2,
            "c" : 3
        },

        "PostWrongTypes" :
        {
            "id": True,
            "code": [1,2,3],
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": 1,
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Fem Keijzer",
                "phone": "(078) 0013363",
                "email": "blamore@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },

        "PostEmptyValues":
        {
            "id": 10002,
            "code": "",
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "",
            "city": "",
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Fem Keijzer",
                "phone": "(078) 0013363",
                "email": "blamore@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        }
        
    }
    return json_objects_dictionary[json_string]


    # test_post_existing_id_endpoint()    # ?? Multiple id's
    # test_post_missing_items_endpoint()  # ?? Missing items
    # test_post_extra_items_endpoint()    # ?? Extra items
    # test_post_wrong_types_endpoint()    # ?? Wrong item types
    # test_post_empty_values_endpoint()   # ?? Empty items

@pytest.mark.parametrize("objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse", [
                        ("PostCorrect", 201, 200, "PostCorrect"),
                        ("PostExistingID", 409, 200, "PostCorrect"),
                        ("PostMissingItems", 400, 404, None),
                        ("PostExtraItems", 400, 404, None),
                        ("PostWrongTypes", 400, 404, None),
                        ("PostEmptyValues", 400, 404, None)])

def test_post_endpoints_func(objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse):
    headers_full = {
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
    }
    warehouseObject = GetJsonWarehousePostObjects(objectKey)
    responsePost = requests.post(
        f"{BASE_URL}/api/v1/warehouses", headers=headers_full, json=warehouseObject)
    
    assert responsePost.status_code == expectedStatusCode, f"{objectKey}, Returns {responsePost.status_code}, Expected {expectedStatusCode}"


    # responseJson, status_code = GetObjectFromDB(warehouseObject["id"])
    # assert status_code == expectedGetStatusCode
    # if expectedGetResponse != None:
    #     assert responseJson == None
    # else:
    #     assert responseJson == GetJsonWarehousePostObjects(expectedGetResponse)

def GetJsonWarehouseGetObjects(json_string):
    json_objects_dictionary = {
        "GetCorrect": 
        {
            "id": 10000,
            "code": "YQZZNL56",
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": "Heemskerk",
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Fem Keijzer",
                "phone": "(078) 0013363",
                "email": "blamore@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },
        "GetNonExistent": 
        {
            "id": 100000,
            "code": "a",
            "name": "a",
            "address": "a",
            "zip": "a",
            "city": "a",
            "province": "a",
            "country": "a",
            "contact":
            {
                "name": "a",
                "phone": "a",
                "email": "a"
            },
            "created_at": "-",
            "updated_at": "-"
        },
        "GetWrongType": 
        {
            "id": "b",
            "code": "b",
            "name": "b",
            "address": "b",
            "zip": "b",
            "city": "b",
            "province": "b",
            "country": "b",
            "contact":
            {
                "name": "b",
                "phone": "b",
                "email": "b"
            },
            "created_at": "-",
            "updated_at": "-"
        }
    }
    return json_objects_dictionary[json_string]


@pytest.mark.parametrize("objectKey, expectedStatusCode, expectedGetResponse",[
                        ("GetCorrect", 200, "GetCorrect"),
                        ("GetNonExistent", 404, None),
                        ("GetWrongType", 400, None)
])

def test_get_endpoints_func(objectKey, expectedStatusCode, expectedGetResponse):

    expectedWarehouseObject = GetJsonWarehouseGetObjects(objectKey)
    responseJson, statusCode = GetObjectFromDB(expectedWarehouseObject["id"])
    assert statusCode == expectedStatusCode, f"{objectKey}, Returns {statusCode}, Expected {expectedStatusCode}"
    if expectedGetResponse != None:
        assert responseJson == None
    else:
        assert responseJson == GetJsonWarehouseGetObjects(expectedGetResponse)

# class Test_Put_Endpoints(unittest.TestCase):
def GetJsonWarehousePutObjects(jsonString):

    jsonobjects = {
        "PutCorrect": 
        {
            "id": 10000,
            "code": "Y4ZYNL57", # changed
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": "Rotterdam", #changed
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Kevin Krul", #changed
                "phone": "(079) 0318253", #changed
                "email": "kevin@example.net" #changed
            },
            "created_at": "-",
            "updated_at": "-"
        },
        "PutNonExistentId" :
        {
            "id": 10000,
            "code": "Y4ZYNL57", 
            "name": "Heemskerk cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": "Rotterdam", 
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "John Doe", 
                "phone": "(079) 123456", 
                "email": "John@Doe.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },
        "PutMissingItems": 
        {
            "id": 10000,
            # "code": "Y4ZYNL57",  removed
            # "name": "Heemskerk cargo hub", removed
            # "address": "Karlijndreef 281", removed
            "zip": "4002 AS",
            "city": "Amsterdam",
            "province": "Noord-Holland",
            "country": "NL",
            "contact":
            {
                "name": "Kevin Krul",
                "phone": "(079) 0318253",
                "email": "kevin@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },
        "PutExtraItems" :
        {
            "id": 10000,
            "code": "Y4ZYNL57", 
            "name": "BE cargo hub",
            "address": "Karlijndreef 281",
            "zip": "4002 AS",
            "city": "Rotterdam",
            "province": "Friesland",
            "country": "BE",
            "a" : 1,
            "b" : 2,
            "c" : 3,
            "contact":
            {
                "name": "Jane Doe",
                "phone": "(079) 0318253",
                "email": "Jane@Doe.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },
        "PutWrongTypes" :
        {
            "id": 10000,
            "code": True,
            "name": 1,
            "address": [1,2,3],
            "zip": "4002 AS",
            "city": "Rotterdam",
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "Kevin Krul",
                "phone": "(079) 0318253",
                "email": "kevin@example.net"
            },
            "created_at": "-",
            "updated_at": "-"
        },
        "PutEmptyValues" :
        {
            "id": 10000,
            "code": "", 
            "name": "Heemskerk cargo hub",
            "address": "",
            "zip": "4002 AS",
            "city": "", 
            "province": "Friesland",
            "country": "NL",
            "contact":
            {
                "name": "", 
                "phone": "(079) 0318253",
                "email": "" 
            },
            "created_at": "-",
            "updated_at": "-"
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
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
    }
    warehouseObject = GetJsonWarehousePutObjects(objectKey)
    responsePut = requests.put(
        f"{BASE_URL}/api/v1/warehouses/{warehouseObject['id']}", headers=headers_full, json=warehouseObject)
    
    assert responsePut.status_code == expectedStatusCode, f"{objectKey}, Returns {responsePut.status_code}, Expected {expectedStatusCode}"


def delete_id(jsonString):
    ids = {"DeleteCorrect" : 10000, "DeleteNonExistentId" : 100004}
    return ids[jsonString]

@pytest.mark.parametrize("TestName, expectedStatusCode, expectedGetStatusCode", [
                        ("DeleteCorrect", 200, 404),
                        ("DeleteNonExistentId", 404, 404)])

def test_delete_endpoint(TestName, expectedStatusCode, expectedGetStatusCode):
    headers_full = {
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
        }
    
    deleteId = delete_id(TestName)
    responseDelete = requests.delete(
        f"{BASE_URL}/api/v1/warehouses/{deleteId}", headers=headers_full)
    assert responseDelete.status_code == expectedStatusCode, f"{TestName}, Returns: {responseDelete.status_code}, Expected: {expectedStatusCode}"

    # responseJson, status_code = GetObjectFromDB(delete_id)
    # assert status_code == expectedGetStatusCode, f"{TestName}, Returns: {status_code}, Expected: {expectedGetStatusCode}"


def test_endpoint_restrictions():

    headers_restricted = {
        "API_KEY": "f6g7h8i9j0",
        "Content-Type": "application/json"
    }
    
    warehouseObject = GetJsonWarehousePostObjects("PostCorrect")

    responsePost_restricted = requests.post(
        f"{BASE_URL}/api/v1/warehouses", headers=headers_restricted, json=warehouseObject)
    responsePut_restricted = requests.put(
        f"{BASE_URL}/api/v1/warehouses/{warehouseObject['id']}", headers=headers_restricted, json=warehouseObject)
    responseDelete_restricted = requests.delete(
        f"{BASE_URL}/api/v1/warehouses/{warehouseObject['id']}", headers=headers_restricted)
    responseGetAll_restricted = requests.get(
        f"{BASE_URL}/api/v1/warehouses", headers=headers_restricted)
    responseGet_restricted = requests.get(
        f"{BASE_URL}/api/v1/warehouses/{warehouseObject['id']}", headers=headers_restricted)
    responseGetLocations_restricted = requests.get(
        f"{BASE_URL}/api/v1/warehouses/{warehouseObject['id']}/locations", headers=headers_restricted)

    assert responsePost_restricted.status_code == 403, "Post failed"
    assert responsePut_restricted.status_code == 403, "Put failed"
    assert responseDelete_restricted.status_code == 403, "Delete failed"

    assert responseGetAll_restricted.status_code == 200, "Get All failed"
    assert responseGet_restricted.status_code == 200, "Get by id failed"
    assert responseGetLocations_restricted.status_code == 200, "Get locations failed"