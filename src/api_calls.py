import json
import requests
import os

def get_filenames(latest_file):
    
    headers_dict = { 'Authorization' : os.environ['API_KEY'] }
    params = {
        "startAfterFilename" : latest_file,
        "maxKeys" : "10"
    }
    
    try:
        response = requests.get(os.environ['KNMI_ENDPOINT'], headers=headers_dict, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise Exception("unable to fetch filenames " + json.dumps(response.json(), indent=4))
             
    to_parse = response.json().get('files', [])
    return [entry['filename'] for entry in to_parse]

def get_download_url(filename):

    url = os.environ['KNMI_ENDPOINT'] + "/" + filename + "/url"
    headers_dict = { 'Authorization' : os.environ['API_KEY'] }

    try:
        response = requests.get(url, headers=headers_dict)
        response.raise_for_status()
        download_url = response.json().get('temporaryDownloadUrl')
    except requests.exceptions.HTTPError:
        raise Exception(("unable to fetch download_url", json.dumps(response.json(), indent=4)))
    return download_url
