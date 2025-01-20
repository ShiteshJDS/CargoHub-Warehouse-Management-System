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


# supplier Endpoint Testing (server must be running when testing endpoints)
@pytest.fixture(scope="module", autouse=True)
def cleanup_suppliers():
    yield
    # Cleanup code
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
    ids = [10000, 10001, 10002]
    for supplier_id in ids:
        response_delete = requests.delete(f"{BASE_URL}/api/v1/suppliers/{supplier_id}", headers=headers_full)
        print(f"Cleanup response for supplier {supplier_id}: {response_delete.status_code}")

def GetObjectFromDB(id):
    headers_full = {
        "API_KEY": os.getenv("API_KEY_1"),
        "Content-Type": "application/json"
    }
   
    responseGet = requests.get(
        f"{BASE_URL}/api/v1/suppliers/{id}", headers=headers_full)

    if responseGet.status_code == 200 and responseGet.content:
        responseJson = responseGet.json()
        # set the created_at and updated_at to "-"
        responseJson["created_at"] = "-"
        responseJson["updated_at"] = "-"
        return responseJson, responseGet.status_code
    else:
        return None, responseGet.status_code

def GetJsonSupplierPostObjects(json_string):
    json_objects_dictionary = { 
        "PostCorrect" : 
        {
            "id": 10000,
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
            "created_at": "-",
            "updated_at": "-"
        },

        "PostExistingID" :
        {
            "id": 10000,
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
            "created_at": "-",
            "updated_at": "-"
        },
        
        "PostMissingItems" :
        {
            "code": "SUP0001",
            "name": "Lee, Parks and Johnson",
            "address": "5989 Sullivan Drives",
            "address_extra": "Apt. 996",
            "city": "Port Anitaburgh",
            "province": "Illinois",
            "country": "Czech Republic",
            "phonenumber": "363.541.7282x36825",
            "reference": "LPaJ-SUP0001",
            "created_at": "-",
            "updated_at": "-"
        },

        "PostExtraItems" :
        {
            "id": 10001,
            "id": 10000,
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
            "created_at": "-",
            "updated_at": "-",
            "a" : 1,
            "b" : 2,
            "c" : 3
        },

        "PostWrongTypes" :
        {
            "id": True,
            "code": "SUP0001",
            "name": ["Lee", "Parks","Johnson"],
            "address": "5989 Sullivan Drives",
            "address_extra": "Apt. 996",
            "city": "Port Anitaburgh",
            "zip_code": 91688,
            "province": "Illinois",
            "country": "Czech Republic",
            "contact_name": "Toni Barnett",
            "phonenumber": "363.541.7282x36825",
            "reference": "LPaJ-SUP0001",
            "created_at": "-",
            "updated_at": "-"
        },

        "PostEmptyValues":
        {
            "id": 10002,
            "code": "",
            "name": "Lee, Parks and Johnson",
            "address": "",
            "address_extra": "Apt. 996",
            "city": "Port Anitaburgh",
            "zip_code": "",
            "province": "Illinois",
            "country": "Czech Republic",
            "contact_name": "",
            "phonenumber": "363.541.7282x36825",
            "reference": "LPaJ-SUP0001",
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
    supplierObject = GetJsonSupplierPostObjects(objectKey)
    responsePost = requests.post(
        f"{BASE_URL}/api/v1/suppliers", headers=headers_full, json=supplierObject)
    
    assert responsePost.status_code == expectedStatusCode, f"{objectKey}, Returns {responsePost.status_code}, Expected {expectedStatusCode}"


    responseJson, status_code = GetObjectFromDB(supplierObject["id"])
    assert status_code == expectedGetStatusCode
    if expectedGetResponse == None:
        assert responseJson == None
    else:
        assert responseJson == GetJsonSupplierPostObjects(expectedGetResponse), "Response does not match expected response"

def GetJsonSupplierGetObjects(json_string):
    json_objects_dictionary = {
        "GetCorrect": 
        {
            "id": 10000,
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
            "created_at": "-",
            "updated_at": "-"
        },
        "GetNonExistent": 
        {
            "id": 100000,
            "code": "a",
            "name": "a",
            "address": "a",
            "address_extra": "a",
            "city": "a",
            "zip_code": "a",
            "province": "a",
            "country": "a",
            "contact_name": "a",
            "phonenumber": "a",
            "reference": "a",
            "created_at": "-",
            "updated_at": "-"
        },
        "GetWrongType": 
        {
            "id": "b",
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

    expectedSupplierObject = GetJsonSupplierGetObjects(objectKey)
    responseJson, statusCode = GetObjectFromDB(expectedSupplierObject["id"])
    assert statusCode == expectedStatusCode, f"{objectKey}, Returns {statusCode}, Expected {expectedStatusCode}"
    if expectedGetResponse == None:
        assert responseJson == None
    else:
        assert responseJson == GetJsonSupplierGetObjects(expectedGetResponse)

# class Test_Put_Endpoints(unittest.TestCase):
def GetJsonSupplierPutObjects(jsonString):

    jsonobjects = {
        "PutCorrect": 
        {
            "id": 10000,
            "code": "SUP1000", #<--- changed
            "name": "Lee, Parks and Johnson",
            "address": "5989 Sullivan Drives",
            "address_extra": "Apt. 996",
            "city": "Port Anitaburgh",
            "zip_code": "10000", #<--- changed
            "province": "Illinois",
            "country": "Czech Republic",
            "contact_name": "Tony Barn", #<--- changed
            "phonenumber": "012345678910",  #<--- changed
            "reference": "LPaJ-SUP0001",
            "created_at": "-",
            "updated_at": "-"
        },
        "PutNonExistentId" :
        {
            "id": 100001,
            "code": "SUP0001",
            "name": "Lee",  #<--- changed
            "address": "5989 Sullivan Drives",
            "address_extra": "Apt. 996",
            "city": "Port Anitaburgh",
            "zip_code": "91688",
            "province": "Arizona",  #<--- changed
            "country": "Russia",  #<--- changed
            "contact_name": "Toni Barnett",
            "phonenumber": "363.541.7282x36825",
            "reference": "LPaJ-SUP0001",
            "created_at": "-",
            "updated_at": "-"
        },
        "PutMissingItems": 
        {
            "id": 10000,
            # "code": "SUP0001", #<--- missing
            "name": "Lee, Parks and Johnson",
            "address": "5989 Sullivan Drives",
            "address_extra": "Apt. 996",
            # "city": "Port Anitaburgh", #<--- missing
            "zip_code": "91688",
            "province": "Illinois",
            "country": "Czech Republic",
            # "contact_name": "Toni Barnett", #<--- missing
            "phonenumber": "363.541.7282x36825",
            "reference": "LPaJ-SUP0001",
            "created_at": "-",
            "updated_at": "-"
        },
        "PutExtraItems" :
        {
            "id": 10000,
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
            "id": True,
            "code": "SUP0001",
            "name": "Lee, Parks and Johnson",
            "address": ["5989", "Sullivan Drives"],
            "address_extra": 996,
            "city": "Port Anitaburgh",
            "zip_code": 91688,
            "province": "Illinois",
            "country": "Czech Republic",
            "contact_name": ["Toni Barnett"],
            "phonenumber": "363.541.7282x36825",
            "reference": "LPaJ-SUP0001",
            "created_at": "-",
            "updated_at": "-"
        },
        "PutEmptyValues" :
        {
            "id": 10000,
           "code": "SUP0001",
            "name": "",
            "address": "5989 Sullivan Drives",
            "address_extra": "",
            "city": "Port Anitaburgh",
            "zip_code": "91688",
            "province": "",
            "country": "Czech Republic",
            "contact_name": "",
            "phonenumber": "363.541.7282x36825",
            "reference": "",
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
    supplierObject = GetJsonSupplierPutObjects(objectKey)
    responsePut = requests.put(
        f"{BASE_URL}/api/v1/suppliers/{supplierObject['id']}", headers=headers_full, json=supplierObject)
    
    assert responsePut.status_code == expectedStatusCode, f"{objectKey}, Returns {responsePut.status_code}, Expected {expectedStatusCode}"
    
    responseJson, status_code = GetObjectFromDB(supplierObject["id"])

    assert status_code == expectedGetStatusCode
    if expectedGetResponse == None:
        assert responseJson == None, "Response does not match expected response NONE"
    else:
        assert responseJson == GetJsonSupplierPutObjects(expectedGetResponse), "Response does not match expected response"

def delete_id(jsonString):
    ids = {"DeleteCorrect" : 10000, "DeleteNonExistentId" : 100004}
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
        f"{BASE_URL}/api/v1/suppliers/{deleteId}", headers=headers_full)
    assert responseDelete.status_code == expectedStatusCode, f"{TestName}, Returns: {responseDelete.status_code}, Expected: {expectedStatusCode}"

    # responseJson, status_code = GetObjectFromDB(delete_id)
    # assert status_code == expectedGetStatusCode, f"{TestName}, Returns: {status_code}, Expected: {expectedGetStatusCode}"


def test_endpoint_restrictions():

    headers_restricted = {
        "API_KEY": os.getenv("API_KEY_2"),
        "Content-Type": "application/json"
    }
    
    supplierObject = GetJsonSupplierPostObjects("PostCorrect")

    responsePost_restricted = requests.post(
        f"{BASE_URL}/api/v1/suppliers", headers=headers_restricted, json=supplierObject)
    responsePut_restricted = requests.put(
        f"{BASE_URL}/api/v1/suppliers/{supplierObject['id']}", headers=headers_restricted, json=supplierObject)
    responseDelete_restricted = requests.delete(
        f"{BASE_URL}/api/v1/suppliers/{supplierObject['id']}", headers=headers_restricted)
    responseGetAll_restricted = requests.get(
        f"{BASE_URL}/api/v1/suppliers", headers=headers_restricted)
    responseGet_restricted = requests.get(
        f"{BASE_URL}/api/v1/suppliers/{supplierObject['id']}", headers=headers_restricted)
    responseGetLocations_restricted = requests.get(
        f"{BASE_URL}/api/v1/suppliers/{supplierObject['id']}/locations", headers=headers_restricted)

    assert responsePost_restricted.status_code == 403, "Post failed"
    assert responsePut_restricted.status_code == 403, "Put failed"
    assert responseDelete_restricted.status_code == 403, "Delete failed"

    assert responseGetAll_restricted.status_code == 200, "Get All failed"
    assert responseGet_restricted.status_code == 200, "Get by id failed"
    assert responseGetLocations_restricted.status_code == 200, "Get locations failed"