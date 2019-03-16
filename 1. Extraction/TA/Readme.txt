
**********************************************************Important Note******************************************************************

This program was executed based on the structure of the Trip Advisor website as of December 2018. Please make necessary changes as required
to make this code working if the underlying strucutre of the website has been changed.

******************************************************************************************************************************************

*********************************** Step 1 - Extraction of attraction urls using search by category *****************************************************
1. Prerequisites

	1.1 Files required
		_trip_advisor_search_by_attr.py
	
	1.2 Python packages
		
		BeautifulSoup
		Selenium
		pandas
		python 3.x
		In addition to python packages make sure the chromium/firefox driver for seleium is downloaded and installed in the same machine.
	
	1.3 How to Run?
	
		- The program uses a search string hardcoded in the program and then extracts the urls of the attractions from the results.
		- Make sure to modify the search string as required before calling the program.
		- Program can be directly called from the command line.
	
	1.4 Output
		
		- A csv file with the urls.


***********************************Step 2 - Extraction of attraction details and reviews from TripAdvisor.com******************************************

1.Prerequisites

	1.1 Files required

		ta_reviewScrapper.py
		ta_scrapperMain.py
		_beaches_in_india_urls.csv
		_hills_stations_in_india_urls.csv
		_historical_sites_in_india_urls.csv

	1.2 Python packages 
		python 3.x
		pandas - use pip install pandas if not present
		beautifulsoup - use pip install bs4 if not present
		requests - use pip install requests if not present

2.How to run?

	a) Make sure all the python packages mentioned in section 1.2 is installed.
	b) Copy all the required filed (section 1.1) to a folder.
	c) Make sure python interpreter is added to path, check this by just typing python and press enter. quit() to come back to command line.
	d) Each csv file contains a list of urls for each category of attraction extracted from tripadvisor.com using search.
	e) ta_scrapperMain.py is the main program and expects the following parms:
		> csv-file-name-with-urls.csv e.g. _beaches_in_india_urls.csv
		> attraction_category e.g. beaches
		> number_of_reviews_to_be_extracted use 100 for our project to extract latest 100 reviews.
	f) Go to command line and execute the below command
	
		python ta_scrapperMain.py _beaches_in_india_urls.csv beaches 100
	
	g) Note that no quotes are required. Also replace the csv file name accordingly.
	h) If the program is running successfully, you should see some log statements printing on the console as shown below. 
		
		[parse] url: http://www.tripadvisor.in/Attraction_Review-g304554-d321412-Reviews-Chhatrapati_Shivaji_Terminus-Mumbai_Maharashtra.html?filterLang=en
		Extracted latest  100 of 4013 reviews for http://www.tripadvisor.in/Attraction_Review-g304554-d321412-Reviews-Chhatrapati_Shivaji_Terminus-Mumbai_Maharashtra.html?filterLang=en
		[Batch complete] Parsing complete for 990 urls. Took 28.810000000000173 seconds for batch - 99.0
		
	i) [parse] log will be printed for every url parsed.[Batch complete] log will be printed for every batch of 10 urls. Use this to monitor the progress
	   script.
	j) If running from windows, make sure the command prompt window is kept open and the computer is on and connected to internet.

3.Outputs
	Hotel_Details_<attraction_category>.csv   - contains attraction name and details
	Hotel_Reviews_<attraction_category>.csv   - contains review details
	parse_complete_urls.csv                   - This csv will contain all the urls for which the parse is complete. In case of restarting the script, this will be
												used to make sure that the scraping continues from where it left off.



