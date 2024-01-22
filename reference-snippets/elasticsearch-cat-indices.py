import csv
import re
from getpass import getpass

import requests


def fetch_es_data(es_url: str, username: str, password: str):
    """
    Fetch data from Elasticsearch using a GET request.

    Args:
    es_url (str): URL of the Elasticsearch instance.
    username (str): Username for Elasticsearch authentication.
    password (str): Password for Elasticsearch authentication.

    Returns:
    requests.Response: The response object from the GET request.
    """

    # Perform a GET request to the Elasticsearch _cat/indices endpoint.
    # The authentication credentials are passed for accessing the server.
    return requests.get(f"{es_url}/_cat/indices?v", auth=(username, password))


def parse_size(size_str: str):
    """
    Convert a size string to bytes. The input string is expected to be binary (e.g., '10KiB', not '10kB')

    Args:
    size_str (str): The string representing the size. Examples: '10kb', '2mb'.

    Returns:
    float: The size in bytes.
    """

    # Define the conversion units from various size units to bytes.
    size_units = {"kb": 1024, "mb": 1024**2, "gb": 1024**3, "tb": 1024**4, "b": 1}

    # Normalize the size string for consistent parsing.
    size_str = size_str.lower().replace(",", ".")

    # Extract the number and unit from the size string and calculate the size in bytes.
    for unit in size_units:
        if unit in size_str:
            return float(re.findall(r"\d+\.?\d*", size_str)[0]) * size_units[unit]
    return 0.0


def process_es_indices(es_url: str, output_csv: str):
    """
    Fetch Elasticsearch indices data and write a summary to a CSV file.

    Args:
    es_url (str): URL of the Elasticsearch instance.
    output_csv (str): File path for the output CSV file.
    """

    # Prompt the user for Elasticsearch credentials.
    username = input("Enter Elasticsearch username: ")
    password = getpass("Enter Elasticsearch password: ")

    # Fetch data from the Elasticsearch instance.
    response = fetch_es_data(es_url, username, password)
    if response.status_code != 200:
        print(f"Error fetching data from Elasticsearch: {response.text}")
        return

    # Split the response text into individual lines for further processing.
    lines = response.text.strip().split("\n")

    data_list = []
    # Extract headers (column names) from the first line of the response.
    headers_list = lines[0].split()

    # Convert each line of data into a dictionary and append to the data list.
    for line in lines[1:]:
        line = line.split()
        data_list.append(dict(zip(headers_list, line[0:])))

    # Convert size values in the data list from strings to bytes.
    for data in data_list:
        data["pri.store.size"] = parse_size(data["pri.store.size"])
        data["store.size"] = parse_size(data["store.size"])
        data["dataset.size"] = parse_size(data["dataset.size"])

    # Write the processed data to a CSV file.
    with open(output_csv, "w", newline="") as file:
        # Create a csv.DictWriter object to write dictionaries to a CSV.
        writer = csv.DictWriter(file, fieldnames=data_list[0].keys())

        # Write column headers to the CSV file.
        writer.writeheader()

        # Write each row of data to the CSV file.
        for row in data_list:
            writer.writerow(row)


# Main script execution
# Prompt the user to enter the Elasticsearch URL.
es_url = getpass("Enter Elasticsearch URL: ")  # Securely collect Elasticsearch URL
output_csv = "output.csv"  # Define the output CSV file name

# Process and output the Elasticsearch indices data to the CSV file.
process_es_indices(es_url, output_csv)
