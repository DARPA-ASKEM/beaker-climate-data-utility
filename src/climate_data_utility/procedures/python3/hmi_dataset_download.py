import os
from io import BytesIO
import requests

from json import JSONDecodeError

import logging

import xarray


logger = logging.getLogger(__name__)

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

logger.error(f"response: {response}")

# Check the response status code
if response.status_code <= 300:
    message = f'Dataset retrieved successfully with status code {response.status_code}.'
    response.content
else:
    message = f'Dataset retrieval failed with status code {response.status_code}.'
    if response.text:
        message += f' Response message: {response.text}'
    message


dataset = xarray.open_dataset(BytesIO(response.content))

dataset
