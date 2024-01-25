import os
import requests

# Get the HMI_SERVER endpoint from the environment variable
hmi_server = os.getenv('HMI_SERVER')

# Get the basic auth token from the environment variable
auth_token = os.getenv('BASIC_AUTH_TOKEN')

# Define the id dynamically
id = {{id}}

# Prepare the request URL
url = f'{hmi_server}/{id}/download-csv'

# Set the headers with the basic auth token
headers = {
    'Authorization': f'Basic {auth_token}',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

# Define the payload with the parameters
payload = {'id': id, 'filename': {{filename}}}

# Make the HTTP GET request to retrieve the dataset
response = requests.get(url, headers=headers, params=payload)

# Check the response status code
if response.status_code == 200:
    message = response.json()
else:
    message = f'Dataset retrieval failed with status code {response.status_code}.'
    if response.text:
        message += f' Response message: {response.text}'

message
