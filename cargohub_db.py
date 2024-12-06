import sqlite3
import json
import os
from datetime import datetime

def create_clients_table(db_name, json_relative_path):
    table_name = 'clients'
    columns = '''id INTEGER PRIMARY KEY, 
                 name TEXT, 
                 address TEXT, 
                 city TEXT, 
                 zip_code TEXT, 
                 province TEXT, 
                 country TEXT, 
                 contact_name TEXT, 
                 contact_phone TEXT, 
                 contact_email TEXT, 
                 created_at TEXT, 
                 updated_at TEXT'''

    # Load data from JSON
    data = load_data_from_json(json_relative_path)
    
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Create the table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
        
        # Insert data into the table
        for client in data:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, name, address, city, zip_code, province, country, 
                                          contact_name, contact_phone, contact_email, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                client['id'], client['name'], client['address'], client['city'], client['zip_code'], 
                client['province'], client['country'], client['contact_name'], client['contact_phone'], 
                client['contact_email'], client.get('created_at', datetime.now().isoformat()), 
                client.get('updated_at', datetime.now().isoformat())
            ))
        
        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{table_name}' table.")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_inventories_table(db_name, json_relative_path):
    inventory_table = 'inventories'
    location_table = 'inventory_locations'

    # Define table schemas
    inventory_columns = '''id INTEGER PRIMARY KEY, 
                           item_id TEXT, 
                           description TEXT, 
                           item_reference TEXT, 
                           total_on_hand INTEGER, 
                           total_expected INTEGER, 
                           total_ordered INTEGER, 
                           total_allocated INTEGER, 
                           total_available INTEGER, 
                           created_at TEXT, 
                           updated_at TEXT'''

    location_columns = '''id INTEGER PRIMARY KEY AUTOINCREMENT, 
                          inventory_id INTEGER, 
                          location_id INTEGER, 
                          FOREIGN KEY (inventory_id) REFERENCES inventories (id) ON DELETE CASCADE'''

    # Load data from JSON
    data = load_data_from_json(json_relative_path)
    
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Create the tables
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {inventory_table} ({inventory_columns});")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {location_table} ({location_columns});")
        
        # Insert data into the inventories table
        for inventory in data:
            cursor.execute(f"""
                INSERT INTO {inventory_table} (id, item_id, description, item_reference, 
                                               total_on_hand, total_expected, total_ordered, 
                                               total_allocated, total_available, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                inventory['id'], inventory['item_id'], inventory['description'], inventory['item_reference'],
                inventory['total_on_hand'], inventory['total_expected'], inventory['total_ordered'],
                inventory['total_allocated'], inventory['total_available'],
                inventory.get('created_at', datetime.now().isoformat()),
                inventory.get('updated_at', datetime.now().isoformat())
            ))
            
            # Get the last inserted inventory id
            inventory_id = inventory['id']
            
            # Insert locations into the locations table
            for location_id in inventory['locations']:
                cursor.execute(f"""
                    INSERT INTO {location_table} (inventory_id, location_id) 
                    VALUES (?, ?)
                """, (inventory_id, location_id))
        
        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{inventory_table}' and '{location_table}' tables.")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_item_groups_table(db_name, json_relative_path):
    table_name = 'item_groups'
    columns = '''id INTEGER PRIMARY KEY, 
                 name TEXT, 
                 description TEXT, 
                 created_at TEXT, 
                 updated_at TEXT'''

    # Load data from JSON
    data = load_data_from_json(json_relative_path)
    
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Create the table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
        
        # Insert data into the table
        for item_group in data:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, name, description, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?)
            """, (
                item_group['id'], item_group['name'], item_group['description'], 
                item_group.get('created_at', datetime.now().isoformat()), 
                item_group.get('updated_at', datetime.now().isoformat())
            ))
        
        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{table_name}' table.")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_item_lines_table(db_name, json_relative_path):
    table_name = 'item_lines'
    columns = '''id INTEGER PRIMARY KEY, 
                 name TEXT, 
                 description TEXT, 
                 created_at TEXT, 
                 updated_at TEXT'''

    # Load data from JSON
    data = load_data_from_json(json_relative_path)
    
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Create the table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
        
        # Insert data into the table
        for item_group in data:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, name, description, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?)
            """, (
                item_group['id'], item_group['name'], item_group['description'], 
                item_group.get('created_at', datetime.now().isoformat()), 
                item_group.get('updated_at', datetime.now().isoformat())
            ))
        
        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{table_name}' table.")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_item_types_table(db_name, json_relative_path):
    table_name = 'item_types'
    columns = '''id INTEGER PRIMARY KEY, 
                 name TEXT, 
                 description TEXT, 
                 created_at TEXT, 
                 updated_at TEXT'''

    # Load data from JSON
    data = load_data_from_json(json_relative_path)
    
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    try:
        # Create the table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
        
        # Insert data into the table
        for item_group in data:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, name, description, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?)
            """, (
                item_group['id'], item_group['name'], item_group['description'], 
                item_group.get('created_at', datetime.now().isoformat()), 
                item_group.get('updated_at', datetime.now().isoformat())
            ))
        
        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{table_name}' table.")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_items_table(db_name, json_relative_path):
    table_name = 'items'
    columns = '''uid Text PRIMARY KEY,
                 code Text,
                 description Text,
                 short_description Text,
                 upc_code Text,
                 model_number Text,
                 commodity_code Text,
                 item_line_id Integer,
                 item_group_id Integer,
                 item_type_id Integer,
                 unit_purchase_quantity Integer,
                 unit_order_quantity Integer,
                 pack_order_quantity Integer,
                 supplier_id Integer,
                 supplier_code Text,
                 supplier_part_number Text,
                 created_at Text,
                 updated_at Text'''
    
    # Load data from JSON
    data = load_data_from_json(json_relative_path)

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        # Create the table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")

        # Insert data into the table
        for item in data:
            cursor.execute(f"""
                INSERT INTO {table_name} (uid, code, description, short_description, upc_code, model_number, 
                                          commodity_code, item_line_id, item_group_id, item_type_id, 
                                          unit_purchase_quantity, unit_order_quantity, pack_order_quantity, 
                                          supplier_id, supplier_code, supplier_part_number, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, ( 
                item['uid'], item['code'], item['description'], item['short_description'], item['upc_code'], 
                item['model_number'], item['commodity_code'], item['item_line'], item['item_group'], 
                item['item_type'], item['unit_purchase_quantity'], item['unit_order_quantity'],
                item['pack_order_quantity'], item['supplier_id'], item['supplier_code'], 
                item['supplier_part_number'], item.get('created_at', datetime.now().isoformat()), 
                item.get('updated_at', datetime.now().isoformat())
            ))
        
        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{table_name}' table.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_locations_table(db_name, json_relative_path):
    table_name = 'locations'
    columns = '''id Integer PRIMARY KEY,
                 warehouse_id Integer,
                 code Text,
                 name Text,
                 created_at Text,
                 updated_at Text'''
    
    # Load data from JSON
    data = load_data_from_json(json_relative_path)

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        # Create the table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")

        # Insert data into the table
        for location in data:
            cursor.execute(f"""
                INSERT INTO {table_name} (id, warehouse_id, code, name, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                location['id'], location['warehouse_id'], location['code'], location['name'], 
                location['created_at'], location['updated_at']
            ))
        
        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{table_name}' table.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_orders_table(db_name, json_relative_path):
    orders_table = 'orders'
    order_items_table = 'order_items'

    orders_columns = '''id INTEGER PRIMARY KEY, 
                        source_id INTEGER, 
                        order_date TEXT, 
                        request_date TEXT, 
                        reference TEXT, 
                        reference_extra TEXT, 
                        order_status TEXT, 
                        notes TEXT, 
                        shipping_notes TEXT, 
                        picking_notes TEXT, 
                        warehouse_id INTEGER, 
                        ship_to TEXT, 
                        bill_to TEXT, 
                        shipment_id INTEGER, 
                        total_amount REAL, 
                        total_discount REAL, 
                        total_tax REAL, 
                        total_surcharge REAL, 
                        created_at TEXT, 
                        updated_at TEXT'''

    order_items_columns = '''id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             order_id INTEGER, 
                             item_id TEXT, 
                             amount INTEGER, 
                             FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE'''

    data = load_data_from_json(json_relative_path)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {orders_table} ({orders_columns});")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {order_items_table} ({order_items_columns});")

        for order in data:
            cursor.execute(f"""
                INSERT OR IGNORE INTO {orders_table} (id, source_id, order_date, request_date, reference, 
                                                      reference_extra, order_status, notes, shipping_notes, 
                                                      picking_notes, warehouse_id, ship_to, bill_to, shipment_id, 
                                                      total_amount, total_discount, total_tax, total_surcharge, 
                                                      created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order['id'], order['source_id'], order['order_date'], order['request_date'], order['reference'], 
                order['reference_extra'], order['order_status'], order['notes'], order['shipping_notes'], 
                order['picking_notes'], order['warehouse_id'], order['ship_to'], order['bill_to'], 
                order['shipment_id'], order['total_amount'], order['total_discount'], order['total_tax'], 
                order['total_surcharge'], order['created_at'], order['updated_at']
            ))

            for item in order['items']:
                cursor.execute(f"""
                    INSERT INTO {order_items_table} (order_id, item_id, amount) 
                    VALUES (?, ?, ?)
                """, (order['id'], item['item_id'], item['amount']))

        conn.commit()
        print(f"Data successfully inserted into the '{orders_table}' and '{order_items_table}' tables.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    finally:
        conn.close()


def create_shipments_table(db_name, json_relative_path):
    shipments_table = "shipments"
    shipment_items_table = "shipment_items"

    # Define table schemas
    shipments_columns = '''id INTEGER PRIMARY KEY, 
                           order_id INTEGER, 
                           source_id INTEGER, 
                           order_date TEXT, 
                           request_date TEXT, 
                           shipment_date TEXT, 
                           shipment_type TEXT, 
                           shipment_status TEXT, 
                           notes TEXT, 
                           carrier_code TEXT, 
                           carrier_description TEXT, 
                           service_code TEXT, 
                           payment_type TEXT, 
                           transfer_mode TEXT, 
                           total_package_count INTEGER, 
                           total_package_weight REAL, 
                           created_at TEXT, 
                           updated_at TEXT'''

    shipment_items_columns = '''id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                shipment_id INTEGER, 
                                item_id TEXT, 
                                amount INTEGER, 
                                FOREIGN KEY (shipment_id) REFERENCES shipments (id) ON DELETE CASCADE'''

    # Load data from JSON
    with open(json_relative_path, 'r') as file:
        data = json.load(file)

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        # Create the tables
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {shipments_table} ({shipments_columns});")
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {shipment_items_table} ({shipment_items_columns});")

        # Insert data into the shipments table
        for shipment in data:
            cursor.execute(f"""
                INSERT INTO {shipments_table} (id, order_id, source_id, order_date, request_date, 
                                               shipment_date, shipment_type, shipment_status, notes, 
                                               carrier_code, carrier_description, service_code, 
                                               payment_type, transfer_mode, total_package_count, 
                                               total_package_weight, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                shipment['id'], shipment['order_id'], shipment['source_id'], shipment['order_date'],
                shipment['request_date'], shipment['shipment_date'], shipment['shipment_type'],
                shipment['shipment_status'], shipment['notes'], shipment['carrier_code'],
                shipment['carrier_description'], shipment['service_code'], shipment['payment_type'],
                shipment['transfer_mode'], shipment['total_package_count'],
                shipment['total_package_weight'], shipment.get('created_at', datetime.now().isoformat()),
                shipment.get('updated_at', datetime.now().isoformat())
            ))

            # Get the shipment ID
            shipment_id = shipment['id']

            # Insert items into the shipment_items table
            for item in shipment['items']:
                cursor.execute(f"""
                    INSERT INTO {shipment_items_table} (shipment_id, item_id, amount) 
                    VALUES (?, ?, ?)
                """, (shipment_id, item['item_id'], item['amount']))
        
        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{shipments_table}' and '{shipment_items_table}' tables.")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_suppliers_table(db_name, json_relative_path):
    suppliers_table = "suppliers"

    # Define table schema
    suppliers_columns = '''id INTEGER PRIMARY KEY, 
                           code TEXT, 
                           name TEXT, 
                           address TEXT, 
                           address_extra TEXT, 
                           city TEXT, 
                           zip_code TEXT, 
                           province TEXT, 
                           country TEXT, 
                           contact_name TEXT, 
                           phonenumber TEXT, 
                           reference TEXT, 
                           created_at TEXT, 
                           updated_at TEXT'''

    # Load data from JSON
    with open(json_relative_path, 'r') as file:
        data = json.load(file)

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        # Create the suppliers table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {suppliers_table} ({suppliers_columns});")

        # Insert data into the suppliers table
        for supplier in data:
            cursor.execute(f"""
                INSERT INTO {suppliers_table} (id, code, name, address, address_extra, city, zip_code, 
                                               province, country, contact_name, phonenumber, reference, 
                                               created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                supplier['id'], supplier['code'], supplier['name'], supplier['address'], 
                supplier.get('address_extra', ''), supplier['city'], supplier['zip_code'], 
                supplier['province'], supplier['country'], supplier['contact_name'], 
                supplier['phonenumber'], supplier['reference'], 
                supplier.get('created_at', datetime.now().isoformat()), 
                supplier.get('updated_at', datetime.now().isoformat())
            ))

        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{suppliers_table}' table.")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def create_transfers_table(db_name, json_relative_path):
    transfers_table = "transfers"
    transfer_items_table = "transfer_items"

    # Define table schemas
    transfers_columns = '''id INTEGER PRIMARY KEY, 
                           reference TEXT, 
                           transfer_from INTEGER, 
                           transfer_to INTEGER, 
                           transfer_status TEXT, 
                           created_at TEXT, 
                           updated_at TEXT'''

    transfer_items_columns = '''id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                transfer_id INTEGER, 
                                item_id TEXT, 
                                amount INTEGER, 
                                FOREIGN KEY (transfer_id) REFERENCES transfers (id) ON DELETE CASCADE'''

    # Load data from JSON
    with open(json_relative_path, 'r') as file:
        data = json.load(file)

    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        # Create the transfers table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {transfers_table} ({transfers_columns});")

        # Create the transfer_items table
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {transfer_items_table} ({transfer_items_columns});")

        # Insert data into the transfers and transfer_items tables
        for transfer in data:
            # Insert into transfers table
            cursor.execute(f"""
                INSERT INTO {transfers_table} (id, reference, transfer_from, transfer_to, 
                                               transfer_status, created_at, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                transfer['id'], transfer['reference'], transfer['transfer_from'], transfer['transfer_to'],
                transfer['transfer_status'], transfer['created_at'], transfer['updated_at']
            ))

            # Insert into transfer_items table
            for item in transfer['items']:
                cursor.execute(f"""
                    INSERT INTO {transfer_items_table} (transfer_id, item_id, amount) 
                    VALUES (?, ?, ?)
                """, (
                    transfer['id'], item['item_id'], item['amount']
                ))

        # Commit changes
        conn.commit()
        print(f"Data successfully inserted into the '{transfers_table}' and '{transfer_items_table}' tables.")
    
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    
    finally:
        # Close the connection
        conn.close()


def load_data_from_json(json_relative_path):
    # Determine the absolute path of the JSON file based on the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, json_relative_path)

    # Open and read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    return data


if __name__ == '__main__':
    db_name = 'data/Cargohub.db'  # Database name

    create_clients_table(db_name, 'data/clients.json')
    create_inventories_table(db_name, 'data/inventories.json')
    create_item_groups_table(db_name, 'data/item_groups.json')
    create_item_lines_table(db_name, 'data/item_lines.json')
    create_item_types_table(db_name, 'data/item_types.json')
    create_items_table(db_name, 'data/items.json')
    create_locations_table(db_name, 'data/locations.json')
    # create_orders_table(db_name, 'data/orders.json')
    create_shipments_table(db_name, 'data/shipments.json')
    create_suppliers_table(db_name, 'data/suppliers.json')
    create_transfers_table(db_name, 'data/transfers.json')
