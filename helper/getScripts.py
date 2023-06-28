#!/usr/bin/env python

import os
import re
import utility
    
data = utility.initialize('confidential.json')

# GitHub repo details
repo_owner = data['repo_owner']
repo_name = data['repo_name']
folder_path = data['folder_path']

# Generated personal access token; Request Rate Limit: 5k/hr (expires 07/19/23)
github_api_access_token = data['github_api_access_token']

# Regex pattern that will be matched against file names. For matches, that file will be pulled
pattern = data['filename_start_pattern']

# Create local folder to store all requested files 
local_folder_path = data['generated_folder_with_fetched_scripts']

# getScripts log file
log_file = open('getScripts_log.txt', 'w')

def write_file_contents_to_local_folder():
    filenames = utility.read_data_from_file('filenames.txt')
    # Fetch each file as specified in filenames.txt and store them in the "scripts" folder
    for filename in filenames:
        matches = re.findall(pattern, filename)
        if not matches: 
            log_file.write(f"Specified regex pattern ({pattern}) not matched for: {filename}\n")
        else:
            file_contents = utility.fetch_file_contents(repo_owner, repo_name, folder_path, filename, github_api_access_token, log_file)
            if file_contents:
                # Write file contents to a file in the "scripts" folder
                file_path = os.path.join(local_folder_path, filename)
                with open(file_path, "w") as file:
                    file.write(file_contents)

                log_file.write(f"Fetched {filename} and stored it as {file_path}\n")

def getScripts():
    # log file is opened at gobal level
    filenames = utility.fetch_folder(repo_owner, repo_name, folder_path, github_api_access_token, log_file)
    utility.write_data_to_file(filenames, 'filenames.txt')
    utility.create_local_folder(local_folder_path)

    # internally matches the specified filename start pattern
    write_file_contents_to_local_folder()
    log_file.close()

def main():
    print('Validating api tokens...')
    utility.validate_github_api_token(github_api_access_token)
    print('Fetching files...')
    getScripts()
    print('Execution complete! See getScripts.log for details.')

if __name__ == "__main__":
    main()