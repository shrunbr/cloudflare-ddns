import yaml
import requests
import json
import sys
import time
import logging

# Load Config File
config = yaml.safe_load(open('config/config.yml'))

# Global Variables
cf_api_key = config['token']
cf_api_email = config['email']
domain = config['domains'][0]
record_name = config['records'][0]['name']
timer = config['timer']
log_level = config['logging_level']

# Logging Variables
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
if log_level == "DEBUG":
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

# To get current IP Address

def get_ip_address():
    # IP Source Variables (uncomment to change source)
    url = 'https://icanhazip.com'
    ### WARNING! THE IP CHECKERS BELOW DO NOT SUPPORT IPV6 ###
    #url = 'https://api.ipify.org/'
    #url = 'https://myexternalip.com/raw'
    global ip_address
    global record_type
    ip_address = requests.get(url).text

    # Check config if we're using IPv6
    if config['use_ipv6'] == True:
        record_type = 'AAAA'
    if config['use_ipv6'] == False:
        record_type = 'A'

    try:
        return ip_address, record_type
    except:
        print("Am I even connected to the internet? I can't get your IP...")
        exit()

def get_zone_id():
    # Variables
    url = (f"https://api.cloudflare.com/client/v4/zones?name={domain}")
    # API Auth Headers
    headers = {
        'X-Auth-Key': (f"{cf_api_key}"),
        'X-Auth-Email': (f"{cf_api_email}"),
        'Content-Type': 'application/json'
    }
    # API Response Variables
    response = requests.request("GET", url, headers=headers)
    # Fetch Zone ID
    try:
        if response.status_code == 200:
            response_json = response.json()
            global zone_id
            zone_id = response_json['result'][0]['id'] 
        else:
            print("Failed to fetch zone ID. Please check your config file and try again. Exiting...")
            exit()
    except:
        print("Failed to fetch zone ID. Please check your config file and try again. Exiting...")
        exit()

def get_record_id():
    # Variables
    url = "https://api.cloudflare.com/client/v4/zones/%s/dns_records?name=%s.%s" % (zone_id, record_name, domain)
    # API Auth Headers
    headers = {
        'X-Auth-Key': (f"{cf_api_key}"),
        'X-Auth-Email': (f"{cf_api_email}"),
        'Content-Type': 'application/json'
    }
    # API Response Variables
    response = requests.request("GET", url, headers=headers)
    # Fetch Record ID
    try:
        if response.status_code == 200:
            response_json = response.json()
            global record_id
            record_id = response_json['result'][0]['id']
        else:
            print("Failed to fetch record ID. Please check your config file and try again. Exiting...")
            exit()
    except:
        print("Failed to fetch record ID. Please check your config file and try again. Exiting...")
        exit()

def update_dns_record():
    # Varibles
    url = "https://api.cloudflare.com/client/v4/zones/%s/dns_records/%s" % (zone_id, record_id)
    update_name = record_name + "." + domain
    if config['use_cf_proxy'] == True:
        proxied = True
    if config['use_cf_proxy'] == False:
        proxied = False
    # API Auth Headers
    headers = {
        'X-Auth-Key': (f"{cf_api_key}"),
        'X-Auth-Email': (f"{cf_api_email}"),
        'Content-Type': 'application/json'
    }
    # API Payload
    data = {'type': (f"{record_type}"),"name": (f"{update_name}"),"content": (f"{ip_address}"),"proxied": proxied}
    payload = json.dumps(data)
    # API Response Variables
    response = requests.request("PUT", url, headers=headers, data=payload)
    if response.status_code == 200:
        logging.info(f"Successfully updated {update_name} to {ip_address}")
    else:
        logging.info(f"Failed to update {update_name} to {ip_address}. Please check config and try again.")

while(True):
    get_ip_address()
    get_zone_id()
    get_record_id()
    update_dns_record()
    time.sleep(timer)