import socketserver
import http.server
import json
import logging

from providers import auth_provider
from providers import data_provider

from processors import notification_processor

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

        if path[0] not in pools:
            self.send_response(404)
            self.end_headers()
            return

        pool = pools[path[0]]
        paths = len(path)

        try:
            if paths == 1:
                if hasattr(pool, "get_" + path[0]):
                    send_json_response(getattr(pool, "get_" + path[0])())
                else:
                    send_json_response(None, 404)
            elif paths == 2:
                identifier = int(path[1]) if path[0] != "items" else path[1]
                if hasattr(pool, "get_" + path[0][:-1]):
                    send_json_response(getattr(pool, "get_" + path[0][:-1])(identifier))
                else:
                    send_json_response(None, 404)
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
        if path[0] == "warehouses":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_warehouse = json.loads(post_data.decode())
            data_provider.fetch_warehouse_pool().add_warehouse(new_warehouse)
            data_provider.fetch_warehouse_pool().save()
            self.send_response(201)
            self.end_headers()
        elif path[0] == "locations":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_location = json.loads(post_data.decode())
            data_provider.fetch_location_pool().add_location(new_location)
            data_provider.fetch_location_pool().save()
            self.send_response(201)
            self.end_headers()
        elif path[0] == "transfers":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_transfer = json.loads(post_data.decode())
            data_provider.fetch_transfer_pool().add_transfer(new_transfer)
            data_provider.fetch_transfer_pool().save()
            notification_processor.push(
                f"Scheduled batch transfer {new_transfer['id']}")
            self.send_response(201)
            self.end_headers()
        elif path[0] == "items":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_item = json.loads(post_data.decode())
            data_provider.fetch_item_pool().add_item(new_item)
            data_provider.fetch_item_pool().save()
            self.send_response(201)
            self.end_headers()

        # elif path[0] == "item_lines":
        #     content_length = int(self.headers["Content-Length"])
        #     post_data = self.rfile.read(content_length)
        #     new_item_line = json.loads(post_data.decode())
        #     data_provider.fetch_item_line_pool().add_item_line(new_item_line)
        #     data_provider.fetch_item_line_pool().save()
        #     self.send_response(201)
        #     self.end_headers()
        # elif path[0] == "item_groups":
        #     content_length = int(self.headers["Content-Length"])
        #     post_data = self.rfile.read(content_length)
        #     new_item_group = json.loads(post_data.decode())
        #     data_provider.fetch_item_group_pool().add_item_group(new_item_group)
        #     data_provider.fetch_item_group_pool().save()
        #     self.send_response(201)
        #     self.end_headers()
        # elif path[0] == "item_types":
        #     content_length = int(self.headers["Content-Length"])
        #     post_data = self.rfile.read(content_length)
        #     new_item_type = json.loads(post_data.decode())
        #     data_provider.fetch_item_type_pool().add_item_type(new_item_type)
        #     data_provider.fetch_item_type_pool().save()
        #     self.send_response(201)
        #     self.end_headers()

        elif path[0] == "inventories":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_inventory = json.loads(post_data.decode())
            data_provider.fetch_inventory_pool().add_inventory(new_inventory)
            data_provider.fetch_inventory_pool().save()
            self.send_response(201)
            self.end_headers()
        elif path[0] == "suppliers":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_supplier = json.loads(post_data.decode())
            data_provider.fetch_supplier_pool().add_supplier(new_supplier)
            data_provider.fetch_supplier_pool().save()
            self.send_response(201)
            self.end_headers()
        elif path[0] == "orders":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_order = json.loads(post_data.decode())
            data_provider.fetch_order_pool().add_order(new_order)
            data_provider.fetch_order_pool().save()
            self.send_response(201)
            self.end_headers()
        elif path[0] == "clients":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_client = json.loads(post_data.decode())
            data_provider.fetch_client_pool().add_client(new_client)
            data_provider.fetch_client_pool().save()
            self.send_response(201)
            self.end_headers()
        elif path[0] == "shipments":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            new_shipment = json.loads(post_data.decode())
            data_provider.fetch_shipment_pool().add_shipment(new_shipment)
            data_provider.fetch_shipment_pool().save()
            self.send_response(201)
            self.end_headers()
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
        if not auth_provider.has_access(user, path, "put"):
            self.send_response(403)
            self.end_headers()
            return
        if path[0] == "warehouses":
            warehouse_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_warehouse = json.loads(post_data.decode())
            data_provider.fetch_warehouse_pool().update_warehouse(
                warehouse_id, updated_warehouse)
            data_provider.fetch_warehouse_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "locations":
            location_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_location = json.loads(post_data.decode())
            data_provider.fetch_location_pool().update_location(location_id, updated_location)
            data_provider.fetch_location_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "transfers":
            paths = len(path)
            match paths:
                case 2:
                    transfer_id = int(path[1])
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_transfer = json.loads(post_data.decode())
                    data_provider.fetch_transfer_pool().update_transfer(transfer_id, updated_transfer)
                    data_provider.fetch_transfer_pool().save()
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if path[2] == "commit":
                        transfer_id = int(path[1])
                        transfer = data_provider.fetch_transfer_pool().get_transfer(transfer_id)
                        for x in transfer["items"]:
                            inventories = data_provider.fetch_inventory_pool(
                            ).get_inventories_for_item(x["item_id"])
                            for y in inventories:
                                if y["location_id"] == transfer["transfer_from"]:
                                    y["total_on_hand"] -= x["amount"]
                                    y["total_expected"] = y["total_on_hand"] + \
                                        y["total_ordered"]
                                    y["total_available"] = y["total_on_hand"] - \
                                        y["total_allocated"]
                                    data_provider.fetch_inventory_pool(
                                    ).update_inventory(y["id"], y)
                                elif y["location_id"] == transfer["transfer_to"]:
                                    y["total_on_hand"] += x["amount"]
                                    y["total_expected"] = y["total_on_hand"] + \
                                        y["total_ordered"]
                                    y["total_available"] = y["total_on_hand"] - \
                                        y["total_allocated"]
                                    data_provider.fetch_inventory_pool(
                                    ).update_inventory(y["id"], y)
                                # The above code contains many errors. It should be rewritten
                                # It is very likely this ↓ ↓ ↓  should be "Completed" instead of "Processed"
                        transfer["transfer_status"] = "Processed"
                        data_provider.fetch_transfer_pool().update_transfer(transfer_id, transfer)
                        notification_processor.push(
                            f"Processed batch transfer with id:{transfer['id']}")
                        data_provider.fetch_transfer_pool().save()
                        data_provider.fetch_inventory_pool().save()
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
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item = json.loads(post_data.decode())
            data_provider.fetch_item_pool().update_item(item_id, updated_item)
            data_provider.fetch_item_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_lines":
            item_line_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_line = json.loads(post_data.decode())
            data_provider.fetch_item_line_pool().update_item_line(
                item_line_id, updated_item_line)
            data_provider.fetch_item_line_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_groups":
            item_group_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_group = json.loads(post_data.decode())
            data_provider.fetch_item_group_pool().update_item_group(
                item_group_id, updated_item_group)
            data_provider.fetch_item_group_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_types":
            item_type_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_item_type = json.loads(post_data.decode())
            data_provider.fetch_item_type_pool().update_item_type(
                item_type_id, updated_item_type)
            data_provider.fetch_item_type_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "inventories":
            inventory_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_inventory = json.loads(post_data.decode())
            data_provider.fetch_inventory_pool().update_inventory(
                inventory_id, updated_inventory)
            data_provider.fetch_inventory_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "suppliers":
            supplier_id = int(path[1])
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_supplier = json.loads(post_data.decode())
            data_provider.fetch_supplier_pool().update_supplier(supplier_id, updated_supplier)
            data_provider.fetch_supplier_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "orders":
            paths = len(path)
            match paths:
                case 2:
                    order_id = int(path[1])
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_order = json.loads(post_data.decode())
                    data_provider.fetch_order_pool().update_order(order_id, updated_order)
                    data_provider.fetch_order_pool().save()
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if path[2] == "items":
                        order_id = int(path[1])
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_items = json.loads(post_data.decode())
                        data_provider.fetch_order_pool().update_items_in_order(order_id, updated_items)
                        data_provider.fetch_order_pool().save()
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
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            updated_client = json.loads(post_data.decode())
            data_provider.fetch_client_pool().update_client(client_id, updated_client)
            data_provider.fetch_client_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "shipments":
            paths = len(path)
            match paths:
                case 2:
                    shipment_id = int(path[1])
                    content_length = int(self.headers["Content-Length"])
                    post_data = self.rfile.read(content_length)
                    updated_shipment = json.loads(post_data.decode())
                    data_provider.fetch_shipment_pool().update_shipment(shipment_id, updated_shipment)
                    data_provider.fetch_shipment_pool().save()
                    self.send_response(200)
                    self.end_headers()
                case 3:
                    if path[2] == "orders":
                        shipment_id = int(path[1])
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_orders = json.loads(post_data.decode())
                        data_provider.fetch_order_pool().update_orders_in_shipment(
                            shipment_id, updated_orders)
                        data_provider.fetch_order_pool().save()
                        self.send_response(200)
                        self.end_headers()
                    elif path[2] == "items":
                        shipment_id = int(path[1])
                        content_length = int(self.headers["Content-Length"])
                        post_data = self.rfile.read(content_length)
                        updated_items = json.loads(post_data.decode())
                        data_provider.fetch_shipment_pool().update_items_in_shipment(
                            shipment_id, updated_items)
                        data_provider.fetch_shipment_pool().save()
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
        if path[0] == "warehouses":
            warehouse_id = int(path[1])
            data_provider.fetch_warehouse_pool().remove_warehouse(warehouse_id)
            data_provider.fetch_warehouse_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "locations":
            location_id = int(path[1])
            data_provider.fetch_location_pool().remove_location(location_id)
            data_provider.fetch_location_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "transfers":
            transfer_id = int(path[1])
            data_provider.fetch_transfer_pool().remove_transfer(transfer_id)
            data_provider.fetch_transfer_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "items":
            item_id = path[1]
            data_provider.fetch_item_pool().remove_item(item_id)
            data_provider.fetch_item_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_lines":
            item_line_id = int(path[1])
            data_provider.fetch_item_line_pool().remove_item_line(item_line_id)
            data_provider.fetch_item_line_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_groups":
            item_group_id = int(path[1])
            data_provider.fetch_item_group_pool().remove_item_group(item_group_id)
            data_provider.fetch_item_group_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "item_types":
            item_type_id = int(path[1])
            data_provider.fetch_item_type_pool().remove_item_type(item_type_id)
            data_provider.fetch_item_type_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "inventories":
            inventory_id = int(path[1])
            data_provider.fetch_inventory_pool().remove_inventory(inventory_id)
            data_provider.fetch_inventory_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "suppliers":
            supplier_id = int(path[1])
            data_provider.fetch_supplier_pool().remove_supplier(supplier_id)
            data_provider.fetch_supplier_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "orders":
            order_id = int(path[1])
            data_provider.fetch_order_pool().remove_order(order_id)
            data_provider.fetch_order_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "clients":
            client_id = int(path[1])
            data_provider.fetch_client_pool().remove_client(client_id)
            data_provider.fetch_client_pool().save()
            self.send_response(200)
            self.end_headers()
        elif path[0] == "shipments":
            shipment_id = int(path[1])
            data_provider.fetch_shipment_pool().remove_shipment(shipment_id)
            data_provider.fetch_shipment_pool().save()
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
