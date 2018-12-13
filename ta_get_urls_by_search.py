
# coding: utf-8

# The script will provide two csv files namely
# 
# - attractions_<city_name>.csv
# - hotels_nearby_<city_name>.csv
# 
# Accepts 3 parameters
# - city_name (e.g. Mysuru)
# - num_attractions (Number of attractions to fetch the data e.g. 20 means top 20 attractions for the city Mysuru)
# - num_nearby_hotels (Number of nearby hotel urls to fetch for each attraction)
# 
# How to run?
# 
# - Place the file Trip_advisor_parse_urls.py  in any folder. Note that output csv's will be created in the same folder
# - Open Anaconda prompt and navigate to the folder where the script is placed
# - Execute the command python Trip_advisor_parse_urls.py Hyderabad 2 3


import pandas as pd
import numpy as np
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import time
import os.path
import argparse
#import reviewScrapper as rs



home = 'http://www.tripadvisor.in'
_num_attractions = 2
_num_hotels = 3
_num_reviews = 5



def get_json(url):
    
    time.sleep(3.5)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    
    print('Fetching url....' + url)
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    print('Fetch complete....')
    json = response.read() # The data u need
    
    return(json)



# Function to fetch the HTML content from an input url.

def get_html_to_soup(url):
    
    time.sleep(3.5)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    
    print('Fetching url....' + url)
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    print('Fetch complete....')
    html = response.read() # The data u need
    
    # Convert html in to a soup
    soup = BeautifulSoup(html,'lxml')
    return(soup)




def get_attractions_hotels(loc_home_page):

    # Fetch the home page for the city.
    loc_home_soup = get_html_to_soup(loc_home_page)

    #Find all the key links from the city home page.
    win_div = loc_home_soup.find_all('a', class_ = 'brand-quick-links-QuickLinkTileItem__link--2V0Pn')
    
    # Form the link dictionary for all key links
    link_dict={}
    hotel_links=[]
    attraction_links=[]
    for div in win_div:
        link_dict[div.text] = div.attrs['href']

    # Form the url for the things to do home page for the input city   
    attr_home_page = home + link_dict.get('Things to do')

    #Soup the attraction page
    attr_home_soup =  get_html_to_soup(attr_home_page)

    page_type2 = False
    
    #Find  top n attractions
    att_div = attr_home_soup.find_all('div', class_ = 'attraction_element')
    
    #Some pages have different structure for attractions.
    if len(att_div)==0:
        att_div = attr_home_soup.find_all('a', class_ = 'attractions-attraction-overview-main-TopPOIs__name--3eQ8p')
        page_type2 = True
                
    attrs_list=[]
    hotels_list=[]
    atr_count=1
    for div in att_div:
        if atr_count > _num_attractions:
                break
        else:
                atr_count+=1

        #Form the attraction dictionary based on page type
        attr_dict={}
        if not page_type2:            
            attr_dict['attraction_name'] = div.find('a').text
            attr_dict['attraction_url'] = home + div.find('a').attrs['href']                     
        else:
            attr_dict['attraction_name'] = div.text
            attr_dict['attraction_url'] = home + div.attrs['href']            
        attr_dict['city'] = inp_city      
        attrs_list.append(attr_dict)
        attraction_links.append(attr_dict['attraction_url'])
        rs.get_reviews(attraction_links,_num_reviews,'a',inp_city,attr_dict['attraction_name'])
        attraction_links.clear()
        
        #For every attraction, form the hotels nearby url
        hotels_nearby_url = attr_dict['attraction_url'].replace('Attraction_Review','HotelsNear')
        hotels_nearby_url = hotels_nearby_url.replace('Reviews-','')

        #Soup the hotels nearby url
        htl_nby_soup =  get_html_to_soup(hotels_nearby_url)

        #Fetch first n hotels for the destination
        div_htls = htl_nby_soup.find_all('div', class_ = 'listing_title')    
        htl_count=1    
        for div in div_htls:
            if htl_count > _num_hotels:
                break
            else:
                htl_count+=1        

            #Form the hotels dictionary
            hotel_dict={}
            hotel_dict['name'] = div.find('a').text
            hotel_dict['link'] = home + div.find('a').attrs['href']
            hotel_dict['nrby_attraction_name'] = attr_dict['attraction_name']

            #Append to hotels list
            hotels_list.append(hotel_dict)
            hotel_links.append(hotel_dict['link'])
            print('Calling Review Scrapper.....')
            
        rs.get_reviews(hotel_links,_num_reviews,'h',inp_city,attr_dict['attraction_name'])
        hotel_links.clear()


#    print(attraction_links)

    #Build the attractions and hotels dataframe                
    attrs_df = pd.DataFrame(attrs_list)
    hotels_df = pd.DataFrame(hotels_list)

    #Write the attractions.csv and hotels.csv
    print('Writing output csvs......')
    attrs_df.to_csv('attractions_' + inp_city+ '.csv')
    hotels_df.to_csv('hotels_nearby_' + inp_city + '.csv')
    print('Finished Writing output csv files for.... ' + inp_city + '........')




def fetch_city_data(inp_city):
    
    #Form the query url
    s_url = 'https://www.tripadvisor.in/TypeAheadJson?action=API&query=' + inp_city + '&types=geo&name_depth=1&details=true&legacy_format=true&'    +'max=8&searchSessionId=87E9B3EDF454783AA20B028A65A7540E1543388831289ssid&startTime=1543388839021'

    #Fetch the json by accessing the url
    loc_json = get_json(s_url)
    import json
    inp_json=json.loads(loc_json)
    resp_df = pd.DataFrame(inp_json)

    #By default, the first result is assumed to be the most accurate one
    loc_home_page = home + resp_df['url'].iloc[0]

    #Fetch the attractions and hotels url
    get_attractions_hotels(loc_home_page)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('inp_city')
    parser.add_argument('inp_num_attr',default='2')
    parser.add_argument('inp_num_hotels',default='3')
    parser.add_argument('inp_num_reviews',default='3')
    args = parser.parse_args()
    inp_city = args.inp_city
    _num_attractions = int(args.inp_num_attr)
    _num_hotels = int(args.inp_num_hotels)
    _num_reviews = int(args.inp_num_reviews)
    
    print('Fetching details for the input city ... ' + inp_city)
    print('Fetching top ' + str(_num_attractions) + ' attractions data...... ')
    print('Fetching top ' + str(_num_hotels) + ' hotels data...... ')
    print('Fetching top ' + str(_num_reviews) + ' top reviews for hotels and attractions ...... ')

    fetch_city_data(inp_city)
