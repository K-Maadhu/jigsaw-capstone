# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 12:54:37 2018

@author: anilnair
"""

import requests
import json,pandas as pd
import time

_base_url = 'https://apis.mapmyindia.com/advancedmaps/v1/api_key/geo_code?addr='
_api_key = 'pdplzplm6ecuannnjztcuvoelm21xgoy'

def call_mmi_api(addr):
    
    _url =_base_url.replace('api_key',_api_key)
    _url += addr
#    _url = _url.replace(' ','%20')
#    _url = _url.replace(',','%20')
    print(_url)
    session = requests.session()
    resp = session.get(_url)    
    return(resp)

_data = pd.read_csv('geocode_addresses.csv')
_adrs_out_list =[]

for index,entry in _data.iterrows():
    time.sleep(0.5)
    response = call_mmi_api(entry['address'])
    if not response:
        print('Error in fetching url')
    else:    
        my_json = response.json()
        ad_dict = my_json.get('results')[0]
        ad_dict['ad_seq'] = entry['seq']
        ad_dict['ad_inp'] = entry['address']
        _adrs_out_list.append(ad_dict)

pd.DataFrame(_adrs_out_list).to_csv('geocode_address_output.csv')