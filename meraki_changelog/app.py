import requests
import json
import time

api_key = 'x'  # Replace with your API key
organization_id = 'x'  # Replace with your organizationId
timespan = 60  # The timespan in seconds

# Set the API endpoint
url = f"https://api.meraki.com/api/v1/organizations/{organization_id}/configurationChanges"

# Set the headers for the API request
headers = {
    'X-Cisco-Meraki-API-Key': api_key,
    'Content-Type': 'application/json'
}

# Set the query parameters
params = {'timespan': timespan}

while True:  # Infinite loop
    # Send the API request and get the response
    response = requests.get(url, headers=headers, params=params)

    # If the request was successful (status code 200), process the response
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if 'wan1' in item['oldValue'] or 'wan2' in item['oldValue'] or \
               'wan1' in item['newValue'] or 'wan2' in item['newValue']:
                print('WAN settings have been changed')
    else:
        print(f"Request failed with status code {response.status_code}")

    time.sleep(60)  # Wait for 60 seconds
