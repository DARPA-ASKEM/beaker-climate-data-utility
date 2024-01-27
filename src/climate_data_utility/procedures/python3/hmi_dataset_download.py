import os
import requests

from json import JSONDecodeError

# Get the HMI_SERVER endpoint from the environment variable
hmi_server = os.getenv('HMI_SERVER')
auth_token = os.getenv('BASIC_AUTH_TOKEN')

# Set the username and password
username = os.getenv("HMI_SERVER_USER")
password = os.getenv("HMI_SERVER_PASSWORD")

# Define the id
id = "{{id}}"

# Prepare the request URL
url = f'{hmi_server}/datasets/{id}/download-file?filename={{filename}}'

# Make the HTTP GET request to retrieve the dataset
response = requests.get(url, auth=(username, password))

# Check the response status code
if response.status_code == 200:
    message = f'Dataset retrieved successfully with status code {response.status_code}. Use the variable "dataset" to access the raw data bytes.'
else:
    message = f'Dataset retrieval failed with status code {response.status_code}.'
    if response.text:
        message += f' Response message: {response.text}'

dataset = response.content

message
