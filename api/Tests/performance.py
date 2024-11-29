import time
import requests
import csv
import json
import os

# Load endpoints from Endpoints.json
current_dir = os.path.dirname(os.path.abspath(__file__))
endpoints_file_path = os.path.join(current_dir, "Endpoints.json")

with open(endpoints_file_path, 'r') as file:
    endpoints = json.load(file)

# File to store performance results
output_file = "performance_results.csv"

def test_endpoint_performance(method, url, headers, data=None):
    response = None
    try:
        if method == "GET":
            start_time = time.time()
            response = requests.get(url, headers=headers)
        elif method == "POST":
            start_time = time.time()
            response = requests.post(url, headers=headers, data=data)
        elif method == "PUT":
            start_time = time.time()
            response = requests.put(url, headers=headers, data=data)
        elif method == "DELETE":
            start_time = time.time()
            response = requests.delete(url, headers=headers)
        else:
            start_time = time.time()
            raise ValueError(f"Unsupported HTTP method: {method}")
    except requests.RequestException as e:
        start_time = time.time()
        return time.time() - start_time, f"Error: {e}"
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time, response.status_code

def save_results_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Method", "URL", "Response Time (s)", "Status Code"])
        writer.writerows(results)

def main():
    json_file_names = ["clients.json", "inventories.json", "item_groups.json", "item_lines.json", "item_types.json", "items.json", "locations.json", "orders.json", "suppliers.json", "transfers.json", "warehouses.json", "shipments.json"]
    results = []  # Initialize results before the loop

    # Iterate over json_file_names and corresponding endpoints
    for i in range(len(json_file_names)):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, "../../data", json_file_names[i])

        # Load the JSON file
        with open(json_file_path, 'r') as file:
            BackupJson = json.load(file)

        # Process each endpoint in the corresponding group
        for endpoint in endpoints[i]:
            method = endpoint['method']
            url = endpoint['url']
            headers = endpoint['headers']
            data = endpoint.get('data')

            print(f"Testing {method} {url}")
            elapsed_time, status_code = test_endpoint_performance(method, url, headers, data)
            print(f"Time: {elapsed_time:.2f}s | Status Code: {status_code}")

            results.append([method, url, elapsed_time, status_code])

        # Save the original JSON back to file
        with open(json_file_path, 'w') as file:
            json.dump(BackupJson, file, indent=4)

    # Save results to a CSV file
    output_file = "performance_results.csv"
    save_results_to_csv(results, output_file)
    print(f"Performance results saved to {output_file}")

if __name__ == "__main__":
    main()