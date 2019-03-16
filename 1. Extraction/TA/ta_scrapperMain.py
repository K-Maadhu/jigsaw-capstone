# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 18:44:01 2018

@author: AnilNair
"""

import requests             
from bs4 import BeautifulSoup 
import csv                  
import webbrowser
import io
import pandas as pd
import re
import ta_reviewScrapper as rs
import argparse
import time,sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inp_file')
    parser.add_argument('inp_attr',default='2')
    parser.add_argument('inp_num_reviews',default='3')
    args = parser.parse_args()
    inp_file = args.inp_file
    inp_attr = args.inp_attr
    _num_reviews = int(args.inp_num_reviews)
    
    print('Fetching details for the input category ... ' + inp_attr)
    print('Fetching top ' + str(_num_reviews) + ' top reviews for attractions ...... ')
    _comp_url_list=[]
    
    _first = False
    _data = pd.read_csv(inp_file)
    try:
        _comp_url_list = pd.read_csv('parse_complete_urls.csv')['urls'].tolist()
    except:
        _comp_url_list.clear()
        _comp_url_list.append('urls')
        _first=True
         
    
    count=0
    _urls=[]
    for index,entry in _data.iterrows():        
        _t_url = entry['atrn_url']
        if _t_url.find('http://') < 0:
            _t_url = 'http://' + _t_url
        if _comp_url_list.__contains__(_t_url):
                continue
        count+=1   
        _urls.append(_t_url)
        if count % 10 == 0: 
#            print(_urls)
            start = time.clock()
            rs.get_reviews(_urls,_num_reviews,'a',inp_attr,'')
            print('[Batch complete] Parsing complete for ' + str(count) + ' urls. Took ' + str(time.clock() - start) + ' seconds for batch - ' + str(count/10))
            sys.stdout.flush()
            with open('parse_complete_urls.csv', 'a') as f:
                if _first:
                    pd.DataFrame(_urls).to_csv(f, header=['urls'],encoding='utf-8')
                    _first = False
                else:
                    pd.DataFrame(_urls).to_csv(f, header=False,encoding='utf-8')   
            _urls.clear()
            