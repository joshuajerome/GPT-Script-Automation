import requests
import utility
import argparse
import utility

def get_root_url(idrac_ip, idrac_username, idrac_password, verify_cert=False):
    url = f"https://{idrac_ip}/redfish/v1/Chassis/"
    response = requests.get(url, verify=verify_cert, auth=(idrac_username, idrac_password))
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve root URL. Status code: {response.status_code}")
        return None
    
data = utility.initialize("confidential.json")

if __name__ == "__main__":
    idrac_ip = data['IP']
    idrac_username = data['USER']
    idrac_password = data['PASS']
    output_file = "root_url.json"

    parser = argparse.ArgumentParser()
    parser.add_argument('--compare',action='store_true', help='Compare flag')
    args = parser.parse_args()

    root_url = get_root_url(idrac_ip, idrac_username, idrac_password)
    
    if root_url is not None:
        if args.compare:
            output_file = utility.generate_comparison_file("root_url",".json")

        utility.save_to_json(root_url, output_file)
        print(f"Root URL saved to {output_file}")
