Cleaning
--------

SQL based cleanup using MySQL

cleanup_query.SQL 
The attractions info file and individual review comments file were imported into MySQL.
All review comment tables were consolidated into a single table.
The attraction and comments tables were cleaned for double-quotes, carriage returns and extra whitespaces.
Both the tables were written into a csv file for further processing.
Though we exported the csv files into MySQL using the MS-Excel plugin, the 'Import Data' feature of MySQL can also be used.

csvConvert.py
This program is used to remove all Non-ASCII (special) characters from an input csv file and will generate an output of a csv file. 
This program can be run without any dependencies. Please change the file name and path as required.


Pre-Processing
--------------

API based Geo-Encoding

_map_my_india_geocode.py
This program is used to extract address info for the given input using the maymyindia.com public API.
Please replace the API key present in the code with a valid value.
The program accepts the Attraction name along with the partial address as input and receives a JSON output from the site.
This program then parses the JSON to take only the State, District, Pincode and Lat/Long info and writes it into a csv file.

Exclude Irrelevant attraction info

Drop_attractions.py
As the data which was fetched from the source websites had info about various tour operators and other non-attractions based info, a list was manually prepared based on the attraction name and then used as a basis to remove that info from the attraction comments file.
This program takes the attraction comments file as input, removes all the comments for all those attractions which are mentioned in the program and generates a csv file as output. This exercise was done periodically to have info only for relevant attractions.

Bag of Words
generate_BOW_Descriptions.py

Python packages
NLTK
Spacy
	
Input files
Attractions_combined_cleaned.csv

Output
Beaches_top_words.csv
Heritage_top_words.csv
Hill-Station_top_words.csv
		
How to Run?
Make sure the required files are in the path and execute the below command
		python generate_BOW_Descriptions.py