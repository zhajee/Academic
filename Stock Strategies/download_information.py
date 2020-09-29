#download_information.py
'''The module that downloads the necessary information 
from the Alpha Vantage API and returns back the json dictionary.'''

import json
import urllib.parse
import urllib.request

BASE_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&'

def build_search_url(api_key: str, symbol: str) -> str:
	'''Takes in an API key and stock symbol and uses this to build a URL that can
	ask the alphavantage data API for information about stocks matching this request.'''

	query_parameters = [
        ('symbol', symbol), ('apikey', api_key), ('outputsize', 'full')
    ]

	return BASE_URL + urllib.parse.urlencode(query_parameters)

def convert_to_python_obj(url: str)-> dict:
	'''Takes a URL and returns a Python dictionary representing the
    parsed JSON response.'''
    
	response = None

	try:
	    response = urllib.request.urlopen(url)
	    json_text = response.read().decode(encoding = 'utf-8')

	    return json.loads(json_text)

	finally:
	    if response != None:
	        response.close()
