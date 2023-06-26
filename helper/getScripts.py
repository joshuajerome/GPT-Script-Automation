#!/usr/bin/env python

import requests
import base64
import os
import shutil
import re
import json

def initialize():
    confidential = 'confidential.json'
    with open(confidential) as file:
        return json.load(file)
    
data = initialize()

# GitHub repo details
repo_owner = data['repo_owner']
repo_name = data['repo_name']
folder_path = data['folder_path']

# Generated personal access token; Request Rate Limit: 5k/hr (expires 07/19/23)
access_token= data['github_api_access_token']

# Regex pattern that will be matched against file names. For matches, that file will be pulled
pattern= data['filename_start_pattern']

# Create local folder to store all requested files 
local_folder_path = data['generated_folder_with_fetched_scripts']

# Fetch file names from GitHub API
def fetch_file_names(repo_owner, repo_name, folder_path):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    response_json = response.json()

    if isinstance(response_json, list):
        # Specify what kind of script to fetch
        file_names = [item["name"] for item in response_json if item["type"] == "file"]
        return file_names
    else:
        print(f"Error fetching file names: {response_json.get('message', 'Unknown error')}")

# Fetch file contents from GitHub API
def fetch_file_contents(filename):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}/{filename}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(api_url, headers=headers)
    response_json = response.json()

    if "content" in response_json:
        content = response_json["content"]
        decoded_content = base64.b64decode(content).decode('utf-8')
        return decoded_content
    else:
        print(f"Error fetching file: {response_json.get('message', 'Unknown error')}")

# Write file names to filenames.txt
def create_filenames_txt(file_names):
    with open("filenames.txt", "w") as file:
        for filename in file_names:
            file.write(filename + "\n")

# Read filenames from filenames.txt
def read_filenames_txt():
    with open("filenames.txt", "r") as file:
        filenames = file.read().splitlines()
    return filenames

# Populate "scripts" folder
def create_local_folder():
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)
    else:
        # Empty the "scripts" directory
        shutil.rmtree(local_folder_path)
        os.makedirs(local_folder_path)

def write_file_contents_to_local_folder():
    filenames = read_filenames_txt()
    # Fetch each file as specified in filenames.txt and store them in the "scripts" folder
    for filename in filenames:
        matches = re.findall(pattern, filename)
        if not matches: 
            print(f"Specified regex pattern ({pattern}) not matched for: {filename}")
        else:
            file_contents = fetch_file_contents(filename)
            if file_contents:
                # Write file contents to a file in the "scripts" folder
                file_path = os.path.join(local_folder_path, filename)
                with open(file_path, "w") as file:
                    file.write(file_contents)

                print(f"Fetched {filename} and stored it as {file_path}")

def getScripts():
    filenames = fetch_file_names(repo_owner, repo_name, folder_path)
    create_filenames_txt(filenames)
    create_local_folder()

    # internally matches the specified filename start pattern
    write_file_contents_to_local_folder()

def main():
    getScripts()

if __name__ == "__main__":
    main()