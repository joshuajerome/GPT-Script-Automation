import requests
import json

def initialize():
    confidential = 'confidential.json'
    with open(confidential) as file:
        return json.load(file)
    
data = initialize()

idrac_ip = data['IP']  # Replace with the actual iDRAC IP address

# Make a GET request to the base Redfish API URL
base_url = f'https://{idrac_ip}/redfish/v1'
response = requests.get(base_url, verify=False)

# Check if the GET request was successful (status code 200)
if response.status_code == 200:
    # Parse the response JSON
    data = response.json()

    # Perform a recursive search through all paths within the JSON structure
    desired_url = None

    def search_urls(obj, target_resource):
        if isinstance(obj, dict):
            if '@odata.id' in obj and target_resource in json.dumps(obj):
                return obj['@odata.id']
            else:
                for key, value in obj.items():
                    result = search_urls(value, target_resource)
                    if result:
                        return result
        elif isinstance(obj, list):
            for item in obj:
                result = search_urls(item, target_resource)
                if result:
                    return result

    desired_resource = 'fan'
    desired_url = search_urls(data, desired_resource)

    # Process the desired URL
    if desired_url:
        print('Desired URL found:', desired_url)
        # Perform further actions with the URL as needed
    else:
        print('Desired URL not found.')

else:
    print('GET request failed with status code:', response.status_code)