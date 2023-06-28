#!/usr/bin/python3

import argparse
import requests
import warnings
import sys
import re
import logging
import getpass
import os
import json

warnings.filterwarnings("ignore")

def initialize():
    confidential = 'confidential.json'
    with open(confidential) as file:
        return json.load(file)
    
data = initialize()
idrac_ip = data['IP']
idrac_username = data['USER']
idrac_password = data['PASS']

parser = argparse.ArgumentParser(description='Python script to serve as a base model for automated script generation, specifically for GET scripts using Redfish API')
parser.add_argument('-ip',help='iDRAC IP address', required=False)
parser.add_argument('-u', help='iDRAC username', required=False)
parser.add_argument('-p', help='iDRAC password. If you do not pass in argument -p, script will prompt to enter user password which will not be echoed to the screen.', required=False)
parser.add_argument('-x', help='Pass in X-Auth session token for executing Redfish calls. All Redfish calls will use X-Auth token instead of username/password', required=False)
parser.add_argument('--ssl', help='SSL cert verification for all Redfish calls, pass in value \"true\" or \"false\". By default, this argument is not required and script ignores validating SSL cert for all Redfish calls.', required=False)
parser.add_argument('--script-examples', help='Get executing script examples', action="store_true", dest="script_examples", required=False) 
# aditional parser arguments

args = vars(parser.parse_args())
logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.INFO)

def script_examples():
    # print statement with examples for running the 'remaining arguments'
    sys.exit(0)

# idrac version path
idrac_version_path = ''

# redfish api path
redfish_api_path = ''

def check_supported_idrac_version():
    if args["x"]:
        response = requests.get(f'{idrac_version_path}' % idrac_ip, verify=False, headers={'X-Auth-Token': args["x"]})
    else:
        response = requests.get(f'{idrac_version_path}' % idrac_ip, verify=False, auth=(idrac_username, idrac_password))
    data = response.json()
    if response.status_code == 401:
        logging.warning("\n- WARNING, status code %s returned. Incorrect iDRAC username/password or invalid privilege detected." % response.status_code)
        sys.exit(0)
    elif response.status_code != 200:
        logging.warning("\n- WARNING, iDRAC version installed does not support this feature using Redfish API")
        sys.exit(0)

# remaining functions