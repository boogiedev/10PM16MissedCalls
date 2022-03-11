import json
import requests
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode


# API constants
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

# Get API Credentials
CLIENT_ID, KEY, GEO_KEY = "", "", ""
with open("credentials.json", "r") as file_to_read:
    json_data = json.load(file_to_read)
    CLIENT_ID = json_data["CLIENT_ID"]
    KEY = json_data["API_KEY"]
    GEO_KEY = json_data["GEO_KEY"]

# Create auth header
HEADER = {"Authorization": f"bearer {KEY}"}

def yelp_request(host:str=API_HOST, path:str=SEARCH_PATH, api_key:str=KEY, url_params:dict=None):
    """Given an API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

# Param Example
# params = {'term': 'coffee',
#           'location': 'Toronto, Ontario',
#           'limit': 10}
