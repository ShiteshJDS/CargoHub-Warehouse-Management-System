import json

def reset_and_increment_ids(json_file_path):
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        # Check if the data is a list of objects
        if not isinstance(data, list):
            print("The JSON file should contain a list of objects.")
            return

        # Reset and increment the 'id' field for each object
        for index, item in enumerate(data, start=1):
            if isinstance(item, dict):
                item['id'] = index
            else:
                print(f"Skipping non-dict item: {item}")

        # Write the modified data back to the JSON file
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print("IDs have been reset and incremented starting from 1 successfully.")

    except FileNotFoundError:
        print(f"The file {json_file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"The file {json_file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
json_file_path = 'data/orders.json'  # Replace with the path to your JSON file
reset_and_increment_ids(json_file_path)
