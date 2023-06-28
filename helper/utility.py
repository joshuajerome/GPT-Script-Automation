#!/usr/bin/python3

import base64
from datetime import datetime
import json
import os
import requests
import shutil
import sys

#-------------------------------------------------------------------------------------------------------------------------------------------#
#                                                    File Utility Functions                                                                 #
#-------------------------------------------------------------------------------------------------------------------------------------------#

# returns a JSON file as an accessible object
def initialize(filename):
    with open(filename) as file:
        return json.load(file)
    
# saves data as a JSON file, to be used when data stores a JSON
def save_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# generates a file named base_timestamp_.extension
def generate_comparison_file(base, extension):
    current_time = datetime.now().strftime("%H%M%S")
    output_file = f'{base}_{current_time}.{extension}'    
    return output_file

# Write file names to name.extension
def write_data_to_file(data, name):
    with open(f"{name}", "w") as file:
        for filename in data:
            file.write(filename + "\n")

# Read filenames from filenames.txt
def read_data_from_file(filename):
    with open(f"{filename}", "r") as file:
        data = file.read().splitlines()
    return data

#-------------------------------------------------------------------------------------------------------------------------------------------#
#                                                      OS Utility Functions                                                                 #
#-------------------------------------------------------------------------------------------------------------------------------------------#

# creates a local folder
def create_local_folder(local_folder_path):
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)
    else:
        shutil.rmtree(local_folder_path)
        os.makedirs(local_folder_path)

#-------------------------------------------------------------------------------------------------------------------------------------------#
#                                                  GitHub API Utility Functions                                                             #
#-------------------------------------------------------------------------------------------------------------------------------------------#

# Check validity of github api access token
def validate_github_api_token(token):
    headers = {
        'Authorization': f'Token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get('https://api.github.com/user', headers=headers)

    if response.status_code == 200:
        print('GitHub API Token is valid')
    else:
        print('GitHub API Token is valid. Either your token has expired or you have reached the Request Rate Limit (5k/hr). Please update your GitHub API Token in confidential.json or try again later!')
        sys.exit()

# Fetch folder from GitHub (only required if storing the filenames for example)
def fetch_folder(repo_owner, repo_name, folder_path, access_token, log_file):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    response_json = response.json()

    if isinstance(response_json, list):
        file_names = [item["name"] for item in response_json if item["type"] == "file"]
        return file_names
    else:
        log_file.write(f"Error fetching file names: {response_json.get('message', 'Unknown error')}\n")

# Fetch file contents from GitHub
def fetch_file_contents(repo_owner, repo_name, folder_path, filename, access_token, log_file):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}/{filename}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    response_json = response.json()

    if "content" in response_json:
        content = response_json["content"]
        decoded_content = base64.b64decode(content).decode('utf-8')
        return decoded_content
    else:
        log_file.write(f"Error fetching file: {response_json.get('message', 'Unknown error')}\n")

