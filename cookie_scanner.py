import datetime
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import requests
import uuid

API_COOKIE_DOCTOR='https://api.cookie.doctor/api/v1/process_host/'

def read_hostnames(input_arg):
    """
    Read hostnames from a single hostname, list of hostnames, or a .txt file.
    """
    if isinstance(input_arg, list):
        return input_arg
    elif input_arg.endswith('.txt'):
        with open(input_arg, 'r') as f:
            return [line.strip() for line in f.readlines()]
    else:
        return [input_arg]

def write_output(response: str, hostname: str, date_time:str ):
    """
    Write the response to a output/hostname/json file.
    """
    file_ext = 'json'
    date_time = date_time.replace(" ", "_")
    hostname = hostname.replace("/", "_")
    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        file_ext = 'txt'
    
    if isinstance(response, str):
        file_ext = 'txt'
    
    filename = f"output/{hostname}/{hostname}_{date_time}.{file_ext}"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    if file_ext == 'json':
        with open(filename, 'w') as f:
            json.dump(response, f, indent=4)
    else:
        with open(filename, 'w') as f:
            f.write(response)
    print("[ OK ] Response saved to", filename)

def send_request(hostname):
    """
    Send a request to api.cookie.doctor with the hostname.
    """
    try:
        date_time = str(datetime.datetime.now())
        hostname = f'https://{hostname}' if not hostname.startswith('http') else hostname
        print(f"Scanning {hostname} at {date_time}")
        response = requests.post(API_COOKIE_DOCTOR, json={
            'url': hostname,
            'is_public': True,
            'start_at': date_time,
            'channel_name': '4fa1ed3d-0b0e-4be3-b3a9-9402bb6a8a4e',
        })
        if (response.status_code == 200) or (response.status_code == 201):
            write_output(response.text, hostname, date_time)
        else:
            print(f"Response for {hostname}, Status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[x] Error: {hostname}, Message: {str(e)}")
    except Exception as e:
        print(f"[x] Error: {hostname}, Message: {str(e)}")

def process_hostnames(hostnames):
    """
    Process a list of hostnames using 4 workers with ThreadPoolExecutor.
    """
    with ThreadPoolExecutor(max_workers=5, thread_name_prefix=f"process_host_workers", ) as executor:
        executor.map(send_request, hostnames)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: script.py <hostname|hostnames.txt|['hostname1', 'hostname2', ...]>")
    else:
        input_arg = sys.argv[1]
        if input_arg.startswith("[") and input_arg.endswith("]"):
            # Convert string list argument to actual list
            hostnames = eval(input_arg)
        else:
            hostnames = read_hostnames(input_arg)
        process_hostnames(hostnames)
