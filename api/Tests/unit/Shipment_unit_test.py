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

from models.shipments import Shipments  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder

class Test_Shipments():

    shipmentObject = Shipments("../Test_Data/Cargohub_Test.db")

       # Shipment Method Testing

    # def test_get_shipments(self):

    #     allShipments = self.shipmentObject.get_shipments()
    #     assert allShipments == [
    #         {
    #             "id": 1,
    #             "order_id": 1,
    #             "source_id": 33,
    #             "order_date": "2000-03-09",
    #             "request_date": "2000-03-11",
    #             "shipment_date": "2000-03-13",
    #             "shipment_type": "I",
    #             "shipment_status": "Pending",
    #             "notes": "Zee vertrouwen klas rots heet lachen oneven begrijpen.",
    #             "carrier_code": "DPD",
    #             "carrier_description": "Dynamic Parcel Distribution",
    #             "service_code": "Fastest",
    #             "payment_type": "Manual",
    #             "transfer_mode": "Ground",
    #             "total_package_count": 31,
    #             "total_package_weight": 594.42,
    #             "created_at": "2000-03-10T11:11:14Z",
    #             "updated_at": "2000-03-11T13:11:14Z",
    #             "items": [
    #                 {
    #                     "item_id": "P007435",
    #                     "amount": 23
    #                 },
    #                 {
    #                     "item_id": "P009557",
    #                     "amount": 1
    #                 },
    #                 {
    #                     "item_id": "P009553",
    #                     "amount": 50
    #                 },
    #                 {
    #                     "item_id": "P010015",
    #                     "amount": 16
    #                 },
    #                 {
    #                     "item_id": "P002084",
    #                     "amount": 33
    #                 },
    #                 {
    #                     "item_id": "P009663",
    #                     "amount": 18
    #                 },
    #                 {
    #                     "item_id": "P010125",
    #                     "amount": 18
    #                 },
    #                 {
    #                     "item_id": "P005768",
    #                     "amount": 26
    #                 },
    #                 {
    #                     "item_id": "P004051",
    #                     "amount": 1
    #                 },
    #                 {
    #                     "item_id": "P005026",
    #                     "amount": 29
    #                 },
    #                 {
    #                     "item_id": "P000726",
    #                     "amount": 22
    #                 },
    #                 {
    #                     "item_id": "P008107",
    #                     "amount": 47
    #                 },
    #                 {
    #                     "item_id": "P001598",
    #                     "amount": 32
    #                 },
    #                 {
    #                     "item_id": "P002855",
    #                     "amount": 20
    #                 },
    #                 {
    #                     "item_id": "P010404",
    #                     "amount": 30
    #                 },
    #                 {
    #                     "item_id": "P010446",
    #                     "amount": 6
    #                 },
    #                 {
    #                     "item_id": "P001517",
    #                     "amount": 9
    #                 },
    #                 {
    #                     "item_id": "P009265",
    #                     "amount": 2
    #                 },
    #                 {
    #                     "item_id": "P001108",
    #                     "amount": 20
    #                 },
    #                 {
    #                     "item_id": "P009110",
    #                     "amount": 18
    #                 },
    #                 {
    #                     "item_id": "P009686",
    #                     "amount": 13
    #                 }
    #             ]
    #         },
    #         {
    #             "id": 2,
    #             "order_id": 2,
    #             "source_id": 9,
    #             "order_date": "1983-11-28",
    #             "request_date": "1983-11-30",
    #             "shipment_date": "1983-12-02",
    #             "shipment_type": "I",
    #             "shipment_status": "Transit",
    #             "notes": "Wit duur fijn vlieg.",
    #             "carrier_code": "PostNL",
    #             "carrier_description": "Royal Dutch Post and Parcel Service",
    #             "service_code": "TwoDay",
    #             "payment_type": "Automatic",
    #             "transfer_mode": "Ground",
    #             "total_package_count": 56,
    #             "total_package_weight": 42.25,
    #             "created_at": "1983-11-29T11:12:17Z",
    #             "updated_at": "1983-11-30T13:12:17Z",
    #             "items": [
    #                 {
    #                     "item_id": "P003790",
    #                     "amount": 10
    #                 },
    #                 {
    #                     "item_id": "P007369",
    #                     "amount": 15
    #                 },
    #                 {
    #                     "item_id": "P007311",
    #                     "amount": 21
    #                 },
    #                 {
    #                     "item_id": "P004140",
    #                     "amount": 8
    #                 },
    #                 {
    #                     "item_id": "P004413",
    #                     "amount": 46
    #                 },
    #                 {
    #                     "item_id": "P004717",
    #                     "amount": 38
    #                 },
    #                 {
    #                     "item_id": "P001919",
    #                     "amount": 13
    #                 },
    #                 {
    #                     "item_id": "P010075",
    #                     "amount": 5
    #                 },
    #                 {
    #                     "item_id": "P006603",
    #                     "amount": 48
    #                 },
    #                 {
    #                     "item_id": "P004504",
    #                     "amount": 30
    #                 },
    #                 {
    #                     "item_id": "P009594",
    #                     "amount": 35
    #                 },
    #                 {
    #                     "item_id": "P008851",
    #                     "amount": 25
    #                 },
    #                 {
    #                     "item_id": "P002129",
    #                     "amount": 46
    #                 },
    #                 {
    #                     "item_id": "P002320",
    #                     "amount": 4
    #                 },
    #                 {
    #                     "item_id": "P008341",
    #                     "amount": 23
    #                 }
    #             ]
    #         },
    #         {
    #             "id": 3,
    #             "order_id": 3,
    #             "source_id": 52,
    #             "order_date": "1973-01-28",
    #             "request_date": "1973-01-30",
    #             "shipment_date": "1973-02-01",
    #             "shipment_type": "I",
    #             "shipment_status": "Pending",
    #             "notes": "Hoog genot springen afspraak mond bus.",
    #             "carrier_code": "DHL",
    #             "carrier_description": "DHL Express",
    #             "service_code": "NextDay",
    #             "payment_type": "Automatic",
    #             "transfer_mode": "Ground",
    #             "total_package_count": 29,
    #             "total_package_weight": 463.0,
    #             "created_at": "1973-01-28T20:09:11Z",
    #             "updated_at": "1973-01-29T22:09:11Z",
    #             "items": [
    #                 {
    #                     "item_id": "P010669",
    #                     "amount": 16
    #                 }
    #             ]
    #         }
    #     ], "The shipment database doesn't match the expected data"

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
            "id": 10103,
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

        saved_shipment = self.shipmentObject.get_shipment(10103)
        saved_shipment.pop("created_at", None)
        saved_shipment.pop("updated_at", None)
        new_shipment.pop("created_at", None)
        new_shipment.pop("updated_at", None)

        assert saved_shipment == new_shipment, \
            "The new shipment wasn't saved correctly, or get_shipment doesn't function properly"

    def test_update_shipment(self):
        updated_shipment = {
            "id": 10103,
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
        self.shipmentObject.update_shipment(10103, updated_shipment)
        new_timestamp = self.shipmentObject.get_timestamp()
        updated_shipment["updated_at"] = new_timestamp

        saved_shipment = self.shipmentObject.get_shipment(10103)
        saved_shipment.pop("created_at", None)
        saved_shipment.pop("updated_at", None)
        updated_shipment.pop("created_at", None)
        updated_shipment.pop("updated_at", None)

        assert saved_shipment == updated_shipment, \
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

        self.shipmentObject.update_items_in_shipment(10103, updated_shipment_items)

        saved_items = self.shipmentObject.get_items_in_shipment(10103)
        for item in saved_items:
            item.pop("created_at", None)
            item.pop("updated_at", None)
        for item in updated_shipment_items:
            item.pop("created_at", None)
            item.pop("updated_at", None)

        assert saved_items == updated_shipment_items, \
            "The shipment items haven't been updated correctly, or get_items_in_shipment doesn't function properly"

    def test_remove_shipment(self):
        # Assert that the Supplier exists before removal
        assert self.shipmentObject.get_shipment(10103) is not None, \
            "Supplier with ID 10103 does not exist before removal"

        self.shipmentObject.remove_shipment(10103)
        assert self.shipmentObject.get_shipment(10103) == None, \
            "Shipment with ID 10103 wasn't removed correctly, ore get_shipment doesn't function properly"