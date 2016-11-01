import requests
import json
import pprint
import os

def request_Airbnb():
    """sending request to QPX and return the results as python dictionary"""

    #The url to send request
    api_key = os.environ['Airbnb_KEY']
    url = "https://api.airbnb.com/v2/search_results?client_id=%s" %(api_key)
    
    #The search parameters to pass into request body
    search_param = { 'locale' : 'en-US', 
        'currency' : 'USD',
        # '_format': 'for_search_results_with_minimal_pricing',
        '_limit':  '1',
        #'_offset': '0',
        'guests':  '1',
        'ib':  'false',
        'sort':  '1',
        'min_beds' :  '1',
        'location':  "Seattle/Tacoma",
        'price_min' : '40',
        # 'price_max': '210',
        # 'fetch_facets':'true',
        # 'ib_add_photo_flow':'true',
        # 'min_num_pic_urls':'10',
        'checkin': '2016-12-26',
        'checkout': '2016-12-31'}


    #Send json request and return json response
    response_json = requests.get(url, params=search_param)

    #Turn json response into python dictionary
    lodging_response_dict = response_json.json()


    pprint.pprint(lodging_response_dict)

    print "URL IS HERE!!!!!!!!*************** ", (response_json.url)

    return lodging_response_dict


def parse_Airbnb(lodging_response_dict):
    """Takes input python dictionary and parse out desire fields into new dictionary"""

    #Set key-value pair for new flight dictionary
    lodging_info_dict = {"lodging_id" : lodging_response_dict["search_results"][0]["listing"]["id"],
    "address" : lodging_response_dict["search_results"][0]["listing"]["public_address"],
    "picture" : lodging_response_dict["search_results"][0]["listing"]["picture_url"],
    "lodging_price" : lodging_response_dict["search_results"][0]["pricing_quote"]["localized_total_price"]}

    return lodging_response_dict
