import asyncio
import aiohttp
import time
import csv
import json
import os
import sqlite3

# Load endpoints from Endpoints.json
current_dir = os.path.dirname(os.path.abspath(__file__))
endpoints_file_path = os.path.join(current_dir, "Endpoints.json")

with open(endpoints_file_path, 'r') as file:
    endpoints = json.load(file)

output_file = "performance_async_results.csv"

# Connect to the SQLite database
db_path = os.path.join(current_dir, "../../../data/Cargohub.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Asynchronous function to test endpoint performance
async def test_endpoint_performance(session, method, url, headers, data=None):
    try:
        start_time = time.time()

        # Perform the appropriate HTTP request based on the method
        if method == "GET":
            async with session.get(url, headers=headers) as response:
                await response.text()  # Read response
                status_code = response.status
        elif method == "POST":
            async with session.post(url, headers=headers, json=data) as response:
                await response.text()
                status_code = response.status
        elif method == "PUT":
            async with session.put(url, headers=headers, json=data) as response:
                await response.text()
                status_code = response.status
        elif method == "DELETE":
            async with session.delete(url, headers=headers) as response:
                await response.text()
                status_code = response.status
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        end_time = time.time()
        elapsed_time = end_time - start_time
        return elapsed_time, status_code

    except aiohttp.ClientError as e:
        return time.time() - start_time, f"Error: {e}"

# Asynchronous function to process each endpoint
async def process_endpoint(session, endpoint):
    method = endpoint['method']
    url = endpoint['url']
    headers = endpoint['headers']
    data = endpoint.get('data')

    print(f"Testing {method} {url}")
    elapsed_time, status_code = await test_endpoint_performance(session, method, url, headers, data)
    print(f"Time: {elapsed_time:.2f}s | Status Code: {status_code}")
    return [method, url, elapsed_time, status_code]

# Asynchronous function to handle the entire process
async def main():
    results = []

    async with aiohttp.ClientSession() as session:
        for endpoint_group in endpoints:
            tasks = []
            for endpoint in endpoint_group:
                task = process_endpoint(session, endpoint)
                tasks.append(task)

            # Gather all results concurrently
            endpoint_results = await asyncio.gather(*tasks)
            results.extend(endpoint_results)

    save_results_to_csv(results, output_file)
    print(f"Performance results saved to {output_file}")

def save_results_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Method", "URL", "Response Time (s)", "Status Code"])
        writer.writerows(results)

if __name__ == "__main__":
    asyncio.run(main())