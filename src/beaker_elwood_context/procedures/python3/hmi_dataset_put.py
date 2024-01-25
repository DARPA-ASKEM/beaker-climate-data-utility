import os
import requests

# Binary data bytes
xarray_dataset = {{data}}  # Replace with your binary data

if not isinstance(xarray_dataset, bytes):
    xarray_dataset = xarray_dataset.to_netcdf()

# Get the HMI_SERVER endpoint and auth token from the environment variable
hmi_server = os.getenv('HMI_SERVER')
auth_token = os.getenv('BASIC_AUTH_TOKEN')

# Define the id and filename dynamically
id = {{id}}
filename = {{filename}}

# Prepare the request payload
payload = {'id': id, 'filename': filename}
files = {'file': file_bytes}

# Set the headers with the basic auth token
headers = {'Authorization': f'Basic {auth_token}'}

# Make the HTTP PUT request to upload the file bytes
url = f'{hmi_server}/{id}/upload-csv'
response = requests.put(url, headers=headers, data=payload, files=files)

# Check the response status code
if response.status_code == 200:
    message = response.json()
else:
    message = f'File upload failed with status code {response.status_code}.'
    if response.text:
        message += f' Response message: {response.text}'

message
