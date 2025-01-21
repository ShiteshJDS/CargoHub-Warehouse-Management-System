from models.warehouses import Warehouses
from models.locations import Locations
from models.transfers import Transfers
from models.items import Items
from models.item_lines import ItemLines
from models.item_groups import ItemGroups
from models.item_types import ItemTypes
from models.inventories import Inventories
from models.suppliers import Suppliers
from models.orders import Orders
from models.clients import Clients
from models.shipments import Shipments

DEBUG = False

ROOT_PATH = "./data/"

_warehouses = None
_locations = None
_transfers = None
_items = None
_item_lines = None
_item_groups = None
_item_types = None
_inventories = None
_suppliers = None
_orders = None
_shipments = None
_clients = None


def init(db_path):
    global _clients, _warehouses, _locations, _transfers, _items, _item_lines, _item_groups, _item_types, _inventories, _suppliers, _orders, _shipments
    _clients = Clients(db_path)
    _warehouses = Warehouses(db_path)
    _locations = Locations(db_path)
    _transfers = Transfers(db_path)
    _items = Items(db_path)
    _item_lines = ItemLines(db_path)
    _item_groups = ItemGroups(db_path)
    _item_types = ItemTypes(db_path)
    _inventories = Inventories(db_path)
    _suppliers = Suppliers(db_path)
    _orders = Orders(db_path)
    _shipments = Shipments(db_path)


def fetch_warehouse_pool():
    return _warehouses


def fetch_location_pool():
    return _locations


def fetch_transfer_pool():
    return _transfers


def fetch_item_pool():
    return _items


def fetch_item_line_pool():
    return _item_lines


def fetch_item_group_pool():
    return _item_groups


def fetch_item_type_pool():
    return _item_types


def fetch_inventory_pool():
    return _inventories


def fetch_supplier_pool():
    return _suppliers


def fetch_order_pool():
    return _orders


def fetch_client_pool():
    return _clients


def fetch_shipment_pool():
    return _shipments
