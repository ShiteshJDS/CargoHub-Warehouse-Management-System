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


BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


# inventory Endpoint Testing (server must be running when testing endpoints)
@pytest.fixture(scope="module", autouse=True)
def cleanup_Inventories():
    yield
    # Cleanup code
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
    ids = [10000, 10001, 10002]
    for inventory_id in ids:
        response_delete = requests.delete(f"{BASE_URL}/api/v1/inventories/{inventory_id}", headers=headers_full)
        print(f"Cleanup response for inventory {inventory_id}: {response_delete.status_code}")

def GetObjectFromDB(id):
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
   
    responseGet = requests.get(
        f"{BASE_URL}/api/v1/inventories/{id}", headers=headers_full)

    if responseGet.status_code == 200 and responseGet.content:
        responseJson = responseGet.json()
        # set the created_at and updated_at to "-"
        responseJson["created_at"] = "-"
        responseJson["updated_at"] = "-"
        return responseJson, responseGet.status_code
    else:
        return None, responseGet.status_code

def GetJsonInventoryPostObjects(json_string):
    json_objects_dictionary = { 
        "PostCorrect" : 
        {
            "id": 20000,
            "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "-",
            "updated_at": "-"
        },

        "PostExistingID" :
        {
            "id": 20000,
            "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "-",
            "updated_at": "-"
        },
        
        "PostMissingItems" :
        {
            "id": 20001,
            # "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 262,
            # "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            # "total_available": 141,
            "created_at": "-",
            "updated_at": "-"
        },

        "PostExtraItems" :
        {
            "id": 20002,
            "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "-",
            "updated_at": "-",
            "a" : 1,
            "b" : 2,
            "c" : 3
        },

        "PostWrongTypes" :
        {
            "id": "d",
            "item_id": 1,
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": '''
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ''',
            "total_on_hand": 262,
            "total_expected": "one",
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "-",
            "updated_at": "-"
        },

        "PostEmptyValues":
        {
             "id": 20003,
            "item_id": "",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "",
            "locations": [],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "2015-02-19 16:08:24",
            "updated_at": "2015-09-26 06:37:56"
                }
        
    }
    return json_objects_dictionary[json_string]


    # test_post_existing_id_endpoint()    # ?? Multiple id's
    # test_post_missing_items_endpoint()  # ?? Missing items
    # test_post_extra_items_endpoint()    # ?? Extra items
    # test_post_wrong_types_endpoint()    # ?? Wrong item types
    # test_post_empty_values_endpoint()   # ?? Empty items

#objectKey is the key of the json object to be used in the test
#expectedStatusCode is the expected status code of the put request
#expectedGetStatusCode is the expected status code of the get request used for verification
#expectedGetResponse is the key to the expected json response of the get request used for verification
@pytest.mark.parametrize("objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse", [
                        ("PostCorrect", 201, 200, "PostCorrect"), #tests the correct post endpoint
                        ("PostExistingID", 409, 200, "PostCorrect"), #tests the post endpoint with an existing id
                        ("PostMissingItems", 400, 404, None), #tests the post endpoint with missing items
                        ("PostExtraItems", 400, 404, None), #tests the post endpoint with extra items
                        ("PostWrongTypes", 400, 404, None), #tests the post endpoint with wrong types
                        ("PostEmptyValues", 400, 404, None)]) #tests the post endpoint with empty values

def test_post_endpoints_func(objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse):
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
    inventoryObject = GetJsonInventoryPostObjects(objectKey)
    responsePost = requests.post(
        f"{BASE_URL}/api/v1/inventories", headers=headers_full, json=inventoryObject)
    
    assert responsePost.status_code == expectedStatusCode, f"{objectKey}, Returns {responsePost.status_code}, Expected {expectedStatusCode}"


    responseJson, status_code = GetObjectFromDB(inventoryObject["id"])
    assert status_code == expectedGetStatusCode
    if expectedGetResponse == None:
        assert responseJson == None
    else:
        assert responseJson == GetJsonInventoryPostObjects(expectedGetResponse), "Response does not match expected response"

def GetJsonInventoryGetObjects(json_string):
    json_objects_dictionary = {
        "GetCorrect": 
        {
            "id": 20000,
            "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "-",
            "updated_at": "-"
        },
        "GetNonExistent": 
        {
            "id": 200000,
            "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "-",
            "updated_at": "-"
        },
        "GetWrongType": 
        {
            "id": "a",
            "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "-",
            "updated_at": "-"
        }
    }
    return json_objects_dictionary[json_string]

#objectKey is the key of the json object to be used in the test
#expectedStatusCode is the expected status code of the put request
#expectedGetResponse is the key to the expected response of the get request used for verification
@pytest.mark.parametrize("objectKey, expectedStatusCode, expectedGetResponse",[
                        ("GetCorrect", 200, "GetCorrect"), #tests the correct get endpoint
                        ("GetNonExistent", 404, None), #tests the get endpoint with a non existent id
                        ("GetWrongType", 400, None) #tests the get endpoint with a wrong type
])

def test_get_endpoints_func(objectKey, expectedStatusCode, expectedGetResponse):

    expectedInventoryObject = GetJsonInventoryGetObjects(objectKey)
    responseJson, statusCode = GetObjectFromDB(expectedInventoryObject["id"])
    assert statusCode == expectedStatusCode, f"{objectKey}, Returns {statusCode}, Expected {expectedStatusCode}"
    if expectedGetResponse == None:
        assert responseJson == None
    else:
        assert responseJson == GetJsonInventoryGetObjects(expectedGetResponse)

# class Test_Put_Endpoints(unittest.TestCase):
def GetJsonInventoryPutObjects(jsonString):

    jsonobjects = {
        "PutCorrect": 
        {
            "id": 20000,
            "item_id": "P006543",   #<-- changed
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "abcdefg123",  #<-- changed
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 300,  #<-- changed
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 150, #<-- changed
            "created_at": "-", 
            "updated_at": "-"
        },
        "PutNonExistentId" :
        {
            "id": 200000,
            "item_id": "P006543",   #<-- changed
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "abcdefg123",  #<-- changed
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 300,  #<-- changed
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 150, #<-- changed
            "created_at": "-", 
            "updated_at": "-"
        },
        "PutMissingItems": 
        {
           "id": 20000,
            # "item_id": "P006543",  
            "description": "Face-to-face clear-thinking complexity",
            # "item_reference": "abcdefg123", 
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 300, 
            "total_expected": 0,
            "total_ordered": 80,
            # "total_allocated": 41,
            "total_available": 150, 
            "created_at": "-", 
            "updated_at": "-"
        },
        "PutExtraItems" :
        {
            "id": 20000,
            "item_id": "P006543",   #<-- changed
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "abcdefg123",  #<-- changed
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 300,  #<-- changed
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 150, #<-- changed
            "created_at": "-", 
            "updated_at": "-",
            "a" : 1,
            "b" : True,
            "c" : []
        },
        "PutWrongTypes" :
        {
            "id": True,
            "item_id": 3,   #<-- changed
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": ["abcdefg123"],  #<-- changed
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": "300",  #<-- changed
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": "41",
            "total_available": 150, #<-- changed
            "created_at": "-", 
            "updated_at": "-"
        },
        "PutEmptyValues" :
        {
            "id": 20000,
            "item_id": "",   #<-- changed
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "",  #<-- changed
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
                    ],
            "total_on_hand": 0,  #<-- changed
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 0, #<-- changed
            "created_at": "-", 
            "updated_at": "-"
        }
    }
    return jsonobjects[jsonString]

#objectKey is the key of the json object to be used in the test
#expectedStatusCode is the expected status code of the put request
#expectedGetStatusCode is the expected status code of the get request used for verification
#expectedGetResponse is the expected response of the get request used for verification
@pytest.mark.parametrize("objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse", [
                        ("PutCorrect", 200, 200, "PutCorrect"), #tests the correct put endpoint
                        ("PutNonExistentId", 404, 404, None), #tests the put endpoint with a non existent id
                        ("PutMissingItems", 400, 200, "PutCorrect"),    #tests the put endpoint with missing items
                        ("PutExtraItems", 400, 200, "PutCorrect"),   #tests the put endpoint with extra items
                        ("PutWrongTypes", 400, 200, "PutCorrect"),  #tests the put endpoint with wrong types
                        ("PutEmptyValues", 400, 200, "PutCorrect")])  #tests the put endpoint with empty values

def test_put_endpoints_func(objectKey, expectedStatusCode, expectedGetStatusCode, expectedGetResponse):
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
    inventoryObject = GetJsonInventoryPutObjects(objectKey)
    responsePut = requests.put(
        f"{BASE_URL}/api/v1/inventories/{inventoryObject['id']}", headers=headers_full, json=inventoryObject)
    
    assert responsePut.status_code == expectedStatusCode, f"{objectKey}, Returns {responsePut.status_code}, Expected {expectedStatusCode}"
    
    responseJson, status_code = GetObjectFromDB(inventoryObject["id"])

    assert status_code == expectedGetStatusCode, f"{objectKey} Get Request, Returns {responsePut.status_code}, Expected {expectedStatusCode}"
    if expectedGetResponse == None:
        assert responseJson == None, "Response does not match expected response NONE"
    else:
        assert responseJson == GetJsonInventoryPutObjects(expectedGetResponse), "Response does not match expected response"

def delete_id(jsonString):
    ids = {"DeleteCorrect" : 20000, "DeleteNonExistentId" : 20004}
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
        f"{BASE_URL}/api/v1/inventories/{deleteId}", headers=headers_full)
    assert responseDelete.status_code == expectedStatusCode, f"{TestName}, Returns: {responseDelete.status_code}, Expected: {expectedStatusCode}"

    # responseJson, status_code = GetObjectFromDB(delete_id)
    # assert status_code == expectedGetStatusCode, f"{TestName}, Returns: {status_code}, Expected: {expectedGetStatusCode}"


def test_endpoint_restrictions():

    headers_restricted = {
        "API_KEY": os.getenv("API_KEY_2"),
        "Content-Type": "application/json"
    }
    
    inventoryObject = GetJsonInventoryPostObjects("PostCorrect")

    responsePost_restricted = requests.post(
        f"{BASE_URL}/api/v1/inventories", headers=headers_restricted, json=inventoryObject)
    responsePut_restricted = requests.put(
        f"{BASE_URL}/api/v1/inventories/{inventoryObject['id']}", headers=headers_restricted, json=inventoryObject)
    responseDelete_restricted = requests.delete(
        f"{BASE_URL}/api/v1/inventories/{inventoryObject['id']}", headers=headers_restricted)
    responseGetAll_restricted = requests.get(
        f"{BASE_URL}/api/v1/inventories", headers=headers_restricted)
    responseGet_restricted = requests.get(
        f"{BASE_URL}/api/v1/inventories/{inventoryObject['id']}", headers=headers_restricted)
    responseGetLocations_restricted = requests.get(
        f"{BASE_URL}/api/v1/inventories/{inventoryObject['id']}/locations", headers=headers_restricted)

    assert responsePost_restricted.status_code == 403, "Post failed"
    assert responsePut_restricted.status_code == 403, "Put failed"
    assert responseDelete_restricted.status_code == 403, "Delete failed"

    assert responseGetAll_restricted.status_code == 200, "Get All failed"
    assert responseGet_restricted.status_code == 200, "Get by id failed"
    assert responseGetLocations_restricted.status_code == 200, "Get locations failed"

# Post, Put, Delete are not working correctly