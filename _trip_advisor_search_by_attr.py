# The BeautifulSoup module
from bs4 import BeautifulSoup
# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd

def slice_str(inp_str,beg,end,incl_ends):
    inp_str = str(inp_str)
    start = inp_str.find(beg)
    stop = inp_str.find(end) + len(end)
    if incl_ends==False:
        start += len(beg)
        stop -= len(end)
    return(inp_str[start:stop])

_home = 'www.tripadvisor.in'
inp_attr = ' hill stations in india'    
driver = webdriver.Chrome() # if you want to use chrome, replace Firefox() with Chrome()
print('Fetching page')
driver.get("https://www.tripadvisor.in/Home-g293860") # load the web page
driver.maximize_window()
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
driver.refresh()
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CLASS_NAME, 'brand-global-nav-action-search-Search__searchButton--2dmUT')))    
inputElementS = driver.find_element_by_class_name ('brand-global-nav-action-search-Search__searchButton--2dmUT')
inputElementS.click() 
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, "mainSearch")))    
inputElement = driver.find_element_by_id('mainSearch')
inputElement.send_keys(inp_attr)
inputElement.send_keys(Keys.ENTER)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-results-title")))  
inputElementB = driver.find_element_by_link_text("Things to do")  
inputElementB.click()

at_urls=[]
while True:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, "Next")))  
    inputElemNxt = driver.find_element_by_link_text('Next')
    soup = BeautifulSoup(driver.page_source,"lxml")
    attrs = soup.find_all('div',class_='location-meta-block')
    atr_list = list(attrs)    
    for stra in atr_list:
        atr_url = _home + slice_str(stra,'/Attraction_Review','.html',True)
        atr_name = slice_str(stra,'<span>','</span>',False)
        atr_dict = {'atrn_url':atr_url,'atr_name':atr_name}
        at_urls.append(atr_dict)    
    try:
        time.sleep(2.5)
        inputElemNxt.click()
    except:
        break
pd.DataFrame(at_urls).to_csv(inp_attr.replace(' ','_') + '_urls.csv')
