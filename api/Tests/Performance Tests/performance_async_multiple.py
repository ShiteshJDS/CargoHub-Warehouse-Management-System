import asyncio
import aiohttp
import json
import csv
import os
import time
import random

# Load endpoints from Endpoints.json
current_dir = os.path.dirname(os.path.abspath(__file__))
endpoints_file_path = os.path.join(current_dir, "Endpoints.json")

with open(endpoints_file_path, 'r') as file:
    endpoints = json.load(file)

# File to store performance results
output_file = "performance_async_multiple_results.csv"

async def test_endpoint_performance(session, method, url, headers, data=None):
    try:
        # Start timing the request
        start_time = time.time()

        # Perform the appropriate HTTP request based on the method
        if method == "GET":
            async with session.get(url, headers=headers) as response:
                await response.text()  # Read the response content
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
        
        # Calculate elapsed time
        end_time = time.time()
        elapsed_time = end_time - start_time
        return elapsed_time, status_code

    except Exception as e:
        print(f"Error with {url}: {e}")
        return None, "Error"

async def process_endpoint(endpoint):
    # Generate a random number of requests between 5 and 10
    num_requests = random.randint(5, 10)

    async with aiohttp.ClientSession() as session:
        method = endpoint['method']
        url = endpoint['url']
        headers = endpoint['headers']
        data = endpoint.get('data')

        # Collect results for all requests
        total_requests = num_requests
        successful_requests = 0
        failed_requests = 0
        total_time = 0

        tasks = []
        for _ in range(num_requests):
            task = asyncio.create_task(test_endpoint_performance(session, method, url, headers, data))
            tasks.append(task)

        # Gather the results from all requests
        results = await asyncio.gather(*tasks)

        # Process the results
        for elapsed_time, status_code in results:
            if status_code == "Error":
                failed_requests += 1
            else:
                successful_requests += 1
                total_time += elapsed_time

        # Calculate the average response time
        average_response_time = total_time / successful_requests if successful_requests > 0 else 0

        return {
            "url": url,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "average_response_time": average_response_time
        }

def save_results_to_csv(results, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Total Requests", "Successful Requests", "Failed Requests", "Average Response Time (s)"])
        for result in results:
            writer.writerow([
                result['url'],
                result['total_requests'],
                result['successful_requests'],
                result['failed_requests'],
                f"{result['average_response_time']:.2f}"
            ])

async def main():
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
            result = await process_endpoint(endpoint)  # Await the coroutine
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
    asyncio.run(main())