
**********************************************************Important Note******************************************************************

This program was executed based on the structure of the HolidayIQ website as of December 2018. Please make necessary changes as required
to make this code working if the underlying strucutre of the website has been changed.

******************************************************************************************************************************************

*********************Step 1 - Extraction of attraction urls for the 3 categories(Beach, Heritage & Hill Station)**************************

Web scraping of HolidayIQ is done using Scrapy.Scrapy is an open source web crawling framework written in Python. It uses XPath to extract
data from web pages. It is possible to scrap any website though that website does not have API for raw data access. scrapy.Spider class is used to
scrap the HolidayIQ website

1. Prerequisites
	1.1 Set up the Development environment for Windows users.
	    Used Visual Source Code Editor.
 	 
	1.2 Source Code
		holidayIQ.py
	
	1.2 Python packages
		Python 3.x
		Scrapy
		
	1.3 How to Run?
	
		- The program uses the landing page url hardcoded in the program and then extracts the location of each attractions.
		- The XPath secletor of Location, Type, url and No. of Sight seeing is provided as input. 
		- Note: The XPath selectors are subject to change when the website undergoes modification. Use the 'correct' XPath selector. 
		- Scrapy code execution systax is : scrapy crawl <name as specified in the identity section in the program> -o <filename>.csv
		
	
	1.4 Output
		
		- A csv file with the Type(Beach, Heritage, Hill Station), Location, corresponding urls, # of sight seeing.




***********************************Step 2 - Extraction of attraction description details from HolidayIQ.com******************************************

1.Prerequisites

	1.1 Files required

		allBeachDesc.py
		allHillDesc.py
		allHeritageDesc.py

	1.2 Python packages 
		python 3.x
		Scrapy

2.How to run?

	- The above three programs contains the list of url's for the respective categories as input(request)
        - In the settings.py file set ROBOTSTXT_OBEY rule to false, set AUTOTHROTTLE_ENABLED = True and  HTTPCACHE_ENABLED = True to 
	   prevent from getting blocked.	
	- Scrapy code execution systax is: scrapy crawl <name as specified in the identity section in the program> -o <filename>.csv
	

3.Outputs
	<file1>.csv   - contains Place, Attraction name and Description for all the beaches from HolidayIQ
	<file2>.csv   - contains Place, Attraction name and Description for all the hillstations from HolidayIQ
	<file3>.csv   - contains Place, Attraction name and Description for all the heritages from HolidayIQ

***********************************Step 3 - Extraction of Review details from HolidayIQ.com******************************************

1.Prerequisites

	1.1 Files required

		BeachReviews.py
		HillStationReviews.py
		HeritageReviews.py

	1.2 Python packages 
		python 3.x
		Scrapy
		json

2.How to run?

	- The above three programs contains the list of url's for the respective categories as input(request)
        - In the settings.py file set ROBOTSTXT_OBEY rule to false, set AUTOTHROTTLE_ENABLED = True and  HTTPCACHE_ENABLED = True to 
	   prevent from getting blocked.	
	- Scrapy code execution systax is  scrapy crawl <name as specified in the identity section in the program> -o <filename>.csv
	- Since the pagination is dynamic in nature, we have to transform the input urls using the request url we get from the XHR.
	   We also need to key in the Authorization header in order for the request to work outside the browser.
	

3.Outputs

	<file1>.csv   - contains Review Heading and User review comments for the first 100 review comments for each attraction for all the beaches from HolidayIQ
	<file2>.csv   - contains Review Heading and User review comments for the first 100 review comments for each attraction for all the hillstations from HolidayIQ
	<file3>.csv   - contains Review Heading and User review comments for the first 100 review comments for each attraction for all the heritages from HolidayIQ



