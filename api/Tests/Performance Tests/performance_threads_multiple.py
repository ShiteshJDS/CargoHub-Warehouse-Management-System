import time
import requests
import csv
import json
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load endpoints from Endpoints.json
current_dir = os.path.dirname(os.path.abspath(__file__))
endpoints_file_path = os.path.join(current_dir, "Endpoints.json")

with open(endpoints_file_path, 'r') as file:
    endpoints = json.load(file)

# File to store performance results
output_file = "performance_threads_multiple_results.csv"

def test_endpoint_performance(method, url, headers, data=None):
    """Test a single endpoint and measure the response time."""
    try:
        start_time = time.time()
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=data)
        elif method == "PUT":
            response = requests.put(url, headers=headers, data=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        elapsed_time = time.time() - start_time
        return elapsed_time, response.status_code
    except requests.RequestException as e:
        return None, f"Error: {e}"

def process_endpoint(endpoint):
    """Process an endpoint by sending multiple requests concurrently."""
    method = endpoint['method']
    url = endpoint['url']
    headers = endpoint['headers']
    data = endpoint.get('data')

    # Random number of requests between 5 and 10
    num_requests = random.randint(5, 10)

    # Prepare a list to store futures (asynchronous results)
    successful_requests = 0
    failed_requests = 0
    total_time = 0

    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [
            executor.submit(test_endpoint_performance, method, url, headers, data)
            for _ in range(num_requests)
        ]
        
        # Collect results from each future
        for future in as_completed(futures):
            elapsed_time, status_code = future.result()
            if isinstance(status_code, int) and status_code == 200:
                successful_requests += 1
            else:
                failed_requests += 1
            
            if elapsed_time is not None:
                total_time += elapsed_time

    # Calculate average response time
    average_response_time = total_time / num_requests if num_requests > 0 else 0

    return {
        'url': url,
        'total_requests': num_requests,
        'successful_requests': successful_requests,
        'failed_requests': failed_requests,
        'average_response_time': average_response_time
    }

def save_results_to_csv(results, filename):
    """Save the performance results to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Endpoint", "Total Requests", "Successful Requests", "Failed Requests", "Average Response Time (s)"])
        for result in results:
            writer.writerow([result['url'], result['total_requests'], result['successful_requests'],
                             result['failed_requests'], f"{result['average_response_time']:.2f}"])

def main():
    json_file_names = ["clients.json", "inventories.json", "item_groups.json", "item_lines.json", "item_types.json",
                       "items.json", "locations.json", "orders.json", "suppliers.json", "transfers.json", "warehouses.json", "shipments.json"]
    results = []

    # Itereren over json_file_names en bijbehorende endpoints
    for i, json_file_name in enumerate(json_file_names):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, "../../../data", json_file_name)

        # laad de JSON file
        with open(json_file_path, 'r') as file:
            BackupJson = json.load(file)

        for endpoint in endpoints[i]:
            print(f"Testing endpoint {endpoint['url']}")
            result = process_endpoint(endpoint)
            results.append(result)
            print(f"Endpoint: {result['url']}")
            print(f"Total Requests: {result['total_requests']}")
            print(f"Successful Requests: {result['successful_requests']}")
            print(f"Failed Requests: {result['failed_requests']}")
            print(f"Average Response Time: {result['average_response_time']:.2f} seconds")
            print("-" * 50)

        # Sla de originele JSON terug op in het bestand
        with open(json_file_path, 'w') as file:
            json.dump(BackupJson, file, indent=4)

    # Save naar CSV
    save_results_to_csv(results, output_file)
    print(f"Performance results saved to {output_file}")

if __name__ == "__main__":
    main()