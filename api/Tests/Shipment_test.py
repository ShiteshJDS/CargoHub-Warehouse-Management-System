
import pytest
import unittest
import sys
import os
import requests
import logging
import shutil

# Add the path to the CargoHub directory to sys.path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from models.shipments import Shipments  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

@pytest.fixture(scope="module", autouse=True)
def manage_warehouse_json_state():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, "../../data/shipments.json")
    backup_file_path = f"{json_file_path}.backup"

    # Backup the JSON file
    shutil.copyfile(json_file_path, backup_file_path)

    yield  # Run the tests

    # Restore the JSON file from backup
    shutil.copyfile(backup_file_path, json_file_path)
    os.remove(backup_file_path)  # Clean up the backup file

class Test_Shipments():

    shipmentObject = Shipments("Test_Data/test_")
    headers_full = {
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
    }

    newShipment = {
        "id": 0,
        "order_id": 2979,
        "source_id": 14,
        "order_date": "1990-05-14",
        "request_date": "1990-05-16",
        "shipment_date": "1990-05-18",
        "shipment_type": "I",
        "shipment_status": "Pending",
        "notes": "Schrijven eis kap houden gemak.",
        "carrier_code": "UPS",
        "carrier_description": "United Parcel Service",
        "service_code": "NextDay",
        "payment_type": "Automatic",
        "transfer_mode": "Ground",
        "total_package_count": 29,
        "total_package_weight": 273.78,
        "created_at": "-",
        "updated_at": "-",
        "items": [
            {
                "item_id": "P005900",
                "amount": 37
            },
            {
                "item_id": "P009650",
                "amount": 50
            },
            {
                "item_id": "P005215",
                "amount": 43
            },
            {
                "item_id": "P006029",
                "amount": 33
            },
            {
                "item_id": "P004916",
                "amount": 15
            },
            {
                "item_id": "P005210",
                "amount": 49
            },
            {
                "item_id": "P005954",
                "amount": 24
            },
            {
                "item_id": "P008475",
                "amount": 28
            },
            {
                "item_id": "P005563",
                "amount": 43
            },
            {
                "item_id": "P004387",
                "amount": 39
            },
            {
                "item_id": "P003905",
                "amount": 18
            },
            {
                "item_id": "P004197",
                "amount": 2
            },
            {
                "item_id": "P009214",
                "amount": 5
            },
            {
                "item_id": "P006997",
                "amount": 33
            },
            {
                "item_id": "P001093",
                "amount": 25
            },
            {
                "item_id": "P008432",
                "amount": 13
            },
            {
                "item_id": "P001658",
                "amount": 13
            },
            {
                "item_id": "P004518",
                "amount": 1
            },
            {
                "item_id": "P004551",
                "amount": 25
            },
            {
                "item_id": "P009852",
                "amount": 36
            },
            {
                "item_id": "P001524",
                "amount": 41
            },
            {
                "item_id": "P007633",
                "amount": 45
            },
            {
                "item_id": "P003571",
                "amount": 29
            },
            {
                "item_id": "P008751",
                "amount": 46
            }
        ]
    }

    # Shipment Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/shipments/", headers=self.headers_full, json=self.newShipment)
        new_timestamp = self.shipmentObject.get_timestamp()
        self.newShipment["created_at"] = new_timestamp.split('T')[0]
        self.newShipment["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newShipment["order_date"] = "2024-05-16"
        self.newShipment["payment_type"] = "Cash"
        self.newShipment["items"][0]["amount"] = 40

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=self.headers_full, json=self.newShipment)
        self.newShipment["updated_at"] = self.shipmentObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newShipment

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restriction(self):
        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/shipments/", headers=headers_restricted, json=self.newShipment)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=headers_restricted, json=self.newShipment)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/shipments/{self.newShipment['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200

    # Shipment Method Testing

    def test_get_shipments(self):

        allShipments = self.shipmentObject.get_shipments()
        assert allShipments == [
            {
                "id": 1,
                "order_id": 1,
                "source_id": 33,
                "order_date": "2000-03-09",
                "request_date": "2000-03-11",
                "shipment_date": "2000-03-13",
                "shipment_type": "I",
                "shipment_status": "Pending",
                "notes": "Zee vertrouwen klas rots heet lachen oneven begrijpen.",
                "carrier_code": "DPD",
                "carrier_description": "Dynamic Parcel Distribution",
                "service_code": "Fastest",
                "payment_type": "Manual",
                "transfer_mode": "Ground",
                "total_package_count": 31,
                "total_package_weight": 594.42,
                "created_at": "2000-03-10T11:11:14Z",
                "updated_at": "2000-03-11T13:11:14Z",
                "items": [
                    {
                        "item_id": "P007435",
                        "amount": 23
                    },
                    {
                        "item_id": "P009557",
                        "amount": 1
                    },
                    {
                        "item_id": "P009553",
                        "amount": 50
                    },
                    {
                        "item_id": "P010015",
                        "amount": 16
                    },
                    {
                        "item_id": "P002084",
                        "amount": 33
                    },
                    {
                        "item_id": "P009663",
                        "amount": 18
                    },
                    {
                        "item_id": "P010125",
                        "amount": 18
                    },
                    {
                        "item_id": "P005768",
                        "amount": 26
                    },
                    {
                        "item_id": "P004051",
                        "amount": 1
                    },
                    {
                        "item_id": "P005026",
                        "amount": 29
                    },
                    {
                        "item_id": "P000726",
                        "amount": 22
                    },
                    {
                        "item_id": "P008107",
                        "amount": 47
                    },
                    {
                        "item_id": "P001598",
                        "amount": 32
                    },
                    {
                        "item_id": "P002855",
                        "amount": 20
                    },
                    {
                        "item_id": "P010404",
                        "amount": 30
                    },
                    {
                        "item_id": "P010446",
                        "amount": 6
                    },
                    {
                        "item_id": "P001517",
                        "amount": 9
                    },
                    {
                        "item_id": "P009265",
                        "amount": 2
                    },
                    {
                        "item_id": "P001108",
                        "amount": 20
                    },
                    {
                        "item_id": "P009110",
                        "amount": 18
                    },
                    {
                        "item_id": "P009686",
                        "amount": 13
                    }
                ]
            },
            {
                "id": 2,
                "order_id": 2,
                "source_id": 9,
                "order_date": "1983-11-28",
                "request_date": "1983-11-30",
                "shipment_date": "1983-12-02",
                "shipment_type": "I",
                "shipment_status": "Transit",
                "notes": "Wit duur fijn vlieg.",
                "carrier_code": "PostNL",
                "carrier_description": "Royal Dutch Post and Parcel Service",
                "service_code": "TwoDay",
                "payment_type": "Automatic",
                "transfer_mode": "Ground",
                "total_package_count": 56,
                "total_package_weight": 42.25,
                "created_at": "1983-11-29T11:12:17Z",
                "updated_at": "1983-11-30T13:12:17Z",
                "items": [
                    {
                        "item_id": "P003790",
                        "amount": 10
                    },
                    {
                        "item_id": "P007369",
                        "amount": 15
                    },
                    {
                        "item_id": "P007311",
                        "amount": 21
                    },
                    {
                        "item_id": "P004140",
                        "amount": 8
                    },
                    {
                        "item_id": "P004413",
                        "amount": 46
                    },
                    {
                        "item_id": "P004717",
                        "amount": 38
                    },
                    {
                        "item_id": "P001919",
                        "amount": 13
                    },
                    {
                        "item_id": "P010075",
                        "amount": 5
                    },
                    {
                        "item_id": "P006603",
                        "amount": 48
                    },
                    {
                        "item_id": "P004504",
                        "amount": 30
                    },
                    {
                        "item_id": "P009594",
                        "amount": 35
                    },
                    {
                        "item_id": "P008851",
                        "amount": 25
                    },
                    {
                        "item_id": "P002129",
                        "amount": 46
                    },
                    {
                        "item_id": "P002320",
                        "amount": 4
                    },
                    {
                        "item_id": "P008341",
                        "amount": 23
                    }
                ]
            },
            {
                "id": 3,
                "order_id": 3,
                "source_id": 52,
                "order_date": "1973-01-28",
                "request_date": "1973-01-30",
                "shipment_date": "1973-02-01",
                "shipment_type": "I",
                "shipment_status": "Pending",
                "notes": "Hoog genot springen afspraak mond bus.",
                "carrier_code": "DHL",
                "carrier_description": "DHL Express",
                "service_code": "NextDay",
                "payment_type": "Automatic",
                "transfer_mode": "Ground",
                "total_package_count": 29,
                "total_package_weight": 463.0,
                "created_at": "1973-01-28T20:09:11Z",
                "updated_at": "1973-01-29T22:09:11Z",
                "items": [
                    {
                        "item_id": "P010669",
                        "amount": 16
                    }
                ]
            }
        ], "The shipment database doesn't match the expected data"

    def test_get_shipment_with_id(self):
        shipment2 = self.shipmentObject.get_shipment(2)
        assert shipment2 == {
            "id": 2,
            "order_id": 2,
            "source_id": 9,
            "order_date": "1983-11-28",
            "request_date": "1983-11-30",
            "shipment_date": "1983-12-02",
            "shipment_type": "I",
            "shipment_status": "Transit",
            "notes": "Wit duur fijn vlieg.",
            "carrier_code": "PostNL",
            "carrier_description": "Royal Dutch Post and Parcel Service",
            "service_code": "TwoDay",
            "payment_type": "Automatic",
            "transfer_mode": "Ground",
            "total_package_count": 56,
            "total_package_weight": 42.25,
            "created_at": "1983-11-29T11:12:17Z",
            "updated_at": "1983-11-30T13:12:17Z",
            "items": [
                {
                    "item_id": "P003790",
                    "amount": 10
                },
                {
                    "item_id": "P007369",
                    "amount": 15
                },
                {
                    "item_id": "P007311",
                    "amount": 21
                },
                {
                    "item_id": "P004140",
                    "amount": 8
                },
                {
                    "item_id": "P004413",
                    "amount": 46
                },
                {
                    "item_id": "P004717",
                    "amount": 38
                },
                {
                    "item_id": "P001919",
                    "amount": 13
                },
                {
                    "item_id": "P010075",
                    "amount": 5
                },
                {
                    "item_id": "P006603",
                    "amount": 48
                },
                {
                    "item_id": "P004504",
                    "amount": 30
                },
                {
                    "item_id": "P009594",
                    "amount": 35
                },
                {
                    "item_id": "P008851",
                    "amount": 25
                },
                {
                    "item_id": "P002129",
                    "amount": 46
                },
                {
                    "item_id": "P002320",
                    "amount": 4
                },
                {
                    "item_id": "P008341",
                    "amount": 23
                }
            ]
        }, "The shipment with id 2 wasn't found in the shipment database"

    def test_get_items_in_shipment(self):
        items_in_shipment2 = self.shipmentObject.get_items_in_shipment(2)
        assert items_in_shipment2 == [
            {
                "item_id": "P003790",
                "amount": 10
            },
            {
                "item_id": "P007369",
                "amount": 15
            },
            {
                "item_id": "P007311",
                "amount": 21
            },
            {
                "item_id": "P004140",
                "amount": 8
            },
            {
                "item_id": "P004413",
                "amount": 46
            },
            {
                "item_id": "P004717",
                "amount": 38
            },
            {
                "item_id": "P001919",
                "amount": 13
            },
            {
                "item_id": "P010075",
                "amount": 5
            },
            {
                "item_id": "P006603",
                "amount": 48
            },
            {
                "item_id": "P004504",
                "amount": 30
            },
            {
                "item_id": "P009594",
                "amount": 35
            },
            {
                "item_id": "P008851",
                "amount": 25
            },
            {
                "item_id": "P002129",
                "amount": 46
            },
            {
                "item_id": "P002320",
                "amount": 4
            },
            {
                "item_id": "P008341",
                "amount": 23
            }
        ], "The items inside the shipment with id 2 don't match the expected data"

    def test_add_shipment(self):
        new_shipment = {
            "id": 4,
            "order_id": 2988,
            "source_id": 21,
            "order_date": "2017-05-23",
            "request_date": "2017-05-25",
            "shipment_date": "2017-05-27",
            "shipment_type": "I",
            "shipment_status": "Delivered",
            "notes": "Hoed doen gebied laag steun nat doos.",
            "carrier_code": "TNTexpress",
            "carrier_description": "TNT Express",
            "service_code": "NextDay",
            "payment_type": "Manual",
            "transfer_mode": "Air",
            "total_package_count": 19,
            "total_package_weight": 795.68,
            "created_at": "-",
            "updated_at": "-",
            "items": [
                {
                    "item_id": "P005978",
                    "amount": 15
                },
                {
                    "item_id": "P011465",
                    "amount": 50
                },
                {
                    "item_id": "P000881",
                    "amount": 42
                },
                {
                    "item_id": "P003490",
                    "amount": 37
                },
                {
                    "item_id": "P004389",
                    "amount": 38
                },
                {
                    "item_id": "P009705",
                    "amount": 22
                },
                {
                    "item_id": "P005412",
                    "amount": 3
                },
                {
                    "item_id": "P010205",
                    "amount": 28
                },
                {
                    "item_id": "P005585",
                    "amount": 28
                }
            ]
        }

        self.shipmentObject.add_shipment(new_shipment)
        new_timestamp = self.shipmentObject.get_timestamp()
        new_shipment["created_at"] = new_timestamp
        new_shipment["updated_at"] = new_timestamp

        assert self.shipmentObject.get_shipment(4) == new_shipment, \
            "The new shipment wasn't saved correctly, or get_shipment doesn't function properly"

    def test_update_shipment(self):
        updated_shipment = {
            "id": 4,
            "order_id": 2988,
            "source_id": 21,
            "order_date": "2024-05-23",                # <- Changed
            "request_date": "2024-05-25",              # <- Changed
            "shipment_date": "2017-05-27",
            "shipment_type": "I",
            "shipment_status": "Delivered",
            "notes": "Hoed doen gebied laag steun nat doos.",
            "carrier_code": "TNTexpress",
            "carrier_description": "TNT Express",
            "service_code": "NextDay",
            "payment_type": "Manual",
            "transfer_mode": "Water",                 # <- Changed
            "total_package_count": 19,
            "total_package_weight": 500.68,           # <- Changed
            "created_at": "2017-05-23T14:48:56Z",
            "updated_at": "-",
            "items": [
                {
                    "item_id": "P005978",
                    "amount": 30             # <- Changed
                },
                {
                    "item_id": "P011465",
                    "amount": 50
                },
                {
                    "item_id": "P000881",
                    "amount": 42
                },
                {
                    "item_id": "P003490",
                    "amount": 37
                },
                {
                    "item_id": "P004389",
                    "amount": 40              # <- Changed
                },
                {
                    "item_id": "P009705",
                    "amount": 22
                },
                {
                    "item_id": "P005412",
                    "amount": 3
                },
                {
                    "item_id": "P010266",    # <- Changed
                    "amount": 28
                },
                {
                    "item_id": "P005585",
                    "amount": 28
                }
            ]
        }
        self.shipmentObject.update_shipment(4, updated_shipment)
        new_timestamp = self.shipmentObject.get_timestamp()
        updated_shipment["updated_at"] = new_timestamp

        assert self.shipmentObject.get_shipment(4) == updated_shipment, \
            "The new shipment wasn't updated correctly, or get_shipment doesn't function properly"

    def test_update_items_in_shipment(self):
        updated_shipment_items = [
            {
                "item_id": "P005978",
                "amount": 77             # <- Changed
            },
            {
                "item_id": "P011465",
                "amount": 50
            },
            {
                "item_id": "P000881",
                "amount": 42
            },
            {
                "item_id": "P003490",
                "amount": 37
            },
            {
                "item_id": "P004389",
                "amount": 12              # <- Changed
            },
            {
                "item_id": "P009705",
                "amount": 22
            },
            {
                "item_id": "P005412",
                "amount": 3
            },
            {
                "item_id": "P010266",    # <- Changed
                "amount": 36
            },
            {
                "item_id": "P005678",     # <- Changed
                "amount": 28
            },
            {
                "item_id": "P025678",     # <- Added
                "amount": 12
            }
        ]

        self.shipmentObject.update_items_in_shipment(4, updated_shipment_items)

        assert self.shipmentObject.get_items_in_shipment(4) == updated_shipment_items, \
            "The shipment items haven't been updated correctly, or get_items_in_shipment doesn't function properly"

    def test_remove_shipment(self):

        self.shipmentObject.remove_shipment(4)
        assert self.shipmentObject.get_shipment(4) == None, \
            "Shipment with ID 4 wasn't removed correctly, ore get_shipment doesn't function properly"
