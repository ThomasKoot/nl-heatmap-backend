import requests
import json
import boto3
import handle_nc_data
import s3_handlers
import re
import os
import api_calls

# os.environ['API_KEY'] = 'eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjlmOTZmMTUzMDVhZTQ4NmI5NDIxOGZlY2NhYmE3NzkxIiwiaCI6Im11cm11cjEyOCJ9'
# os.environ['BUCKET'] = 'dieters-content-server'
# os.environ['BASE_PATH'] = 'nl_heat/data/'
# os.environ['KNMI_ENDPOINT'] = 'https://api.dataplatform.knmi.nl/open-data/v1/datasets/Actuele10mindataKNMIstations/versions/2/files'

def handler(event, context):

    current = s3_handlers.get_current()
    last_file = current.get('config').get('last_file') + '/url'
    filenames = api_calls.get_filenames(last_file)

    if len(filenames) == 0:
        print("no new files to fetch")
        return

    for filename in filenames:
        download_url = api_calls.get_download_url(filename)
        data = handle_nc_data.extract_data(filename, download_url)
        current['data'][re.search('\d{12}', filename).group()] = data

    current['config']['last_file'] = filenames[-1]

    s3_handlers.upload(current)

    print("succesfully uploaded " + str(len(filenames)) + " files")
    return
