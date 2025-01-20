import time
import requests
import csv
import json
import os
import sqlite3

# Load endpoints from Endpoints.json
current_dir = os.path.dirname(os.path.abspath(__file__))
endpoints_file_path = os.path.join(current_dir, "Endpoints.json")

with open(endpoints_file_path, 'r') as file:
    endpoints = json.load(file)

# File to store performance results
output_file = "performance_results.csv"

# Connect to the SQLite database
db_path = os.path.join(current_dir, "../../../data/Cargohub.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def test_endpoint_performance(method, url, headers, data=None):
    response = None
    try:
        if method == "GET":
            start_time = time.time()
            response = requests.get(url, headers=headers)
        elif method == "POST":
            start_time = time.time()
            response = requests.post(url, headers=headers, json=data)
        elif method == "PUT":
            start_time = time.time()
            response = requests.put(url, headers=headers, json=data)
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
        writer.writerow(["Method", "URL", "Elapsed Time", "Status Code"])
        writer.writerows(results)

def main():
    results = []
    for endpoint_group in endpoints:
        for endpoint in endpoint_group:
            method = endpoint['method']
            url = endpoint['url']
            headers = endpoint['headers']
            data = endpoint.get('data')

            print(f"Testing {method} {url}")
            elapsed_time, status_code = test_endpoint_performance(method, url, headers, data)
            print(f"Time: {elapsed_time:.2f}s | Status Code: {status_code}")

            results.append([method, url, elapsed_time, status_code])

    save_results_to_csv(results, output_file)
    print(f"Performance results saved to {output_file}")

if __name__ == "__main__":
    main()