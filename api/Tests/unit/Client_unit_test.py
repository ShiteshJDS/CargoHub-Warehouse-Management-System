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
os.path.join(os.path.dirname(__file__), '..', '..')))
from models.clients import Clients



BASE_URL = "http://localhost:3000"  # Replace with your API's base URL

class Test_Clients():

    ClientsObject = Clients("../Test_Data/Cargohub_Test.db")

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
