# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 20:17:20 2018

input - csv file with non ASCII characters
output - csv file after removing the non ASCII characters

@author: Hiran Kumar
"""
    
import csv

in_file = r"C:/Users/Hiran/Desktop/virtual_workspace/demo_project/Reviews_combined.csv"
csv_file = r"C:/Users/Hiran/Desktop/virtual_workspace/demo_project/Reviews_combined_Cleaned.csv"

in_txt = csv.reader(open(in_file, "rt", encoding="utf8"  ), delimiter = ',')

f = open(csv_file, 'wt')        
out_csv = csv.writer( f)

out_txt = []
for row in in_txt:
#    print(row)
    out_txt.append([
        "".join(a if ord(a) < 128 else ' ' for a in i)
        
        for i in row
    ])

out_csv.writerows(out_txt)

f.close()






