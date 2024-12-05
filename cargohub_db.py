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
