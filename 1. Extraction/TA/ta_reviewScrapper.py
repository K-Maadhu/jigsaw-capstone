import requests             
from bs4 import BeautifulSoup 
import csv                  
import webbrowser
import io
import pandas as pd
import re
import time


en_type = ''
hotel_name = ''
hotel_details_list = []
atr_details_list = []
num_reviews_max = 0
overall_rating_g = ''
hotel_features_g =''
lang = 'en'
#print('test invoked')
reviews =[]
city = ''
nearby_attr=''
num_reviews=0
next_url=''
    

def display(content, filename='output.html'):
    with open(filename, 'wb') as f:
        f.write(content)
        webbrowser.open(filename)

def get_soup(session, url, show=False):
    
    time.sleep(2.5)
    r = session.get(url)
    if show:
        display(r.content, 'temp.html')

    if r.status_code != 200: # not OK
        print('[get_soup] status code:', r.status_code)
    else:
        return BeautifulSoup(r.text, 'html.parser')
    
def post_soup(session, url, params, show=False):
    '''Read HTML from server and convert to Soup'''
    time.sleep(2.5)

    r = session.post(url, data=params)
    
    if show:
        display(r.content, 'temp.html')

    if r.status_code != 200: # not OK
        print('[post_soup] status code:', r.status_code)
    else:
        return BeautifulSoup(r.text, 'html.parser')
    
def scrape(url, lang='ALL'):

    # create session to keep all cookies (etc.) between requests
    session = requests.Session()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0',
    })


    items = parse(session, url + '?filterLang=' + lang)

    return items

def parse(session, url):
    '''Get number of reviews and start getting subpages with reviews'''
    global overall_rating_g
    global num_reviews
    global next_url
    
    print('[parse] url:', url)

    soup = get_soup(session, url)

    if not soup:
#        print('[parse] no soup:', url)
        return
    
    hotel_name = soup.find('h1', id='HEADING').text
    
    try:
        overall_rating_g = soup.find('span',class_= re.compile('overallRating')).text
        overall_rating_g= int(re.findall("\d+", overall_rating_g)[0])
    except:
        overall_rating_g = 0    
        
    if en_type == 'h':
        get_hotel_features (soup,hotel_name)
    else:
        get_attr_features (soup,hotel_name)            
    
    try:
        revs_cnt = soup.find('span', class_='reviews_header_count')
        if not revs_cnt:
            revs_cnt = soup.find('span', class_='reviewCount') # get text   
            
        num_reviews = revs_cnt.text.replace(',','') # get text    
        num_reviews = num_reviews[1:-1] 
    #    num_reviews = num_reviews.replace(',', '')
        num_reviews = int(re.findall("\d+", num_reviews)[0])    
    except:
         num_reviews = 0
#    print('num_reviews :', num_reviews)

#    url_template = url.replace('.html', '-or{}.html')
#    print('[parse] url_template:', url_template)

    items = []

    next_url = url

    while(True):
        
        next_sub_page_url = next_url        
#        print('Fetching sub-page review url - ' + next_sub_page_url)
        
        if len(next_sub_page_url) <= 0:
#            print('Breaking as no next url')
            break
        
        subpage_items = parse_reviews(session, next_sub_page_url)
        if not subpage_items:
#            print('Breaking as no data returned')
            break

        items += subpage_items
        if len(subpage_items) < 5 or len(items) >= num_reviews_max or len(items) >= num_reviews:
#            print('Breaking from loop - num_reviews_max = ' + str(num_reviews_max) + 'Num_reviews - ' + str(num_reviews))
            break
#        else:
#            print('Extracted ' + str(len(items)) + ' Total reviews - ' + str(num_reviews))
        
    print('Extracted latest  ' + str(len(items)) + ' of ' + str(num_reviews) + ' reviews for ' + url)
    return items

def get_hotel_features(soup,hotel_name):
    
    global hotel_features_g

    divs_hotel_features = soup.find_all('div', class_= re.compile('HighlightedAmenities__amenityItem'))
    
    if len(divs_hotel_features) == 0:
        divs_hotel_features = soup.find_all('span', class_= re.compile('Amenity__name'))
        
    hotel_features=''
    
    for divs in divs_hotel_features:
        hotel_features += divs.text + ','
            
#    print('setting rating ....')
    hotel_features_g = hotel_features
    hotel_details = {'hotel_name':hotel_name,
                     'hotel_rating':overall_rating_g,
                     'hotel_features':hotel_features_g,
                     'nearby_attraction':nearby_attr}   

    hotel_details_list.append(hotel_details)   

def get_attr_features(soup,hotel_name):
    
    try:
        strt_address = soup.find('span', class_='street-address').text
    except:
        strt_address = ''
    try:
        ext_address = soup.find('span', class_='extended-address').text
    except:
        ext_address = ''
    try:
        locality = soup.find('span', class_='locality').text
    except:
        locality=''
    try:
        atr_details = soup.find('div',class_= re.compile('attractions-attraction-detail-about-card')).text
    except:
        atr_details=''
    try:        
        revw_items = soup.find_all('a')
        revw_kwrds=''
        for revw in revw_items:
            if (revw.attrs.get('href') == '#REVIEWS') and (revw.text.upper().find('REVIEWS') == -1):
                revw_kwrds += revw.text + ' ' 
    except:
        revw_kwrds=''
    atr_details = {'Attraction_Name':hotel_name,
                   'Address':strt_address + ',' + ext_address + ',' + locality,
                   'about_atrcn':atr_details,
                   'review_keywords':revw_kwrds,
                   'rating':overall_rating_g,
                   'num_reviews':num_reviews}
    atr_details_list.append(atr_details)


def get_reviews_ids(soup):

    items = soup.find_all('div', attrs={'data-reviewid': True})

    if items:
        reviews_ids = [x.attrs['data-reviewid'] for x in items][::2]
#        print('[get_reviews_ids] data-reviewid:', reviews_ids)
        return reviews_ids
    
def get_more(session, reviews_ids):

    url = 'https://www.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_HOTEL_REVIEWS_RESP&metaReferer=Hotel_Review'

    payload = {
        'reviews': ','.join(reviews_ids), # ie. "577882734,577547902,577300887",
        #'contextChoice': 'DETAIL_HR', # ???
        'widgetChoice': 'EXPANDED_HOTEL_REVIEW_HSX', # ???
        'haveJses': 'earlyRequireDefine,amdearly,global_error,long_lived_global,apg-Hotel_Review,apg-Hotel_Review-in,bootstrap,desktop-rooms-guests-dust-en_US,responsive-calendar-templates-dust-en_US,taevents',
        'haveCsses': 'apg-Hotel_Review-in',
        'Action': 'install',
    }

    soup = post_soup(session, url, payload)

    return soup

def parse_reviews(session, url):
    '''Get all reviews from one page'''
    global next_url

#    print('[parse_reviews] url:', url)
    soup =  get_soup(session, url)

    if not soup:
#        print('[parse_reviews] no soup:', url)
        return
    
    try:
         next_url = soup.find('a', class_='nav next taLnk ui_button primary').attrs['href']
         if len(next_url) > 1:
             next_url = 'http://www.tripadvisor.in' + next_url
         else:
             next_url=''
#        print('Next-page is - ' + next_url)
    except:
        next_url=''
   
    hotel_name = soup.find('h1', id='HEADING').text

    reviews_ids = get_reviews_ids(soup)
    if not reviews_ids:
        return

    soup = get_more(session, reviews_ids)

    if not soup:
#        print('[parse_reviews] no soup:', url)
        return

    items = []
    
    for idx, review in enumerate(soup.find_all('div', class_='reviewSelector')):
        
        if len(review.attrs['class']) > 1:
            continue        
              
        badgets = review.find_all('span', class_='badgetext')
        if len(badgets) > 0:
            contributions = badgets[0].text
        else:
            contributions = '0'

        if len(badgets) > 1:
            helpful_vote = badgets[1].text
        else:
            helpful_vote = '0'
        user_loc = review.select_one('div.userLoc strong')
        if user_loc:
            user_loc = user_loc.text
        else:
            user_loc = ''
            
        bubble_rating = review.select_one('span.ui_bubble_rating')['class']
        bubble_rating = bubble_rating[1].split('_')[-1]
        try:
            bubble_rating = int(bubble_rating)/10
        except:
            bubble_rating = 0
        
        
        if en_type == 'h':
            item = {
                'city_name'  : city,
                'hotel_name' : hotel_name,   
                'review_body': review.find('p', class_='partial_entry').text,
                'nearby_attraction':nearby_attr,
                'review_date': review.find('span', class_='ratingDate')['title'], # 'ratingDate' instead of 'relativeDate'
                'review_rating':bubble_rating
            }
        else :
            item = {
                'city_name'  : city,
                'review_body': review.find('p', class_='partial_entry').text,
                'nearby_attraction':hotel_name,
                'review_date': review.find('span', class_='ratingDate')['title'], # 'ratingDate' instead of 'relativeDate'
                'review_rating':bubble_rating
                
            }
        

        items.append(item)
#        print('\n--- review ---\n')
#        for key,val in item.items():
#            print(' ', key, ':', val)

#    print()

    return items

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def get_reviews(start_urls,in_num_reviews_max,in_en_type,inp_city,nrby_attraction):
    
    global num_reviews_max
    global en_type
    global reviews
    global city
    global nearby_attr
    
    lang = 'en'       
    city = inp_city
    num_reviews_max = int(in_num_reviews_max)
    en_type = in_en_type
    nearby_attr = nrby_attraction
    reviews.clear()
    hotel_details_list.clear()
    atr_details_list.clear()

#    print('scrapper called for -  ' + in_en_type + "-" + nrby_attraction)
#    print(start_urls)

    for url in start_urls:
        # get all reviews for 'url' and 'lang'
        reviews += scrape(url, lang)
        write_data(reviews,url)
        reviews.clear()
        hotel_details_list.clear()
        atr_details_list.clear()

def write_data(reviews,url):    
    #Strip non-ascii characters from the string
    for rev in reviews:
        rev['review_body'] = strip_non_ascii(rev['review_body'])
        
    for atrs in atr_details_list:
        atrs['Attraction_Name'] = strip_non_ascii(atrs['Attraction_Name'])
        atrs['Address'] = strip_non_ascii(atrs['Address'])
        atrs['about_atrcn'] = strip_non_ascii(atrs['about_atrcn'])
        atrs['review_keywords'] = strip_non_ascii(atrs['review_keywords'])
    
    if not reviews:
        print('No reviews')
    else:
    # write in CSV
        if en_type == 'h':
            filename_rvw = 'Hotel_Reviews_' + inp_city + '.csv'
            filename_dtl = 'Hotel_Details_' + inp_city + '.csv'
            
            with open(filename_rvw, 'a') as f:
                pd.DataFrame(reviews).to_csv(f, header=False,encoding='utf-8')
                
            with open(filename_dtl, 'a') as f:
                pd.DataFrame(hotel_details_list).to_csv(f, header=False,encoding='utf-8')
                
        else:
            filename_rvw = 'Attraction_Reviews_' + city + '.csv'    
            filename_dtl = 'Attraction_details_' + city + '.csv'
            with open(filename_rvw, 'a') as f:
                pd.DataFrame(reviews).to_csv(f, header=False,encoding='utf-8')
            with open(filename_dtl, 'a') as f:
                pd.DataFrame(atr_details_list).to_csv(f, header=False,encoding='utf-8')
#        print('Writing reviews to filename:', filename)

