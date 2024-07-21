import requests
import csv

# URL for the GET request
url = "https://mp3quran.net/api/v3/radios"

# Send the GET request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    data = response.json()

    # Specify the CSV file name
    csv_file = 'radios.csv'

    # CSV column headers based on the keys in the JSON
    columns = ['id', 'name', 'url', 'recent_date']

    # Open a CSV file for writing
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=columns)

        # Write the header to the CSV file
        writer.writeheader()

        # Write data to the CSV file
        for radio in data['radios']:
            writer.writerow(radio)

    print(f"Data saved to {csv_file}")
else:
    print(f"Failed to retrieve data: {response.status_code}")

