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
        if path[0] == "warehouses":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_warehouse = json.loads(post_data.decode())
            warehouse_id = new_warehouse.get("id")
            if data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_warehouse_pool().add_warehouse(new_warehouse)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "locations":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_location = json.loads(post_data.decode())
            location_id = new_location.get("id")
            if data_provider.fetch_location_pool().get_location(location_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_location_pool().add_location(new_location)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "transfers":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_transfer = json.loads(post_data.decode())
            transfer_id = new_transfer.get("id")
            if data_provider.fetch_transfer_pool().get_transfer(transfer_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_transfer_pool().add_transfer(new_transfer)
            notification_processor.push(f"Scheduled batch transfer {new_transfer['id']}")
            self.send_response(201)
            self.end_headers()
        elif path[0] == "items":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item = json.loads(post_data.decode())
            item_id = new_item.get("uid")
            if data_provider.fetch_item_pool().get_item(item_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_item_pool().add_item(new_item)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "item_lines":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item_line = json.loads(post_data.decode())
            item_line_id = new_item_line.get("id")
            if data_provider.fetch_item_line_pool().get_item_line(item_line_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_item_line_pool().add_item_line(new_item_line)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "item_groups":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item_group = json.loads(post_data.decode())
            item_group_id = new_item_group.get("id")
            if data_provider.fetch_item_group_pool().get_item_group(item_group_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_item_group_pool().add_item_group(new_item_group)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "item_types":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item_type = json.loads(post_data.decode())
            item_type_id = new_item_type.get("id")
            if data_provider.fetch_item_type_pool().get_item_type(item_type_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_item_type_pool().add_item_type(new_item_type)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "inventories":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_inventory = json.loads(post_data.decode())
            inventory_id = new_inventory.get("id")
            if data_provider.fetch_inventory_pool().get_inventory(inventory_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_inventory_pool().add_inventory(new_inventory)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "suppliers":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_supplier = json.loads(post_data.decode())
            supplier_id = new_supplier.get("id")
            if data_provider.fetch_supplier_pool().get_supplier(supplier_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_supplier_pool().add_supplier(new_supplier)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "orders":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_order = json.loads(post_data.decode())
            order_id = new_order.get("id")
            if data_provider.fetch_order_pool().get_order(order_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_order_pool().add_order(new_order)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "clients":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_client = json.loads(post_data.decode())
            client_id = new_client.get("id")
            if data_provider.fetch_client_pool().get_client(client_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_client_pool().add_client(new_client)
            self.send_response(201)
            self.end_headers()
        elif path[0] == "shipments":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_shipment = json.loads(post_data.decode())
            shipment_id = new_shipment.get("id")
            if data_provider.fetch_shipment_pool().get_shipment(shipment_id):
                self.send_response(409)
                self.end_headers()
                return
            data_provider.fetch_shipment_pool().add_shipment(new_shipment)
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
        if path[0] == "warehouses":
            warehouse_id = int(path[1])
            warehouse = data_provider.fetch_warehouse_pool().get_warehouse(warehouse_id)
            if not warehouse:
                self.send_response(404)
                self.end_headers()
                return
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_warehouse = json.loads(post_data.decode())
            data_provider.fetch_warehouse_pool().update_warehouse(warehouse_id, updated_warehouse)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "locations":
            location_id = int(path[1])
            location = data_provider.fetch_location_pool().get_location(location_id)
            if not location:
                self.send_response(404)
                self.end_headers()
                return
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_location = json.loads(post_data.decode())
            data_provider.fetch_location_pool().update_location(location_id, updated_location)
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
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_transfer = json.loads(post_data.decode())
                    data_provider.fetch_transfer_pool().update_transfer(transfer_id, updated_transfer)
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
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item = json.loads(post_data.decode())
            data_provider.fetch_item_pool().update_item(item_id, updated_item)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_lines":
            item_line_id = int(path[1])
            item_line = data_provider.fetch_item_line_pool().get_item_line(item_line_id)
            if not item_line:
                self.send_response(404)
                self.end_headers()
                return
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_line = json.loads(post_data.decode())
            data_provider.fetch_item_line_pool().update_item_line(item_line_id, updated_item_line)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_groups":
            item_group_id = int(path[1])
            item_group = data_provider.fetch_item_group_pool().get_item_group(item_group_id)
            if not item_group:
                self.send_response(404)
                self.end_headers()
                return
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_group = json.loads(post_data.decode())
            data_provider.fetch_item_group_pool().update_item_group(item_group_id, updated_item_group)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_types":
            item_type_id = int(path[1])
            item_type = data_provider.fetch_item_type_pool().get_item_type(item_type_id)
            if not item_type:
                self.send_response(404)
                self.end_headers()
                return
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_type = json.loads(post_data.decode())
            data_provider.fetch_item_type_pool().update_item_type(item_type_id, updated_item_type)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "inventories":
            inventory_id = int(path[1])
            inventory = data_provider.fetch_inventory_pool().get_inventory(inventory_id)
            if not inventory:
                self.send_response(404)
                self.end_headers()
                return
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_inventory = json.loads(post_data.decode())
            data_provider.fetch_inventory_pool().update_inventory(inventory_id, updated_inventory)
            self.send_response(200)
            self.end_headers()
        elif path[0] == "suppliers":
            supplier_id = int(path[1])
            supplier = data_provider.fetch_supplier_pool().get_supplier(supplier_id)
            if not supplier:
                self.send_response(404)
                self.end_headers()
                return
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_supplier = json.loads(post_data.decode())
            data_provider.fetch_supplier_pool().update_supplier(supplier_id, updated_supplier)
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
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_order = json.loads(post_data.decode())
                    data_provider.fetch_order_pool().update_order(order_id, updated_order)
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
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_items = json.loads(post_data.decode())
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
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_client = json.loads(post_data.decode())
            data_provider.fetch_client_pool().update_client(client_id, updated_client)
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
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_shipment = json.loads(post_data.decode())
                    data_provider.fetch_shipment_pool().update_shipment(shipment_id, updated_shipment)
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
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_orders = json.loads(post_data.decode())
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
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_items = json.loads(post_data.decode())
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