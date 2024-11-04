
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

from models.orders import Orders  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


class Test_Orders():

    orderObject = Orders("Test_Data/test_")
    headers_full = {
        "API_KEY": "a1b2c3d4e5",
        "Content-Type": "application/json"
    }

    newOrder = {
        "id": 0,
        "source_id": 33,
        "order_date": "2019-04-03T11:33:15Z",
        "request_date": "2019-04-07T11:33:15Z",
        "reference": "ORD00001",
        "reference_extra": "Bedreven arm straffen bureau.",
        "order_status": "Delivered",
        "notes": "Voedsel vijf vork heel.",
        "shipping_notes": "Buurman betalen plaats bewolkt.",
        "picking_notes": "Ademen fijn volgorde scherp aardappel op leren.",
        "warehouse_id": 18,
        "ship_to": None,
        "bill_to": None,
        "shipment_id": 1,
        "total_amount": 9905.13,
        "total_discount": 150.77,
        "total_tax": 372.72,
        "total_surcharge": 77.6,
        "created_at": "-",
        "updated_at": "-",
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
    }

    # Order Endpoint Testing (server must be running when testing endpoints)

    def test_post_endpoint(self):

        responsePost = requests.post(
            f"{BASE_URL}/api/v1/orders/", headers=self.headers_full, json=self.newOrder)
        new_timestamp = self.orderObject.get_timestamp()
        self.newOrder["created_at"] = new_timestamp.split('T')[0]
        self.newOrder["updated_at"] = new_timestamp.split('T')[0]
        assert responsePost.status_code == 201

    def test_update_endpoint(self):

        self.newOrder["order_status"] = "Pending"
        self.newOrder["total_tax"] = 400.00
        self.newOrder["items"][0]["amount"] = 40

        responsePut = requests.put(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=self.headers_full, json=self.newOrder)
        self.newOrder["updated_at"] = self.orderObject.get_timestamp().split('T')[
            0]
        assert responsePut.status_code == 200

    def test_get_endpoint(self):

        responseGet = requests.get(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=self.headers_full)
        assert responseGet.status_code == 200

        dict_response = responseGet.json()
        dict_response["created_at"] = dict_response["created_at"].split('T')[0]
        dict_response["updated_at"] = dict_response["updated_at"].split('T')[0]
        assert dict_response == self.newOrder

    def test_delete_endpoint(self):

        responseDelete = requests.delete(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=self.headers_full)
        assert responseDelete.status_code == 200

    def test_endpoint_restriction(self):
        headers_restricted = {
            "API_KEY": "f6g7h8i9j0",
            "Content-Type": "application/json"
        }

        responsePost_restricted = requests.post(
            f"{BASE_URL}/api/v1/orders/", headers=headers_restricted, json=self.newOrder)
        responsePut_restricted = requests.put(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=headers_restricted, json=self.newOrder)
        responseDelete_restricted = requests.delete(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=headers_restricted)
        responseGet_restricted = requests.get(
            f"{BASE_URL}/api/v1/orders/{self.newOrder['id']}", headers=headers_restricted)

        assert responsePost_restricted.status_code == 403
        assert responsePut_restricted.status_code == 403
        assert responseDelete_restricted.status_code == 403
        assert responseGet_restricted.status_code == 200

    # Order Method Testing

    def test_get_orders(self):

        allOrders = self.orderObject.get_orders()
        assert allOrders == [
            {
                "id": 1,
                "source_id": 33,
                "order_date": "2019-04-03T11:33:15Z",
                "request_date": "2019-04-07T11:33:15Z",
                "reference": "ORD00001",
                "reference_extra": "Bedreven arm straffen bureau.",
                "order_status": "Delivered",
                "notes": "Voedsel vijf vork heel.",
                "shipping_notes": "Buurman betalen plaats bewolkt.",
                "picking_notes": "Ademen fijn volgorde scherp aardappel op leren.",
                "warehouse_id": 18,
                "ship_to": 8783,
                "bill_to": 8783,
                "shipment_id": 1,
                "total_amount": 9905.13,
                "total_discount": 150.77,
                "total_tax": 372.72,
                "total_surcharge": 77.6,
                "created_at": "2019-04-03T11:33:15Z",
                "updated_at": "2019-04-05T07:33:15Z",
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
                "source_id": 9,
                "order_date": "1999-07-05T19:31:10Z",
                "request_date": "1999-07-09T19:31:10Z",
                "reference": "ORD00002",
                "reference_extra": "Vergelijken raak geluid beetje altijd.",
                "order_status": "Delivered",
                "notes": "We hobby thee compleet wiel fijn.",
                "shipping_notes": "Nood provincie hier.",
                "picking_notes": "Borstelen dit verf suiker.",
                "warehouse_id": 20,
                "ship_to": 6428,
                "bill_to": 6428,
                "shipment_id": 2,
                "total_amount": 8484.98,
                "total_discount": 214.52,
                "total_tax": 665.09,
                "total_surcharge": 42.12,
                "created_at": "1999-07-05T19:31:10Z",
                "updated_at": "1999-07-07T15:31:10Z",
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
                "source_id": 52,
                "order_date": "1983-09-26T19:06:08Z",
                "request_date": "1983-09-30T19:06:08Z",
                "reference": "ORD00003",
                "reference_extra": "Vergeven kamer goed enkele wiel tussen.",
                "order_status": "Delivered",
                "notes": "Zeil hoeveel onze map sex ding.",
                "shipping_notes": "Ontvangen schoon voorzichtig instrument ster vijver kunnen raam.",
                "picking_notes": "Grof geven politie suiker bodem zuid.",
                "warehouse_id": 11,
                "ship_to": 8783,
                "bill_to": 8783,
                "shipment_id": 2,
                "total_amount": 1156.14,
                "total_discount": 420.45,
                "total_tax": 677.42,
                "total_surcharge": 86.03,
                "created_at": "1983-09-26T19:06:08Z",
                "updated_at": "1983-09-28T15:06:08Z",
                "items": [
                    {
                        "item_id": "P010669",
                        "amount": 16
                    }
                ]
            }
        ], "The order database doesn't match the expected data"

    def test_get_order_with_id(self):
        order2 = self.orderObject.get_order(2)
        assert order2 == {
            "id": 2,
            "source_id": 9,
            "order_date": "1999-07-05T19:31:10Z",
            "request_date": "1999-07-09T19:31:10Z",
            "reference": "ORD00002",
            "reference_extra": "Vergelijken raak geluid beetje altijd.",
            "order_status": "Delivered",
            "notes": "We hobby thee compleet wiel fijn.",
            "shipping_notes": "Nood provincie hier.",
            "picking_notes": "Borstelen dit verf suiker.",
            "warehouse_id": 20,
            "ship_to": 6428,
            "bill_to": 6428,
            "shipment_id": 2,
            "total_amount": 8484.98,
            "total_discount": 214.52,
            "total_tax": 665.09,
            "total_surcharge": 42.12,
            "created_at": "1999-07-05T19:31:10Z",
            "updated_at": "1999-07-07T15:31:10Z",
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
        }, "The order with id 2 wasn't found in the order database"

    def test_get_items_in_order(self):
        items_in_order2 = self.orderObject.get_items_in_order(2)
        assert items_in_order2 == [
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
        ], "The items inside the order with id 2 don't match the expected data"

    def test_get_orders_in_shipment(self):
        orders_in_shipment2 = self.orderObject.get_orders_in_shipment(2)
        assert orders_in_shipment2 == [
            {
                "id": 2,
                "source_id": 9,
                "order_date": "1999-07-05T19:31:10Z",
                "request_date": "1999-07-09T19:31:10Z",
                "reference": "ORD00002",
                "reference_extra": "Vergelijken raak geluid beetje altijd.",
                "order_status": "Delivered",
                "notes": "We hobby thee compleet wiel fijn.",
                "shipping_notes": "Nood provincie hier.",
                "picking_notes": "Borstelen dit verf suiker.",
                "warehouse_id": 20,
                "ship_to": 6428,
                "bill_to": 6428,
                "shipment_id": 2,
                "total_amount": 8484.98,
                "total_discount": 214.52,
                "total_tax": 665.09,
                "total_surcharge": 42.12,
                "created_at": "1999-07-05T19:31:10Z",
                "updated_at": "1999-07-07T15:31:10Z",
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
                "source_id": 52,
                "order_date": "1983-09-26T19:06:08Z",
                "request_date": "1983-09-30T19:06:08Z",
                "reference": "ORD00003",
                "reference_extra": "Vergeven kamer goed enkele wiel tussen.",
                "order_status": "Delivered",
                "notes": "Zeil hoeveel onze map sex ding.",
                "shipping_notes": "Ontvangen schoon voorzichtig instrument ster vijver kunnen raam.",
                "picking_notes": "Grof geven politie suiker bodem zuid.",
                "warehouse_id": 11,
                "ship_to": 8783,
                "bill_to": 8783,
                "shipment_id": 2,
                "total_amount": 1156.14,
                "total_discount": 420.45,
                "total_tax": 677.42,
                "total_surcharge": 86.03,
                "created_at": "1983-09-26T19:06:08Z",
                "updated_at": "1983-09-28T15:06:08Z",
                "items": [
                    {
                        "item_id": "P010669",
                        "amount": 16
                    }
                ]
            }
        ], "The orders within shipment 2 don't match the expected data"

    def test_get_orders_for_client(self):
        orders_for_client8783 = self.orderObject.get_orders_for_client(8783)
        assert orders_for_client8783 == [
            {
                "id": 1,
                "source_id": 33,
                "order_date": "2019-04-03T11:33:15Z",
                "request_date": "2019-04-07T11:33:15Z",
                "reference": "ORD00001",
                "reference_extra": "Bedreven arm straffen bureau.",
                "order_status": "Delivered",
                "notes": "Voedsel vijf vork heel.",
                "shipping_notes": "Buurman betalen plaats bewolkt.",
                "picking_notes": "Ademen fijn volgorde scherp aardappel op leren.",
                "warehouse_id": 18,
                "ship_to": 8783,
                "bill_to": 8783,
                "shipment_id": 1,
                "total_amount": 9905.13,
                "total_discount": 150.77,
                "total_tax": 372.72,
                "total_surcharge": 77.6,
                "created_at": "2019-04-03T11:33:15Z",
                "updated_at": "2019-04-05T07:33:15Z",
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
                "id": 3,
                "source_id": 52,
                "order_date": "1983-09-26T19:06:08Z",
                "request_date": "1983-09-30T19:06:08Z",
                "reference": "ORD00003",
                "reference_extra": "Vergeven kamer goed enkele wiel tussen.",
                "order_status": "Delivered",
                "notes": "Zeil hoeveel onze map sex ding.",
                "shipping_notes": "Ontvangen schoon voorzichtig instrument ster vijver kunnen raam.",
                "picking_notes": "Grof geven politie suiker bodem zuid.",
                "warehouse_id": 11,
                "ship_to": 8783,
                "bill_to": 8783,
                "shipment_id": 2,
                "total_amount": 1156.14,
                "total_discount": 420.45,
                "total_tax": 677.42,
                "total_surcharge": 86.03,
                "created_at": "1983-09-26T19:06:08Z",
                "updated_at": "1983-09-28T15:06:08Z",
                "items": [
                    {
                        "item_id": "P010669",
                        "amount": 16
                    }
                ]
            }
        ], "The orders for client 8783 don't match the expected data"

    def test_add_order(self):
        new_order = {
            "id": 4,
            "source_id": 11,
            "order_date": "2001-10-20T12:03:23Z",
            "request_date": "2001-10-24T12:03:23Z",
            "reference": "ORD05399",
            "reference_extra": "Begrijpen lopen trein verliezen bloem branden land.",
            "order_status": "Delivered",
            "notes": "Lang liegen succes geen papa.",
            "shipping_notes": "Nacht hart oceaan spel wanneer.",
            "picking_notes": "Huren tijd angst ijs.",
            "warehouse_id": 45,
            "ship_to": None,
            "bill_to": None,
            "shipment_id": 5399,
            "total_amount": 9785.31,
            "total_discount": 432.25,
            "total_tax": 964.0,
            "total_surcharge": 64.0,
            "created_at": "-",
            "updated_at": "-",
            "items": [
                {
                    "item_id": "P004263",
                    "amount": 38
                },
                {
                    "item_id": "P003874",
                    "amount": 35
                },
                {
                    "item_id": "P003503",
                    "amount": 38
                }
            ]
        }

        self.orderObject.add_order(new_order)
        new_timestamp = self.orderObject.get_timestamp()
        new_order["created_at"] = new_timestamp
        new_order["updated_at"] = new_timestamp

        assert self.orderObject.get_order(4) == new_order, \
            "The new order wasn't saved correctly, or get_order doesn't function properly"

    def test_update_order(self):
        updated_order = {
            "id": 4,
            "source_id": 12,                                    # <- Changed
            "order_date": "2001-10-20T12:03:23Z",
            "request_date": "2001-10-24T12:03:23Z",
            "reference": "ORD05400",                            # <- Changed
            "reference_extra": "Begrijpen lopen trein verliezen bloem branden land.",
            "order_status": "Pending",                          # <- Changed
            "notes": "Lang liegen succes geen papa.",
            "shipping_notes": "Nacht hart oceaan spel wanneer.",
            "picking_notes": "Huren tijd angst ijs.",
            "warehouse_id": 50,                                 # <- Changed
            "ship_to": None,
            "bill_to": None,
            "shipment_id": 5399,
            "total_amount": 4323.31,                            # <- Changed
            "total_discount": 432.25,
            "total_tax": 964.0,
            "total_surcharge": 55.0,                            # <- Changed
            "created_at": "2001-10-20T12:03:23Z",
            "updated_at": "-",
            "items": [
                {
                    "item_id": "P004263",
                    "amount": 38
                },
                {
                    "item_id": "P003874",
                    "amount": 1                                 # <- Changed
                },
                {
                    "item_id": "P003603",                       # <- Changed
                    "amount": 38
                }
            ]
        }
        self.orderObject.update_order(4, updated_order)
        new_timestamp = self.orderObject.get_timestamp()
        updated_order["updated_at"] = new_timestamp

        assert self.orderObject.get_order(4) == updated_order, \
            "The new order wasn't updated correctly, or get_order doesn't function properly"

    def test_update_items_in_order(self):
        updated_order_items = [
            {
                "item_id": "P004263",
                "amount": 38
            },
            {
                "item_id": "P003874",
                "amount": 7771111                                # <- Changed
            },
            {
                "item_id": "P001603",                       # <- Changed
                "amount": 38
            },
            {
                "item_id": "P013603",                       # <- Added
                "amount": 12
            },

        ]

        self.orderObject.update_items_in_order(4, updated_order_items)

        assert self.orderObject.get_items_in_order(4) == updated_order_items, \
            "The order items haven't been updated correctly, or get_items_in_order doesn't function properly"

    # def test_orders_in_shipment(self):

    def test_remove_order(self):

        self.orderObject.remove_order(4)
        assert self.orderObject.get_order(4) == None, \
            "Order with ID 4 wasn't removed correctly, ore get_order doesn't function properly"
