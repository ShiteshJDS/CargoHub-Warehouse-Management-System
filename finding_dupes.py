import json
from collections import Counter
import os

def load_data_from_json(json_relative_path):
    # Determine the absolute path of the JSON file based on the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, json_relative_path)

    # Open and read the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    return data

def check_for_duplicates(json_path):
    """
    Checks for duplicate `id` values in the orders JSON file.

    :param json_path: Path to the JSON file containing orders data.
    :return: List of duplicate IDs, if any.
    """
    data = load_data_from_json(json_path)
    
    # Extract all IDs
    ids = [order['id'] for order in data]
    
    # Find duplicates
    id_counts = Counter(ids)
    duplicates = [item for item, count in id_counts.items() if count > 1]
    
    if duplicates:
        print(f"Duplicate IDs found in {json_path}: {duplicates}")
    else:
        print(f"No duplicate IDs found in {json_path}.")
    
    return duplicates

# Example usage:
# json_file_names = ["clients.json", "inventories.json", "item_groups.json", "item_lines.json", "item_types.json", "locations.json", "suppliers.json", "transfers.json", "warehouses.json", "shipments.json"]

# for json_file in json_file_names:
#     check_for_duplicates(f"data/{json_file}")

check_for_duplicates("data/orders.json")
