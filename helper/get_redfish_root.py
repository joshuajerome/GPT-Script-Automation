import requests
import json

def get_root_url(idrac_ip, idrac_username, idrac_password, verify_cert=False):
    url = f"https://{idrac_ip}/redfish/v1"
    response = requests.get(url, verify=verify_cert, auth=(idrac_username, idrac_password))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve root URL. Status code: {response.status_code}")
        return None

def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def initialize():
    confidential = 'confidential.json'
    with open(confidential) as file:
        return json.load(file)
    
data = initialize()

if __name__ == "__main__":
    idrac_ip = data['IP']
    idrac_username = data['USER']
    idrac_password = data['PASS']
    output_file = "root_url.json"

    root_url = get_root_url(idrac_ip, idrac_username, idrac_password)
    
    if root_url is not None:
        save_to_json(root_url, output_file)
        print(f"Root URL saved to {output_file}")
