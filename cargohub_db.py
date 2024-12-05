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
    json_file_names = ["clients.json", "inventories.json", "item_groups.json", "item_lines.json", "item_types.json", "items.json", "locations.json", "orders.json", "shipments.json", "suppliers.json", "transfers.json", "warehouses.json"]

    create_clients_table(db_name, 'data/clients.json')
