import socketserver
import http.server
import json
import logging
import os
from time import sleep

from providers import auth_provider
from providers import data_provider

from processors import notification_processor
import cargohub_db

# Configure logging
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ApiRequestHandler(http.server.BaseHTTPRequestHandler):

    def set_db_path(self):
        """Sets the database path based on the port number."""
        port = self.server.server_address[1]
        if port == 3001:
            self.db_path = "data/Cargohub_3001.db"
        elif port == 3000:
            self.db_path = "data/Cargohub.db"
        else:
            raise ValueError("Unsupported port number")
        data_provider.init(self.db_path)

    def log_request(self, user):
        """Logs details of the incoming request."""
        api_key = self.headers.get("API_KEY")
        request_info = {
            "method": self.command,
            "path": self.path,
            "api_key": api_key,
            "user": user,
            "headers": dict(self.headers),
        }
        logging.info(f"Request: {json.dumps(request_info)}")

    def is_valid_path_end(self, path_end):
        valid_endings = {
            "clients", "orders", "inventories", "item_groups", "items", "item_lines",
            "item_types", "inventory", "totals", "locations", "shipments", "commit",
            "suppliers", "transfers", "warehouses"
        }
        return path_end.isdigit() or path_end.startswith("P") and path_end[1:].isdigit() or path_end in valid_endings

    def handle_get_version_1(self, path, user):
        if not auth_provider.has_access(user, path, "get"):
            self.send_response(403)
            self.end_headers()
            return
        if not self.is_valid_path_end(path[-1]):
            self.send_response(400)
            self.end_headers()
            return
        if path[0] == "warehouses":
            paths = len(path)
            match paths:
                case 1:
                    warehouses = data_provider.fetch_warehouse_pool().get_warehouses()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(warehouses).encode("utf-8"))
                case 2:
                    warehouse_id = int(path[1])
                    warehouse = data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id)
                    if warehouse:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(warehouse).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "locations":
                        warehouse_id = int(path[1])
                        locations = data_provider.fetch_location_pool().get_locations_in_warehouse(warehouse_id)
                        if locations:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(locations).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "locations":
            paths = len(path)
            match paths:
                case 1:
                    locations = data_provider.fetch_location_pool().get_locations()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(locations).encode("utf-8"))
                case 2:
                    location_id = int(path[1])
                    location = data_provider.fetch_location_pool().get_location(location_id)
                    if location:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(location).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "transfers":
            paths = len(path)
            match paths:
                case 1:
                    transfers = data_provider.fetch_transfer_pool().get_transfers()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(transfers).encode("utf-8"))
                case 2:
                    transfer_id = int(path[1])
                    transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
                    if transfer:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(transfer).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "items":
                        transfer_id = int(path[1])
                        items = data_provider.fetch_transfer_pool().get_items_in_transfer(transfer_id)
                        if items:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(items).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "items":
            paths = len(path)
            match paths:
                case 1:
                    items = data_provider.fetch_item_pool().get_items()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(items).encode("utf-8"))
                case 2:
                    item_id = path[1]
                    item = data_provider.fetch_item_pool().get_item(item_id)
                    if item:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(item).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "inventory":
                        item_id = path[1]
                        inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(item_id)
                        if inventories:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(inventories).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 4:
                    if path[2] == "inventory" and path[3] == "totals":
                        item_id = path[1]
                        totals = data_provider.fetch_inventory_pool().get_inventory_totals_for_item(item_id)
                        if totals:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(totals).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "item_lines":
            paths = len(path)
            match paths:
                case 1:
                    item_lines = data_provider.fetch_item_line_pool().get_item_lines()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_lines).encode("utf-8"))
                case 2:
                    item_line_id = int(path[1])
                    item_line = data_provider.fetch_item_line_pool().get_item_line(item_line_id)
                    if item_line:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(item_line).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "items":
                        item_line_id = int(path[1])
                        items = data_provider.fetch_item_pool().get_items_for_item_line(item_line_id)
                        if items:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(items).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "item_groups":
            paths = len(path)
            match paths:
                case 1:
                    item_groups = data_provider.fetch_item_group_pool().get_item_groups()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_groups).encode("utf-8"))
                case 2:
                    item_group_id = int(path[1])
                    item_group = data_provider.fetch_item_group_pool().get_item_group(item_group_id)
                    if item_group:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(item_group).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "items":
                        item_group_id = int(path[1])
                        items = data_provider.fetch_item_pool().get_items_for_item_group(item_group_id)
                        if items:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(items).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "item_types":
            paths = len(path)
            match paths:
                case 1:
                    item_types = data_provider.fetch_item_type_pool().get_item_types()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(item_types).encode("utf-8"))
                case 2:
                    item_type_id = int(path[1])
                    item_type = data_provider.fetch_item_type_pool().get_item_type(item_type_id)
                    if item_type:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(item_type).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "items":
                        item_type_id = int(path[1])
                        items = data_provider.fetch_item_pool().get_items_for_item_type(item_type_id)
                        if items:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(items).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "inventories":
            paths = len(path)
            match paths:
                case 1:
                    inventories = data_provider.fetch_inventory_pool().get_inventories()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(inventories).encode("utf-8"))
                case 2:
                    inventory_id = int(path[1])
                    inventory = data_provider.fetch_inventory_pool().get_inventory(inventory_id)
                    if inventory:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(inventory).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "suppliers":
            paths = len(path)
            match paths:
                case 1:
                    suppliers = data_provider.fetch_supplier_pool().get_suppliers()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(suppliers).encode("utf-8"))
                case 2:
                    supplier_id = int(path[1])
                    supplier = data_provider.fetch_supplier_pool().get_supplier(supplier_id)
                    if supplier:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(supplier).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "items":
                        supplier_id = int(path[1])
                        items = data_provider.fetch_item_pool().get_items_for_supplier(supplier_id)
                        if items:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(items).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "orders":
            paths = len(path)
            match paths:
                case 1:
                    orders = data_provider.fetch_order_pool().get_orders()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(orders).encode("utf-8"))
                case 2:
                    order_id = int(path[1])
                    order = data_provider.fetch_order_pool().get_order(order_id)
                    if order:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(order).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "items":
                        order_id = int(path[1])
                        items = data_provider.fetch_order_pool().get_items_in_order(order_id)
                        if items:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(items).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "clients":
            paths = len(path)
            match paths:
                case 1:
                    clients = data_provider.fetch_client_pool().get_clients()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(clients).encode("utf-8"))
                case 2:
                    client_id = int(path[1])
                    client = data_provider.fetch_client_pool().get_client(client_id)
                    if client:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(client).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "orders":
                        client_id = int(path[1])
                        orders = data_provider.fetch_order_pool().get_orders_for_client(client_id)
                        if orders:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(orders).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "shipments":
            paths = len(path)
            match paths:
                case 1:
                    shipments = data_provider.fetch_shipment_pool().get_shipments()
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(shipments).encode("utf-8"))
                case 2:
                    shipment_id = int(path[1])
                    shipment = data_provider.fetch_shipment_pool().get_shipment(shipment_id)
                    if shipment:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(json.dumps(shipment).encode("utf-8"))
                    else:
                        self.send_response(404)
                        self.end_headers()
                case 3:
                    if path[2] == "orders":
                        shipment_id = int(path[1])
                        orders = data_provider.fetch_order_pool().get_orders_in_shipment(shipment_id)
                        if orders:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(orders).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    elif path[2] == "items":
                        shipment_id = int(path[1])
                        items = data_provider.fetch_shipment_pool().get_items_in_shipment(shipment_id)
                        if items:
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(json.dumps(items).encode("utf-8"))
                        else:
                            self.send_response(404)
                            self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        self.set_db_path()
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        self.log_request(user)
        if user is None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                path = self.path.split("/")
                if len(path) > 3 and path[1] == "api" and path[2] == "v1":
                    self.handle_get_version_1(path[3:], user)
            except Exception:
                self.send_response(500)
                self.end_headers()

    def handle_post_version_1(self, path, user):
        if not auth_provider.has_access(user, path, "post"):
            self.send_response(403)
            self.end_headers()
            return

        if not self.is_valid_path_end(path[-1]):
            self.send_response(400)
            self.end_headers()
            return

        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        try:
            new_data = json.loads(post_data.decode())
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode("utf-8"))
            return

        # Define validation rules for each path
        validation_rules = {
    "warehouses": {
        "id": int,
        "code": str,
        "name": str,
        "address": str,
        "zip": str,
        "city": str,
        "province": str,
        "country": str,
        "contact": dict,  # Contact is a nested object
        "created_at": str,
        "updated_at": str,
    },
    "locations": {
        "id": int,
        "warehouse_id": int,
        "code": str,
        "name": str,
        "created_at": str,
        "updated_at": str,
    },
    "transfers": {
        "id": int,
        "reference": str,
        "transfer_from": (int, type(None)),  # Can be null
        "transfer_to": int,
        "transfer_status": str,
        "created_at": str,
        "updated_at": str,
        "items": list,  # List of item objects
    },
    "items": {
        "uid": str,
        "code": str,
        "name": str,
        "description": str,
        "short_description": str,
        "upc_code": str,
        "model_number": str,
        "commodity_code": str,
        "item_line_id": int,
        "item_group_id": int,
        "item_type_id": int,
        "unit_purchase_quantity": int,
        "unit_order_quantity": int,
        "pack_order_quantity": int,
        "supplier_id": int,
        "supplier_code": str,
        "supplier_part_number": str,
        "created_at": str,
        "updated_at": str,
    },
    "item_lines": {
        "id": int,
        "name": str,
        "description": str,
        "item_id": str,
        "quantity": int,
        "created_at": str,
        "updated_at": str,
    },
    "item_groups": {
        "id": int,
        "name": str,
        "description": str,
        "created_at": str,
        "updated_at": str,
    },
    "item_types": {
        "id": int,
        "name": str,
        "type": str,
        "description": str,
        "created_at": str,
        "updated_at": str,
    },
    "inventories": {
        "id": int,
        "item_id": str,
        "description": str,
        "item_reference": str,
        "locations": list,
        "total_on_hand": int,
        "total_expected": int,
        "total_ordered": int,
        "total_allocated": int,
        "total_available": int,
        "warehouse_id": int,
        "stock": int,
        "created_at": str,
        "updated_at": str,
    },
    "suppliers": {
        "id": int,
        "code": str,
        "name": str,
        "address": str,
        "address_extra": str,
        "city": str,
        "zip_code": str,
        "province": str,
        "country": str,
        "contact_name": str,
        "phonenumber": str,
        "reference": str,
        "created_at": str,
        "updated_at": str,
    },
    "orders": {
        "id": int,
        "source_id": int,
        "client_id": int,
        "order_date": str,
        "request_date": str,
        "reference": str,
        "reference_extra": str,
        "order_status": str,
        "notes": str,
        "shipping_notes": str,
        "picking_notes": str,
        "warehouse_id": int,
        "ship_to": (str, type(None)),  # Can be null
        "bill_to": (str, type(None)),  # Can be null
        "shipment_id": int,
        "total_amount": float,
        "total_discount": float,
        "total_tax": float,
        "total_surcharge": float,
        "created_at": str,
        "updated_at": str,
        "items": list,  # List of item objects
    },
    "clients": {
        "id": int,
        "name": str,
        "address": str,
        "city": str,
        "zip_code": str,
        "province": str,
        "country": str,
        "contact_name": str,
        "contact_phone": str,
        "contact_email": str,
        "created_at": str,
        "updated_at": str,
    },
    "shipments": {
        "id": int,
        "order_id": int,
        "source_id": int,
        "order_date": str,
        "request_date": str,
        "shipment_date": str,
        "shipment_type": str,
        "shipment_status": str,
        "notes": str,
        "carrier_code": str,
        "carrier_description": str,
        "service_code": str,
        "payment_type": str,
        "transfer_mode": str,
        "total_package_count": int,
        "total_package_weight": float,
        "created_at": str,
        "updated_at": str,
        "items": list,  # List of item objects
    },
}


        # Validate data
        if path[0] in validation_rules:
            required_keys = validation_rules[path[0]]

            # Check for empty values
            empty_values = [key for key, value in new_data.items() if not value and value != 0]
            if empty_values:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Empty values", "keys": empty_values}).encode("utf-8"))
                return
            
            # Check for missing keys
            missing_keys = [key for key in required_keys if key not in new_data]
            if missing_keys:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing keys", "keys": missing_keys}).encode("utf-8"))
                return

            # Check for extra keys
            extra_keys = [key for key in new_data if key not in required_keys]
            if extra_keys:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Extra keys", "keys": extra_keys}).encode("utf-8"))
                return

            # Check for wrong data types
            wrong_types = [key for key, value in new_data.items() if not isinstance(value, required_keys[key])]
            if wrong_types:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Wrong types", "keys": wrong_types}).encode("utf-8"))
                return

        # Process the request based on path
        if path[0] == "warehouses":
            warehouse_id = new_data.get("id")
            if data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_warehouse_pool().add_warehouse(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "locations":
            location_id = new_data.get("id")
            if data_provider.fetch_location_pool().get_location(location_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_location_pool().add_location(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "transfers":
            transfer_id = new_data.get("id")
            if data_provider.fetch_transfer_pool().get_transfer(transfer_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_transfer_pool().add_transfer(new_data)
            notification_processor.push(f"Scheduled batch transfer {new_data['id']}")
            self.send_response(201)
            self.end_headers()
        elif path[0] == "items":
            item_id = new_data.get("uid")
            if data_provider.fetch_item_pool().get_item(item_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_item_pool().add_item(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "item_lines":
            item_line_id = new_data.get("id")
            if data_provider.fetch_item_line_pool().get_item_line(item_line_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_item_line_pool().add_item_line(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "item_groups":
            item_group_id = new_data.get("id")
            if data_provider.fetch_item_group_pool().get_item_group(item_group_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_item_group_pool().add_item_group(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "item_types":
            item_type_id = new_data.get("id")
            if data_provider.fetch_item_type_pool().get_item_type(item_type_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_item_type_pool().add_item_type(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "inventories":
            inventory_id = new_data.get("id")
            if data_provider.fetch_inventory_pool().get_inventory(inventory_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_inventory_pool().add_inventory(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "suppliers":
            supplier_id = new_data.get("id")
            if data_provider.fetch_supplier_pool().get_supplier(supplier_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_supplier_pool().add_supplier(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "orders":
            order_id = new_data.get("id")
            if data_provider.fetch_order_pool().get_order(order_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_order_pool().add_order(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "clients":
            client_id = new_data.get("id")
            if data_provider.fetch_client_pool().get_client(client_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_client_pool().add_client(new_data)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "shipments":
            shipment_id = new_data.get("id")
            if data_provider.fetch_shipment_pool().get_shipment(shipment_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_shipment_pool().add_shipment(new_data)
            self.send_response(201)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


    def do_POST(self):
        self.set_db_path()
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        self.log_request(user)
        if user == None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                path = self.path.split("/")
                if len(path) > 3 and path[1] == "api" and path[2] == "v1":
                    self.handle_post_version_1(path[3:], user)
            except Exception:
                self.send_response(500)
                self.end_headers()

    def handle_put_version_1(self, path, user):
        if not auth_provider.has_access(user, path, "put"):
            self.send_response(403)
            self.end_headers()
            return
        if not self.is_valid_path_end(path[-1]):
            self.send_response(400)
            self.end_headers()
            return
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        try:
            new_data = json.loads(post_data.decode())
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode("utf-8"))
            return

        # Define validation rules for each path
        validation_rules = {
            "warehouses": {
                "id": int,
                "code": str,
                "name": str,
                "address": str,
                "zip": str,
                "city": str,
                "province": str,
                "country": str,
                "contact": dict,  # Contact is a nested object
                "created_at": str,
                "updated_at": str,
            },
            "locations": {
                "id": int,
                "warehouse_id": int,
                "code": str,
                "name": str,
                "created_at": str,
                "updated_at": str,
            },
            "transfers": {
                "id": int,
                "reference": str,
                "transfer_from": (int, type(None)),  # Can be null
                "transfer_to": int,
                "transfer_status": str,
                "created_at": str,
                "updated_at": str,
                "items": list,  # List of item objects
            },
            "items": {
                "uid": str,
                "code": str,
                "name": str,
                "description": str,
                "short_description": str,
                "upc_code": str,
                "model_number": str,
                "commodity_code": str,
                "item_line_id": int,
                "item_group_id": int,
                "item_type_id": int,
                "unit_purchase_quantity": int,
                "unit_order_quantity": int,
                "pack_order_quantity": int,
                "supplier_id": int,
                "supplier_code": str,
                "supplier_part_number": str,
                "created_at": str,
                "updated_at": str,
            },
            "item_lines": {
                "id": int,
                "name": str,
                "description": str,
                "item_id": str,
                "quantity": int,
                "created_at": str,
                "updated_at": str,
            },
            "item_groups": {
                "id": int,
                "name": str,
                "description": str,
                "created_at": str,
                "updated_at": str,
            },
            "item_types": {
                "id": int,
                "name": str,
                "type": str,
                "description": str,
                "created_at": str,
                "updated_at": str,
            },
            "inventories": {
                "id": int,
                "item_id": str,
                "description": str,
                "item_reference": str,
                "locations": list,
                "total_on_hand": int,
                "total_expected": int,
                "total_ordered": int,
                "total_allocated": int,
                "total_available": int,
                "warehouse_id": int,
                "stock": int,
                "created_at": str,
                "updated_at": str,
            },
            "suppliers": {
                "id": int,
                "code": str,
                "name": str,
                "address": str,
                "address_extra": str,
                "city": str,
                "zip_code": str,
                "province": str,
                "country": str,
                "contact_name": str,
                "phonenumber": str,
                "reference": str,
                "created_at": str,
                "updated_at": str,
            },
            "orders": {
                "id": int,
                "source_id": int,
                "client_id": int,
                "order_date": str,
                "request_date": str,
                "reference": str,
                "reference_extra": str,
                "order_status": str,
                "notes": str,
                "shipping_notes": str,
                "picking_notes": str,
                "warehouse_id": int,
                "ship_to": (str, type(None)),  # Can be null
                "bill_to": (str, type(None)),  # Can be null
                "shipment_id": int,
                "total_amount": float,
                "total_discount": float,
                "total_tax": float,
                "total_surcharge": float,
                "created_at": str,
                "updated_at": str,
                "items": list,  # List of item objects
            },
            "clients": {
                "id": int,
                "name": str,
                "address": str,
                "city": str,
                "zip_code": str,
                "province": str,
                "country": str,
                "contact_name": str,
                "contact_phone": str,
                "contact_email": str,
                "created_at": str,
                "updated_at": str,
            },
            "shipments": {
                "id": int,
                "order_id": int,
                "source_id": int,
                "order_date": str,
                "request_date": str,
                "shipment_date": str,
                "shipment_type": str,
                "shipment_status": str,
                "notes": str,
                "carrier_code": str,
                "carrier_description": str,
                "service_code": str,
                "payment_type": str,
                "transfer_mode": str,
                "total_package_count": int,
                "total_package_weight": float,
                "created_at": str,
                "updated_at": str,
                "items": list,  # List of item objects
            },
        }

        # Validate data
        if path[0] in validation_rules:
            required_keys = validation_rules[path[0]]

            # Check for empty values, but allow empty strings for description in item_groups, item_types, and item_lines
            if path[0] in {"item_groups", "item_types", "item_lines"}:
                empty_values = [key for key, value in new_data.items() if not value and value != 0 and key != "description"]
            else:
                empty_values = [key for key, value in new_data.items() if not value and value != 0]

            if empty_values:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Empty values", "keys": empty_values}).encode("utf-8"))
                return

            # Check for missing keys
            missing_keys = [key for key in required_keys if key not in new_data]
            if missing_keys:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing keys", "keys": missing_keys}).encode("utf-8"))
                return

            # Check for extra keys
            extra_keys = [key for key in new_data if key not in required_keys]
            if extra_keys:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Extra keys", "keys": extra_keys}).encode("utf-8"))
                return

            # Check for wrong data types
            wrong_types = [key for key, value in new_data.items() if not isinstance(value, required_keys[key])]
            if wrong_types:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Wrong types", "keys": wrong_types}).encode("utf-8"))
                return

        # Process the request based on path
        if path[0] == "warehouses":
            warehouse_id = int(path[1])
            warehouse = data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id)
            if not warehouse:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_warehouse_pool().update_warehouse(warehouse_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "locations":
            location_id = int(path[1])
            location = data_provider.fetch_location_pool().get_location(location_id)
            if not location:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_location_pool().update_location(location_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "transfers":
            paths = len(path)
            match paths:
                case 2:
                    transfer_id = int(path[1])
                    transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
                    if not transfer:
                        self.send_response(404)
                        self.end_headers()
                        return
                    data_provider.fetch_transfer_pool().update_transfer(transfer_id, new_data)
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if path[2] == "commit":
                        transfer_id = int(path[1])
                        transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
                        if not transfer:
                            self.send_response(404)
                            self.end_headers()
                            return
                        for x in transfer["items"]:
                            inventories = data_provider.fetch_inventory_pool().get_inventories_for_item(x["item_id"])
                            for y in inventories:
                                if y["location_id"] == transfer["transfer_from"]:
                                    y["total_on_hand"] -= x["amount"]
                                    y["total_expected"] = y["total_on_hand"] + y["total_ordered"]
                                    y["total_available"] = y["total_on_hand"] - y["total_allocated"]
                                    data_provider.fetch_inventory_pool().update_inventory(y["id"], y)
                                elif y["location_id"] == transfer["transfer_to"]:
                                    y["total_on_hand"] += x["amount"]
                                    y["total_expected"] = y["total_on_hand"] + y["total_ordered"]
                                    y["total_available"] = y["total_on_hand"] - y["total_allocated"]
                                    data_provider.fetch_inventory_pool().update_inventory(y["id"], y)
                        transfer["transfer_status"] = "Processed"
                        data_provider.fetch_transfer_pool().update_transfer(transfer_id, transfer)
                        notification_processor.push(f"Processed batch transfer with id:{transfer['id']}")
                        self.send_response(200)
                        self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "items":
            item_id = path[1]
            item = data_provider.fetch_item_pool().get_item(item_id)
            if not item:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_item_pool().update_item(item_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_lines":
            item_line_id = int(path[1])
            item_line = data_provider.fetch_item_line_pool().get_item_line(item_line_id)
            if not item_line:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_item_line_pool().update_item_line(item_line_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_groups":
            item_group_id = int(path[1])
            item_group = data_provider.fetch_item_group_pool().get_item_group(item_group_id)
            if not item_group:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_item_group_pool().update_item_group(item_group_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_types":
            item_type_id = int(path[1])
            item_type = data_provider.fetch_item_type_pool().get_item_type(item_type_id)
            if not item_type:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_item_type_pool().update_item_type(item_type_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "inventories":
            inventory_id = int(path[1])
            inventory = data_provider.fetch_inventory_pool().get_inventory(inventory_id)
            if not inventory:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_inventory_pool().update_inventory(inventory_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "suppliers":
            supplier_id = int(path[1])
            supplier = data_provider.fetch_supplier_pool().get_supplier(supplier_id)
            if not supplier:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_supplier_pool().update_supplier(supplier_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "orders":
            paths = len(path)
            match paths:
                case 2:
                    order_id = int(path[1])
                    order = data_provider.fetch_order_pool().get_order(order_id)
                    if not order:
                        self.send_response(404)
                        self.end_headers()
                        return
                    data_provider.fetch_order_pool().update_order(order_id, new_data)
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if path[2] == "items":
                        order_id = int(path[1])
                        items = data_provider.fetch_order_pool().get_items_in_order(order_id)
                        if not items:
                            self.send_response(404)
                            self.end_headers()
                            return
                        updated_items = new_data
                        data_provider.fetch_order_pool().update_items_in_order(order_id, updated_items)
                        self.send_response(200)
                        self.end_headers()
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        elif path[0] == "clients":
            client_id = int(path[1])
            client = data_provider.fetch_client_pool().get_client(client_id)
            if not client:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_client_pool().update_client(client_id, new_data)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "shipments":
            paths = len(path)
            match paths:
                case 2:
                    shipment_id = int(path[1])
                    shipment = data_provider.fetch_shipment_pool().get_shipment(shipment_id)
                    if not shipment:
                        self.send_response(404)
                        self.end_headers()
                        return
                    data_provider.fetch_shipment_pool().update_shipment(shipment_id, new_data)
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if path[2] == "orders":
                        shipment_id = int(path[1])
                        orders = data_provider.fetch_order_pool().get_orders_in_shipment(shipment_id)
                        if not orders:
                            self.send_response(404)
                            self.end_headers()
                            return
                        updated_orders = new_data
                        data_provider.fetch_order_pool().update_orders_in_shipment(shipment_id, updated_orders)
                        self.send_response(200)
                        self.end_headers()
                    elif path[2] == "items":
                        shipment_id = int(path[1])
                        items = data_provider.fetch_shipment_pool().get_items_in_shipment(shipment_id)
                        if not items:
                            self.send_response(404)
                            self.end_headers()
                            return
                        updated_items = new_data
                        data_provider.fetch_shipment_pool().update_items_in_shipment(shipment_id, updated_items)
                        self.send_response(200)
                        self.end_headers()
                    elif path[2] == "commit":
                        # ToDo (Pending, Transit, Delivered)
                        pass
                    else:
                        self.send_response(404)
                        self.end_headers()
                case _:
                    self.send_response(404)
                    self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_PUT(self):
        self.set_db_path()
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        self.log_request(user)
        if user == None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                path = self.path.split("/")
                if len(path) > 3 and path[1] == "api" and path[2] == "v1":
                    self.handle_put_version_1(path[3:], user)
            except Exception:
                self.send_response(500)
                self.end_headers()

    def handle_delete_version_1(self, path, user):
        if not auth_provider.has_access(user, path, "delete"):
            self.send_response(403)
            self.end_headers()
            return
        if not self.is_valid_path_end(path[-1]):
            self.send_response(400)
            self.end_headers()
            return
        if path[0] == "warehouses":
            warehouse_id = int(path[1])
            warehouse = data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id)
            if not warehouse:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_warehouse_pool().remove_warehouse(warehouse_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "locations":
            location_id = int(path[1])
            location = data_provider.fetch_location_pool().get_location(location_id)
            if not location:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_location_pool().remove_location(location_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "transfers":
            transfer_id = int(path[1])
            transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
            if not transfer:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_transfer_pool().remove_transfer(transfer_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "items":
            item_id = path[1]
            item = data_provider.fetch_item_pool().get_item(item_id)
            if not item:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_item_pool().remove_item(item_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_lines":
            item_line_id = int(path[1])
            item_line = data_provider.fetch_item_line_pool().get_item_line(item_line_id)
            if not item_line:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_item_line_pool().remove_item_line(item_line_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_groups":
            item_group_id = int(path[1])
            item_group = data_provider.fetch_item_group_pool().get_item_group(item_group_id)
            if not item_group:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_item_group_pool().remove_item_group(item_group_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_types":
            item_type_id = int(path[1])
            item_type = data_provider.fetch_item_type_pool().get_item_type(item_type_id)
            if not item_type:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_item_type_pool().remove_item_type(item_type_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "inventories":
            inventory_id = int(path[1])
            inventory = data_provider.fetch_inventory_pool().get_inventory(inventory_id)
            if not inventory:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_inventory_pool().remove_inventory(inventory_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "suppliers":
            supplier_id = int(path[1])
            supplier = data_provider.fetch_supplier_pool().get_supplier(supplier_id)
            if not supplier:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_supplier_pool().remove_supplier(supplier_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "orders":
            order_id = int(path[1])
            order = data_provider.fetch_order_pool().get_order(order_id)
            if not order:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_order_pool().remove_order(order_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "clients":
            client_id = int(path[1])
            client = data_provider.fetch_client_pool().get_client(client_id)
            if not client:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_client_pool().remove_client(client_id)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "shipments":
            shipment_id = int(path[1])
            shipment = data_provider.fetch_shipment_pool().get_shipment(shipment_id)
            if not shipment:
                self.send_response(404)
                self.end_headers()
                return
            data_provider.fetch_shipment_pool().remove_shipment(shipment_id)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        self.set_db_path()
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        self.log_request(user)
        if user is None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                path = self.path.split("/")
                if len(path) > 3 and path[1] == "api" and path[2] == "v1":
                    self.handle_delete_version_1(path[3:], user)
            except Exception:
                self.send_response(500)
                self.end_headers()


def StartWebAPI(port, db_name, test_db_name):
    cargohub_db.delete_db(test_db_name)

    if port == 3001:
        cargohub_db.delete_db(db_name)

    # Create and populate the database if it doesn't exist
    if not os.path.exists(db_name):
        cargohub_db.create_clients_table(db_name, 'data/clients.json')
        cargohub_db.create_inventories_table(db_name, 'data/inventories.json')
        cargohub_db.create_item_groups_table(db_name, 'data/item_groups.json')
        cargohub_db.create_item_lines_table(db_name, 'data/item_lines.json')
        cargohub_db.create_item_types_table(db_name, 'data/item_types.json')
        cargohub_db.create_items_table(db_name, 'data/items.json')
        cargohub_db.create_locations_table(db_name, 'data/locations.json')
        cargohub_db.create_orders_table(db_name, 'data/orders.json')
        cargohub_db.create_shipments_table(db_name, 'data/shipments.json')
        cargohub_db.create_suppliers_table(db_name, 'data/suppliers.json')
        cargohub_db.create_transfers_table(db_name, 'data/transfers.json')
        cargohub_db.create_warehouses_table(db_name, 'data/warehouses.json')

    # Create test database if it doesn't exist
    cargohub_db.create_clients_table(test_db_name, 'data/clients.json')
    cargohub_db.create_inventories_table(test_db_name, 'data/inventories.json')
    cargohub_db.create_item_groups_table(test_db_name, 'data/item_groups.json')
    cargohub_db.create_item_lines_table(test_db_name, 'data/item_lines.json')
    cargohub_db.create_item_types_table(test_db_name, 'data/item_types.json')
    cargohub_db.create_items_table(test_db_name, 'data/items.json')
    cargohub_db.create_locations_table(test_db_name, 'data/locations.json')
    cargohub_db.create_orders_table(test_db_name, 'data/orders.json')
    cargohub_db.create_shipments_table(test_db_name, 'data/shipments.json')
    cargohub_db.create_suppliers_table(test_db_name, 'data/suppliers.json')
    cargohub_db.create_transfers_table(test_db_name, 'data/transfers.json')
    cargohub_db.create_warehouses_table(test_db_name, 'data/warehouses.json')

    with socketserver.TCPServer(("", port), ApiRequestHandler) as httpd:
        auth_provider.init()
        data_provider.init(db_name)
        notification_processor.start()
        print(f"Serving on port {port}...")
        httpd.serve_forever()


def start_servers():
    import threading

    # Start the second server on port 3001
    threading.Thread(target=StartWebAPI, args=(3001, 'data/Cargohub_3001.db', 'api/Tests/Test_Data/Cargohub_Test_3001.db')).start()
    sleep(7)
    os.system('cls' if os.name == 'nt' else 'clear')
    # Start the first server on port 3000
    threading.Thread(target=StartWebAPI, args=(3000, 'data/Cargohub.db', 'api/Tests/Test_Data/Cargohub_Test.db')).start()



if __name__ == "__main__":
    start_servers()

# Improvement ideas:
# All files should prevent double id's, incomplete jsons and nonexistent id's
# For each delete endpoint, stop as soon as the id is found. Now it goes through the whole file all the time
# get_items_in_transfer() in transfers returns a list, however this list always contains one item. This can be simplified
# Each transfer has only one item. Maybe the dictionary structure can be simplified
# get_inventories_for_item() in items returns a list, however this list always contains one item. This can be simplified
# get_orders_in_shipment() returns a list, however this list always contains one item. This can be simplified
# get_orders_in_shipment() returns a list with a number. We could consider changing the code to return the order objects.

# Found Errors:
# Non-fullaccess users in Auth-provider
# Post endpoint for item_type, item_line and item_group
# Empty PUT commit endpoint in shipment
# Failing PUT update_items in shipment
# The PUT update_orders in shipments 200 OK, but can cause negative id's and potentially more errors
# Failing PUT commit endpoint in transfers
# Failing PUT update_items in orders