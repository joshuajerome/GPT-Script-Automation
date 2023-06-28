import utility
import requests
import warnings

# merging dependent urls together
from urllib.parse import urljoin

# printing progress bar to console
from tqdm import tqdm

# timing runtime
import time

warnings.filterwarnings("ignore")

def traverse_tree(base_uri, session, output_file, visited=None, indent=0):
    if visited is None:
        visited = set()

    if base_uri in visited:
        return

    visited.add(base_uri)

    response = session.get(base_uri, verify=False)  # Disable SSL certificate verification
    if response.status_code == 200:
        data = response.json()
        for key, value in tqdm(data.items(), desc=f"Traversing {base_uri}", unit="nodes", dynamic_ncols=True):
            line_prefix = '┃   ' * indent + '┣━━ ' if indent > 0 else ''
            uri = None
            if isinstance(value, dict):
                if '@odata.id' in value:
                    uri = value['@odata.id']
                elif 'Members' in value and isinstance(value['Members'], list):
                    uri = value['Members'][0]['@odata.id'] if len(value['Members']) > 0 else ''
            output_file.write(f'{line_prefix}{key} \t({base_uri})\n')

            if isinstance(value, dict) and '@odata.id' in value:
                subdir_uri = value['@odata.id']
                complete_uri = urljoin(base_uri, subdir_uri)
                try:
                    traverse_tree(complete_uri, session, output_file, visited, indent + 1)
                except Exception as e:
                    output_file.write('┃   ' * (indent + 1) + f'Error: {str(e)}\n')
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict) and '@odata.id' in item:
                        subdir_uri = item['@odata.id']
                        complete_uri = urljoin(base_uri, subdir_uri)
                        try:
                            traverse_tree(complete_uri, session, output_file, visited, indent + 1)
                        except Exception as e:
                            output_file.write('┃   ' * (indent + 1) + f'Error: {str(e)}\n')
    else:
        output_file.write(f'Failed to access {base_uri}. Status code: {response.status_code}\n')


def main():
    data = utility.initialize('confidential.json')
    idrac_ip = data['IP']
    idrac_username = data['USER']
    idrac_password = data['PASS']

    base_uri = f"https://{idrac_ip}/redfish/v1/"
    session = requests.Session()
    session.auth = (idrac_username, idrac_password)

    output_filename = 'redfish_tree2.txt'
    with open(output_filename, 'w') as output_file:
        output_file.write("┣━━ Root\n")  # Add the root node manually
        traverse_tree(base_uri, session, output_file)

    print(f"Traversal completed. Tree structure saved in {output_filename}.")


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    print(f"\nScript runtime: {end - start}")
