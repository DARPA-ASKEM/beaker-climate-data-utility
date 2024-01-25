import requests
import os
from datetime import datetime

# Set the current datetime
current_datetime = datetime.now().isoformat()

# Define the payload
payload = {
    "userId": "service-user",
    "name": "{{identifier}} dataset transformed",
    "description": "This dataset was generated by beaker after a transformation operation occurred on an original dataset {{identifier}}.",
    "dataSourceDate": "",
    "fileNames": ["{{identifier}}"],
    "datasetUrl": "",
    "columns": [
        {
            "name": "string",
            "dataType": "UNKNOWN",
            "formatStr": "string",
            "annotations": ["string"],
            "metadata": {},
            "grounding": {"identifiers": {}, "context": {}},
            "description": "string",
        }
    ],
    "metadata": {},
    "source": "string",
    "grounding": {"identifiers": {}, "context": {}},
}

payload["dataSourceDate"] = current_datetime

# Get the HMI_SERVER environment variable
hmi_server = os.getenv("HMI_SERVER")
auth_token = os.getenv("BASIC_AUTH_TOKEN")

# Set the headers
headers = {
    "accept": "application/json",
    "Authorization": f"Basic {auth_token}",
    "Content-Type": "application/json",
}

# Send the POST request
response = requests.post(hmi_server, json=payload, headers=headers)

# Check the response status code
if response.status_code == 200:
    message = response.json()
else:
    message = f'File upload failed with status code {response.status_code}.'
    if response.text:
        message += f' Response message: {response.text}'

message
