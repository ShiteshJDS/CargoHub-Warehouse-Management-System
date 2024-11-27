import time
import requests
import csv
import subprocess

# Define endpoints with methods, headers, and payloads
endpoints = [
    # Clients Endpoints
    {
        "method": "GET",
        "url": "http://localhost:3000/api/v1/clients",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": None,
    },
    {
        "method": "GET",
        "url": "http://localhost:3000/api/v1/clients/1",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": None,
    },
    {
        "method": "GET",
        "url": "http://localhost:3000/api/v1/clients/1/orders",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": None,
    },
    {
        "method": "PUT",
        "url": "http://localhost:3000/api/v1/clients/1",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": """{
            "id": 1,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "2010-04-28 02:22:53",
            "updated_at": "2022-02-09 20:22:35"
        }""",
    },
    {
        "method": "POST",
        "url": "http://localhost:3000/api/v1/clients",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": """{
            "id": 1,
            "name": "Raymond Inc",
            "address": "1296 Daniel Road Apt. 349",
            "city": "Pierceview",
            "zip_code": "28301",
            "province": "Colorado",
            "country": "United States",
            "contact_name": "Bryan Clark",
            "contact_phone": "242.732.3483x2573",
            "contact_email": "robertcharles@example.net",
            "created_at": "2010-04-28 02:22:53",
            "updated_at": "2022-02-09 20:22:35"
        }""",
    },
    {
        "method": "DELETE",
        "url": "http://localhost:3000/api/v1/clients/1",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
        },
        "data": None,
    },
    # Inventories Endpoints
    {
        "method": "GET",
        "url": "http://localhost:3000/api/v1/inventories",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": None,
    },
    {
        "method": "GET",
        "url": "http://localhost:3000/api/v1/inventories/1",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": None,
    },
    {
        "method": "PUT",
        "url": "http://localhost:3000/api/v1/inventories/1",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": """{
            "id": 1,
            "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
            ],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "2015-02-19 16:08:24",
            "updated_at": "2015-09-26 06:37:56"
        }""",
    },
    {
        "method": "POST",
        "url": "http://localhost:3000/api/v1/inventories",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json",
        },
        "data": """{
            "id": 1,
            "item_id": "P000001",
            "description": "Face-to-face clear-thinking complexity",
            "item_reference": "sjQ23408K",
            "locations": [
                3211,
                24700,
                14123,
                19538,
                31071,
                24701,
                11606,
                11817
            ],
            "total_on_hand": 262,
            "total_expected": 0,
            "total_ordered": 80,
            "total_allocated": 41,
            "total_available": 141,
            "created_at": "2015-02-19 16:08:24",
            "updated_at": "2015-09-26 06:37:56"
        }""",
    },
    {
        "method": "DELETE",
        "url": "http://localhost:3000/api/v1/inventories/1",
        "headers": {
            "API_KEY": "a1b2c3d4e5",
        },
        "data": None,
    },
]

# File to store performance results
output_file = "performance_results.csv"

def test_endpoint_performance(method, url, headers, data=None):
    start_time = time.time()
    response = None
    try:
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
    except requests.RequestException as e:
        return time.time() - start_time, f"Error: {e}"
    
    end_time = time.time()
    elapsed_time = end_time - start_time

    return elapsed_time, response.status_code

def save_results_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Method", "URL", "Response Time (s)", "Status Code"])
        writer.writerows(results)

def save_git_state():
    """
    Save the current state of the repository before running tests.
    """
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Save clean state before tests"], check=True)
        print("Git state saved.")
    except subprocess.CalledProcessError as e:
        print(f"Error saving git state: {e}")

def revert_git_state():
    """
    Revert to the last committed state using Git.
    """
    try:
        subprocess.run(["git", "reset", "--hard"], check=True)
        print("Reverted to last committed state.")
    except subprocess.CalledProcessError as e:
        print(f"Error reverting git state: {e}")

def main():
    try:
        # Save initial Git state
        save_git_state()

        # Run endpoint performance tests
        results = []
        for endpoint in endpoints:
            method = endpoint['method']
            url = endpoint['url']
            headers = endpoint['headers']
            data = endpoint.get('data')
            
            print(f"Testing {method} {url}")
            elapsed_time, status_code = test_endpoint_performance(method, url, headers, data)
            print(f"Time: {elapsed_time:.2f}s | Status Code: {status_code}")
            
            results.append([method, url, elapsed_time, status_code])
        
        # Save results to CSV
        save_results_to_csv(results, output_file)
        print(f"Performance results saved to {output_file}")
    finally:
        # Ensure changes are reverted after tests
        revert_git_state()

if __name__ == "__main__":
    main()
