import socketserver
import http.server
import json
import logging
import os

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

    def handle_get_version_1(self, path, user):
        self.log_request(user)
        if not auth_provider.has_access(user, path, "get"):
            self.send_response(403)
            self.end_headers()
            return

        # helper function voor het verzenden van responses
        def send_json_response(data, status=200):
            self.send_response(status)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            if data is not None:
                self.wfile.write(json.dumps(data).encode("utf-8"))

        pools = {
            "warehouses": data_provider.fetch_warehouse_pool(),
            "locations": data_provider.fetch_location_pool(),
            "transfers": data_provider.fetch_transfer_pool(),
            "items": data_provider.fetch_item_pool(),
            "inventories": data_provider.fetch_inventory_pool(),
            "suppliers": data_provider.fetch_supplier_pool(),
            "orders": data_provider.fetch_order_pool(),
            "clients": data_provider.fetch_client_pool(),
            "shipments": data_provider.fetch_shipment_pool(),
            "item_lines": data_provider.fetch_item_line_pool(),
            "item_groups": data_provider.fetch_item_group_pool(),
            "item_types": data_provider.fetch_item_type_pool(),
        }

        # kijkt of de recource bestaat in de dictionary
        if path[0] not in pools:
            self.send_response(404)
            self.end_headers()
            return

        pool = pools[path[0]]
        paths = len(path)

        try:
            # Verwerk verzoeken met alleen de resource-naam (bijv. "/items").
            if paths == 1:
                if hasattr(pool, "get_" + path[0]):
                    send_json_response(getattr(pool, "get_" + path[0])())
                else:
                    send_json_response(None, 404)

            # Verwerk verzoeken met een resource en een identificator (bijv. "/items/123").
            elif paths == 2:
                identifier = int(path[1]) if path[0] != "items" else path[1]
                if hasattr(pool, "get_" + path[0][:-1]):
                    send_json_response(getattr(pool, "get_" + path[0][:-1])(identifier))
                else:
                    send_json_response(None, 404)

            # Verwerk verzoeken met een resource, een identificator en een geneste resource (bijv. "/warehouses/123/items").
            elif paths == 3:
                if path[2] in ["locations", "items", "inventory", "orders"]:
                    if hasattr(pool, "get_" + path[2] + "_in_" + path[0][:-1]):
                        send_json_response(
                            getattr(pool, "get_" + path[2] + "_in_" + path[0][:-1])(
                                int(path[1])
                            )
                        )
                    elif path[2] == "inventory" and hasattr(pool, "get_inventories_for_item"):
                        send_json_response(
                            pool.get_inventories_for_item(path[1])
                        )
                    else:
                        send_json_response(None, 404)
                else:
                    send_json_response(None, 404)

            # Verwerk een speciale case voor inventory-totals (bijv. "/items/123/inventory/totals").
            elif paths == 4 and path[2] == "inventory" and path[3] == "totals":
                if hasattr(pool, "get_inventory_totals_for_item"):
                    send_json_response(pool.get_inventory_totals_for_item(path[1]))
                else:
                    send_json_response(None, 404)
            else:
                send_json_response(None, 404)
        except Exception:
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        if user is None:
            self.send_response(401)
            self.end_headers()
        else:
            try:
                path = self.path.split("/")
                if len(path) > 3 and path[1] == "api" and path[2] == "v1":
                    self.handle_get_version_1(path[3:], user)
                else:
                    self.send_response(404)
                    self.end_headers()
            except Exception:
                self.send_response(500)
                self.end_headers()

    def handle_post_version_1(self, path, user):
        self.log_request(user)
        if not auth_provider.has_access(user, path, "post"):
            self.send_response(403)
            self.end_headers()
            return

        # Define pools as a dictionary mapping
        pools = {
            "warehouses": data_provider.fetch_warehouse_pool,
            "locations": data_provider.fetch_location_pool,
            "transfers": data_provider.fetch_transfer_pool,
            "items": data_provider.fetch_item_pool,
            "item_lines": data_provider.fetch_item_line_pool,
            "item_groups": data_provider.fetch_item_group_pool,
            "item_types": data_provider.fetch_item_type_pool,
            "inventories": data_provider.fetch_inventory_pool,
            "suppliers": data_provider.fetch_supplier_pool,
            "orders": data_provider.fetch_order_pool,
            "clients": data_provider.fetch_client_pool,
            "shipments": data_provider.fetch_shipment_pool,
        }

        # Hieronder is de volgende code refactored
        # if path[0] == "warehouses":
        # content_length = int(self.headers["Content-Length"])
        # post_data = self.rfile.read(content_length)
        # new_warehouse = json.loads(post_data.decode())
        # data_provider.fetch_warehouse_pool().add_warehouse(new_warehouse)
        # data_provider.fetch_warehouse_pool().save()
        # self.send_response(201)
        # self.end_headers()

        if path[0] in pools:
            try:
                # Read and parse the POST data
                content_length = int(self.headers["Content-Length"])
                post_data = self.rfile.read(content_length)
                new_data = json.loads(post_data.decode())

                # Get the pool and add/save the new data
                pool = pools[path[0]]()
                add_method = getattr(pool, f"add_{path[0][:-1]}")
                add_method(new_data)
                print("Client added to the database successfully.")

                # Special case for "transfers" to handle notifications
                if path[0] == "transfers":
                    notification_processor.push(
                        f"Scheduled batch transfer {new_data['id']}"
                    )

                self.send_response(201)
                self.end_headers()
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                print(f"Error processing POST for {path[0]}: {e}")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
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
        self.log_request(user)
        
        # Check for access authorization
        if not auth_provider.has_access(user, path, "put"):
            self.send_response(403)
            self.end_headers()
            return
        
        # Define the entity pools and their respective update methods
        pools = {
            "warehouses": (data_provider.fetch_warehouse_pool(), "update_warehouse"),
            "locations": (data_provider.fetch_location_pool(), "update_location"),
            "items": (data_provider.fetch_item_pool(), "update_item"),
            "item_lines": (data_provider.fetch_item_line_pool(), "update_item_line"),
            "item_groups": (data_provider.fetch_item_group_pool(), "update_item_group"),
            "item_types": (data_provider.fetch_item_type_pool(), "update_item_type"),
            "inventories": (data_provider.fetch_inventory_pool(), "update_inventory"),
            "suppliers": (data_provider.fetch_supplier_pool(), "update_supplier"),
            "clients": (data_provider.fetch_client_pool(), "update_client"),
            "orders": (data_provider.fetch_order_pool(), "update_order"),
            "shipments": (data_provider.fetch_shipment_pool(), "update_shipment")
        }
        
        # Handle different entities with similar logic
        if path[0] in pools:
            entity_pool, update_method = pools[path[0]]
            entity_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_entity = json.loads(post_data.decode())
            getattr(entity_pool, update_method)(entity_id, updated_entity)
            self.send_response(200)
            self.end_headers()
        
        # Special case for "transfers" with nested logic
        elif path[0] == "transfers":
            paths = len(path)
            match paths:
                case 2:
                    transfer_id = int(path[1])
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
        
        # Handle "orders" with nested "items" update logic
        elif path[0] == "orders" and len(path) == 3 and path[2] == "items":
            order_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_items = json.loads(post_data.decode())
            data_provider.fetch_order_pool().update_items_in_order(order_id, updated_items)
            self.send_response(200)
            self.end_headers()
        
        # Handle "shipments" with nested logic
        elif path[0] == "shipments":
            paths = len(path)
            match paths:
                case 2:
                    shipment_id = int(path[1])
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_shipment = json.loads(post_data.decode())
                    data_provider.fetch_shipment_pool().update_shipment(shipment_id, updated_shipment)
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if path[2] == "orders":
                        shipment_id = int(path[1])
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_orders = json.loads(post_data.decode())
                        data_provider.fetch_order_pool().update_orders_in_shipment(shipment_id, updated_orders)
                        self.send_response(200)
                        self.end_headers()
                    elif path[2] == "items":
                        shipment_id = int(path[1])
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
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
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
        self.log_request(user)

        if not auth_provider.has_access(user, path, "delete"):
            self.send_response(403)
            self.end_headers()
            return

        # Dictionary mapping paths to corresponding remove methods and pool fetchers
        pools = {
            "warehouses": (data_provider.fetch_warehouse_pool(), "remove_warehouse"),
            "locations": (data_provider.fetch_location_pool(), "remove_location"),
            "transfers": (data_provider.fetch_transfer_pool(), "remove_transfer"),
            "items": (data_provider.fetch_item_pool(), "remove_item"),
            "item_lines": (data_provider.fetch_item_line_pool(), "remove_item_line"),
            "item_groups": (data_provider.fetch_item_group_pool(), "remove_item_group"),
            "item_types": (data_provider.fetch_item_type_pool(), "remove_item_type"),
            "inventories": (data_provider.fetch_inventory_pool(), "remove_inventory"),
            "suppliers": (data_provider.fetch_supplier_pool(), "remove_supplier"),
            "orders": (data_provider.fetch_order_pool(), "remove_order"),
            "clients": (data_provider.fetch_client_pool(), "remove_client"),
            "shipments": (data_provider.fetch_shipment_pool(), "remove_shipment")
        }

        # Het volgende code wordt hieronder uitgevoerd maar dan refactored
        # if path[0] == "warehouses":
        # warehouse_id = int(path[1])
        # data_provider.fetch_warehouse_pool().remove_warehouse(warehouse_id)
        # data_provider.fetch_warehouse_pool().save()
        # self.send_response(200)
        # self.end_headers()

        if path[0] in pools:
            pool, remove_method = pools[path[0]]
            # Special handling for "items" as it uses a string ID
            entity_id = int(path[1]) if path[0] != "items" else path[1]
            # Call the corresponding remove method dynamically
            getattr(pool, remove_method)(entity_id)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        api_key = self.headers.get("API_KEY")
        user = auth_provider.get_user(api_key)
        if user == None:
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


def StartWebAPI():
    # Create and populate the database if it doesn't exist
    db_name = 'data/Cargohub.db'
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
    test_db_name = 'api/Tests/Test_Data/Cargohub_Test.db'
    if not os.path.exists(test_db_name):
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
    
    PORT = 3000
    with socketserver.TCPServer(("", PORT), ApiRequestHandler) as httpd:
        auth_provider.init()
        data_provider.init()
        notification_processor.start()
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()


if __name__ == "__main__":
    StartWebAPI()


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
