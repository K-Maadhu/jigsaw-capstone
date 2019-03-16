# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 12:54:37 2018

@author: anilnair
"""

import requests
import json,pandas as pd
import time,csv

_base_url = 'https://apis.mapmyindia.com/advancedmaps/v1/api_key/geo_code?addr='
_api_key = '---------paste your api key heare----------'

def call_mmi_api(addr):
    
    _url =_base_url.replace('api_key',_api_key)
    _url += addr
#    _url = _url.replace(' ','%20')
#    _url = _url.replace(',','%20')
    print(_url)
    session = requests.session()
    resp = session.get(_url)    
    return(resp)

_data = pd.read_csv('Attr_New_Geocoding.csv')
_adrs_out_list =[]
count = 0

for index,entry in _data.iterrows():
    time.sleep(0.5)
    count+=1
    response = call_mmi_api(str(entry['Attraction_name']) + ' ' + str(entry['Place']))
    if not response:
        print('Error in fetching url')
    else:    
        my_json = response.json()
        ad_dict = my_json.get('results')[0]
        ad_dict['attraction_id'] = entry['attraction_id']
        ad_dict['Attraction_name'] = entry['Attraction_name']
        ad_dict['Place'] = entry['Place']
        ad_dict['Description'] = entry['Description']
        ad_dict['Category'] = entry['Category']
        ad_dict['Website'] = entry['Website']
        ad_dict['User_rating'] = entry['User_rating']
        ad_dict['Review_keywords'] = entry['Review_keywords']
        ad_dict['Avg User Review Score'] = entry['Avg User Review Score']
        _adrs_out_list.append(ad_dict)
        if count % 50 == 0:
            with open('Attractions_combined_cleaned_new.csv', 'a') as f:
                pd.DataFrame(_adrs_out_list).to_csv(f,header=False,encoding= 'utf-8')                        
                print('Writing to CSV for Batch - ' + str(count/10))
                _adrs_out_list.clear()

if len(_adrs_out_list) > 0:
    with open('Attractions_combined_cleaned_new.csv', 'a') as f:
        pd.DataFrame(_adrs_out_list).to_csv(f,header=False,encoding= 'utf-8')                        