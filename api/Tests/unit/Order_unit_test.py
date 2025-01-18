
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

from models.orders import Orders  # noqa

BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

# Must run in test folder


class Test_Orders():

    orderObject = Orders("../Test_Data/Cargohub_Test.db")
    # Order Method Testing

    # def test_get_orders(self):

    #     allOrders = self.orderObject.get_orders()
    #     assert allOrders == [
    #         {
    #             "id": 1,
    #             "source_id": 33,
    #             "order_date": "2019-04-03T11:33:15Z",
    #             "request_date": "2019-04-07T11:33:15Z",
    #             "reference": "ORD00001",
    #             "reference_extra": "Bedreven arm straffen bureau.",
    #             "order_status": "Delivered",
    #             "notes": "Voedsel vijf vork heel.",
    #             "shipping_notes": "Buurman betalen plaats bewolkt.",
    #             "picking_notes": "Ademen fijn volgorde scherp aardappel op leren.",
    #             "warehouse_id": 18,
    #             "ship_to": 8783,
    #             "bill_to": 8783,
    #             "shipment_id": 1,
    #             "total_amount": 9905.13,
    #             "total_discount": 150.77,
    #             "total_tax": 372.72,
    #             "total_surcharge": 77.6,
    #             "created_at": "2019-04-03T11:33:15Z",
    #             "updated_at": "2019-04-05T07:33:15Z",
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
    #             "source_id": 9,
    #             "order_date": "1999-07-05T19:31:10Z",
    #             "request_date": "1999-07-09T19:31:10Z",
    #             "reference": "ORD00002",
    #             "reference_extra": "Vergelijken raak geluid beetje altijd.",
    #             "order_status": "Delivered",
    #             "notes": "We hobby thee compleet wiel fijn.",
    #             "shipping_notes": "Nood provincie hier.",
    #             "picking_notes": "Borstelen dit verf suiker.",
    #             "warehouse_id": 20,
    #             "ship_to": 6428,
    #             "bill_to": 6428,
    #             "shipment_id": 2,
    #             "total_amount": 8484.98,
    #             "total_discount": 214.52,
    #             "total_tax": 665.09,
    #             "total_surcharge": 42.12,
    #             "created_at": "1999-07-05T19:31:10Z",
    #             "updated_at": "1999-07-07T15:31:10Z",
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
    #             "source_id": 52,
    #             "order_date": "1983-09-26T19:06:08Z",
    #             "request_date": "1983-09-30T19:06:08Z",
    #             "reference": "ORD00003",
    #             "reference_extra": "Vergeven kamer goed enkele wiel tussen.",
    #             "order_status": "Delivered",
    #             "notes": "Zeil hoeveel onze map sex ding.",
    #             "shipping_notes": "Ontvangen schoon voorzichtig instrument ster vijver kunnen raam.",
    #             "picking_notes": "Grof geven politie suiker bodem zuid.",
    #             "warehouse_id": 11,
    #             "ship_to": 8783,
    #             "bill_to": 8783,
    #             "shipment_id": 2,
    #             "total_amount": 1156.14,
    #             "total_discount": 420.45,
    #             "total_tax": 677.42,
    #             "total_surcharge": 86.03,
    #             "created_at": "1983-09-26T19:06:08Z",
    #             "updated_at": "1983-09-28T15:06:08Z",
    #             "items": [
    #                 {
    #                     "item_id": "P010669",
    #                     "amount": 16
    #                 }
    #             ]
    #         }
    #     ], "The order database doesn't match the expected data"

    def test_get_order_with_id(self):
        order2 = self.orderObject.get_order(2)
        expected_order = {
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
            "ship_to": None,
            "bill_to": None,
            "shipment_id": 2,
            "total_amount": 8484.98,
            "total_discount": 214.52,
            "total_tax": 665.09,
            "total_surcharge": 42.12,
            "created_at": "1999-07-05T19:31:10Z",
            "updated_at": "1999-07-07T15:31:10Z",
            "items": [
                {"item_id": "P003790", "amount": 10},
                {"item_id": "P007369", "amount": 15},
                {"item_id": "P007311", "amount": 21},
                {"item_id": "P004140", "amount": 8},
                {"item_id": "P004413", "amount": 46},
                {"item_id": "P004717", "amount": 38},
                {"item_id": "P001919", "amount": 13},
                {"item_id": "P010075", "amount": 5},
                {"item_id": "P006603", "amount": 48},
                {"item_id": "P004504", "amount": 30},
                {"item_id": "P009594", "amount": 35},
                {"item_id": "P008851", "amount": 25},
                {"item_id": "P002129", "amount": 46},
                {"item_id": "P002320", "amount": 4},
                {"item_id": "P008341", "amount": 23}
            ]
        }
        assert order2 == expected_order, "The order with id 2 wasn't found in the order database"

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
        orders_in_shipment2 = self.orderObject.get_orders_in_shipment(1)
        assert orders_in_shipment2 == [
            1], "The orders within shipment 2 don't match the expected data"

    def test_get_orders_for_client(self):
        orders_for_client8783 = self.orderObject.get_orders_for_client(1)
        expected_orders = [
            {
                "id": 9325,
                "source_id": 32,
                "order_date": "2003-12-27T08:47:45Z",
                "request_date": "2003-12-31T08:47:45Z",
                "reference": "ORD02467",
                "reference_extra": "Oceaan lot bibliotheek stad zon baby reeds belangrijk.",
                "order_status": "Shipped",
                "notes": "Knie tellen drinken jas mond.",
                "shipping_notes": "Dichtbij jas geit dun mensen branden af mand.",
                "picking_notes": "Pijn alleen start kaart dapper tamelijk.",
                "warehouse_id": 21,
                "ship_to": "1",
                "bill_to": "1",
                "shipment_id": 8086,
                "total_amount": 5153.45,
                "total_discount": 195.06,
                "total_tax": 130.96,
                "total_surcharge": 66.05,
                "created_at": "2003-12-27T08:47:45Z",
                "updated_at": "2003-12-29T04:47:45Z",
                "items": [
                    {
                        "item_id": "P002181",
                        "amount": 33
                    },
                    {
                        "item_id": "P004732",
                        "amount": 21
                    },
                    {
                        "item_id": "P007613",
                        "amount": 7
                    },
                    {
                        "item_id": "P000060",
                        "amount": 3
                    },
                    {
                        "item_id": "P004959",
                        "amount": 7
                    },
                    {
                        "item_id": "P004394",
                        "amount": 47
                    },
                    {
                        "item_id": "P000832",
                        "amount": 2
                    },
                    {
                        "item_id": "P005823",
                        "amount": 49
                    },
                    {
                        "item_id": "P006835",
                        "amount": 13
                    },
                    {
                        "item_id": "P003474",
                        "amount": 20
                    }
                ]
            }
        ]
        assert orders_for_client8783 == expected_orders

    def test_add_order(self):
        new_order = {
            "id": 15000,
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
            "shipment_id": 1,
            "total_amount": 9785.31,
            "total_discount": 432.25,
            "total_tax": 964.0,
            "total_surcharge": 64.0,
            "created_at": "-",
            "updated_at": "-",
            "items": [
                {"item_id": "P004263", "amount": 38},
                {"item_id": "P003874", "amount": 35},
                {"item_id": "P003503", "amount": 38}
            ]
        }

        self.orderObject.add_order(new_order)
        new_timestamp = self.orderObject.get_timestamp()
        new_order["created_at"] = new_timestamp
        new_order["updated_at"] = new_timestamp

        # Add items to the order_items table
        self.orderObject.update_items_in_order(
            new_order["id"], new_order["items"])

        get_order = self.orderObject.get_order(15000)
        # Remove the created_at and updated_at fields for comparison
        new_order.pop("created_at", None)
        new_order.pop("updated_at", None)
        get_order.pop("created_at", None)
        get_order.pop("updated_at", None)

        assert get_order == new_order, \
            "The new order wasn't saved correctly, or get_order doesn't function properly"

    def test_update_order(self):
        updated_order = {
            "id": 15000,
            "source_id": 12,
            "order_date": "2001-10-20T12:03:23Z",
            "request_date": "2001-10-24T12:03:23Z",
            "reference": "ORD05400",
            "reference_extra": "Begrijpen lopen trein verliezen bloem branden land.",
            "order_status": "Pending",
            "notes": "Lang liegen succes geen papa.",
            "shipping_notes": "Nacht hart oceaan spel wanneer.",
            "picking_notes": "Huren tijd angst ijs.",
            "warehouse_id": 50,
            "ship_to": None,
            "bill_to": None,
            "shipment_id": 1,
            "total_amount": 4323.31,
            "total_discount": 432.25,
            "total_tax": 964.0,
            "total_surcharge": 55.0,
            "items": [
                {"item_id": "P004263", "amount": 38},
                {"item_id": "P003874", "amount": 1},
                {"item_id": "P003603", "amount": 38}
            ]
        }

        # Update the order
        self.orderObject.update_order(15000, updated_order)

        # Get the updated order
        get_order = self.orderObject.get_order(15000)

        # Add updated_at timestamp for comparison
        updated_order["updated_at"] = get_order["updated_at"]

        # Validate order items separately
        assert get_order["items"] == updated_order["items"], "Order items were not updated correctly"

        # Remove created_at for full comparison
        updated_order.pop("created_at", None)
        get_order.pop("created_at", None)

        # Validate the entire order
        assert get_order == updated_order, "The order update was not applied correctly"

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
            }
        ]

        self.orderObject.update_items_in_order(15000, updated_order_items)

        assert self.orderObject.get_items_in_order(15000) == updated_order_items, \
            "The order items haven't been updated correctly, or get_items_in_order doesn't function properly"

    def test_update_orders_in_shipment(self):
        updated_shipment_orders = [1, 4]

        self.orderObject.update_orders_in_shipment(
            15000, updated_shipment_orders)

        assert self.orderObject.get_orders_in_shipment(15000) == updated_shipment_orders, \
            "The orders in this shipment haven't been updated correctly, or get_orders_in_shipment doesn't function properly"

        self.orderObject.update_orders_in_shipment(1, [1])
        self.orderObject.update_orders_in_shipment(4, [4])

    def test_remove_order(self):

        self.orderObject.remove_order(15000)
        assert self.orderObject.get_order(
            15000) == None, "Order with ID 4 wasn't removed correctly, ore get_order doesn't function properly"
