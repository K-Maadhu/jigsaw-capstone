
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import time
import os.path


# In[2]:


# Function to fetch the HTML content from an input url.

def get_html_to_soup(url):
    
    time.sleep(3.5)
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,} 
    
    request=urllib.request.Request(url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)
    html = response.read() # The data u need
    
    # Convert html in to a soup
    soup = BeautifulSoup(html,'lxml')
    return(soup)


# In[3]:


# Function to return the first element in a list that contains JSON data.
def find_jelem(l_locs):
    idx = 0
    for elem in l_locs:
        if str(elem).__contains__('script type="application/ld+json"'):
            return l_locs[idx].string
        else: 
            idx = idx + 1 
    print(l_locs[idx].string)
    return l_locs[idx].string


# In[4]:


# Function to return the first element in a list that contains JSON data.
def find_json_places(l_locs):
    idx = 0
    for elem in l_locs:
        if str(elem).__contains__('script type="application/ld+json"') &            str(elem).__contains__('sightseeing-and-things-to-do.html') :
            return l_locs[idx].string
        else: 
            idx = idx + 1 
    print(l_locs[idx].string)
    return l_locs[idx].string


# In[5]:


# Get reviews for a given place and write the output to place_reviews.csv

def get_place_reviews(inp_place_url):
    
    # Form the url for all reviews page 
    url_revw = inp_place_url + 'tips-and-reviews.html'
    
    # Soup the url
    soup_p = get_html_to_soup(url_revw)
    
    # Find all div tags with review content.
    revws = soup_p.findAll('div',class_ = "col-md-12 col-xs-12 allReviewCard visibleReview")
    
    # Parse through reviews result set to form a dictionary with following columns
        # place
        # state
        # review
        
    revw_list = []
    for rv in revws:
        revw_dict = {}
        revw_dict['place'] = place
        revw_dict['state'] = state
        revw_dict['review'] = rv.text.strip()
        revw_list.append(revw_dict)
   
    # Convert list of dict reviews to a dataframe
    revws_df = pd.DataFrame(revw_list)
    
    #Append the reviews to place_reviews.csv
    if(os.path.isfile('holidify/place_reviews.csv')):
        revws_df.to_csv('holidify/place_reviews.csv',mode = 'a',header=False)
    else:
        revws_df.to_csv('holidify/place_reviews.csv',mode = 'a',header=True)


# In[19]:


# Get html output for the Himachal pradesh tourist destinations
# soup=get_html_to_soup("http://www.holidify.com/state/himachal-pradesh/top-destinations-places-to-visit.html")
soup=get_html_to_soup("https://www.holidify.com/state/kerala/top-destinations-places-to-visit.html")

# Find JSON like data using the script tag
l_locs= list(soup.find_all('script'))


# In[20]:


# Parse the JSON data in to a dictionary using the JSON library
comm  = find_jelem(l_locs)
import json
comment=json.loads(comm)
locs_df = pd.DataFrame(comment.get('itemListElement'))
locs_df=locs_df.drop(['@type','position'],axis=1)
locs_df.to_csv('test.csv',mode = 'a',header = True)


# In[22]:


# =============================================================================
# #Fetch the pages for places.
# for index,locn in locs_df.iterrows():
#     soup_p = get_html_to_soup(locn['url'])
#     # Extracting the description for the place out of the div
#     win_div = soup_p.find('div', class_ = 'col-md-12 sectionBorderMidSection nopaddingLeft nopaddingRight col-xs-12')
#     place,state = locn['name'].split(",",1)
#     plc_desc = win_div.text
#     place_dict = [{'place':place,'state':state,'place_desc':plc_desc}]
#     pd.DataFrame(place_dict).to_csv('holidify/place_details.csv',mode = 'a', header=False)
#     # Get Reviews for the current place
#     #get_place_reviews(locn['url'])
#     
#     #Get attractions for the place.
#     soup_a = get_html_to_soup(locn['url'] + 'sightseeing-and-things-to-do.html')
#     # Find JSON like data using the script tag
#     l_attrs= list(soup_a.find_all('script'))
#     at_json  = find_json_places(l_attrs)
#     import json
#     at_json=json.loads(at_json)
#     attrs_df = pd.DataFrame(at_json.get('itemListElement'))
#     attrs_df=attrs_df.drop(['@type','position'],axis=1)
#     
#     # Get reviews and description for each attraction.
#     for index,at in attrs_df.iterrows():
#         if not (at['url'].__contains__('holidify.com')):
#             at['url'] = 'https://www.holidify.com' + at['url']
# =============================================================================
            #print(at['url'])
#         soup_t = get_html_to_soup(at['url'])
#         attr_name = at['name']
#         attr_tag_rset = soup_t.find_all('div', class_ = 'col-md-12 col-xs-12 middleSection')
#         attr_desc=''
#         attr_reviews=[]
#         for attrs in attr_tag_rset:
#             if not (attrs.get('id') == "reviews"):
#                  attr_desc +=  attrs.text
#             else:
#                 attr_tvw_rset = soup_t.find_all('div', class_ = 'col-md-12 col-xs-12 allReviewCard visibleReview')
#                 for attr_rvs in attr_tvw_rset:
#                     at_revw_dict = {}
#                     at_revw_dict['place'] = place
#                     at_revw_dict['state'] = state
#                     at_revw_dict['attr_name'] = attr_name
#                     at_revw_dict['review'] = attr_rvs.text.strip()
#                     attr_reviews.append(at_revw_dict)                
#         attr_dict = [{'place':place,'state':state,'attr_name':attr_name,'attr_desc':attr_desc}]

# =============================================================================
#         attr_dict = [{'place':place,'state':state,'attr_name':at['name']}]
#         if(os.path.isfile('holidify/attr_details.csv')):
#             pd.DataFrame(attr_dict).to_csv('holidify/attr_details.csv',mode = 'a',header = False)
#         else:
#             pd.DataFrame(attr_dict).to_csv('holidify/attr_details.csv',mode = 'a',header = True)
# =============================================================================

#         if(os.path.isfile('holidify/attr_reviews.csv')):
#             pd.DataFrame(attr_reviews).to_csv('holidify/attr_reviews.csv',mode = 'a', header = False)
#         else:
#             pd.DataFrame(attr_reviews).to_csv('holidify/attr_reviews.csv',mode = 'a', header = True)


