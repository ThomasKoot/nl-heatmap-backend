import netCDF4 as nc
import requests

def parse_nc_data(filename):

    ds = nc.Dataset(filename)
    temp = ds['ta'][:]
    st = ds['station'][:]

    data = {}

    for i in range(len(temp)):
        data[st[i]] = temp[i].data[0]

    return data

def extract_data(filename, download_url):
    response = requests.get(download_url)
    filepath = '/tmp/' + filename

    with open(filepath, 'wb') as filehandle:
        filehandle.write(response.content)
    
    data = parse_nc_data(filepath)
    return data