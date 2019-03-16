# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import spacy
import pandas as pd

from spacy.symbols import *

stop_words=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", 
            "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", 
            "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", 
            "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", 
            "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", 
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", 
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", 
            "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", 
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "place", "places"]

_word_list=[]


def get_aspects(review):
    doc=nlp(review) ## Tokenize and extract grammatical components
    doc=[i.text for i in doc if i.text not in stop_words and i.pos_=="NOUN"] ## Remove common words and retain only nouns
    doc=list(map(lambda i: i.lower(),doc)) ## Normalize text to lower case
    doc=pd.Series(doc)
    doc=doc.value_counts().head(20).index.tolist() ## Get 5 most frequent nouns
    #doc=doc.value_counts().index.tolist()
    #return "The aspects are: "+", ".join(doc)
    return doc

def get_subtree(usr_comm):
    noun_phrases = ""
    word = nlp(usr_comm)
    word=[i.text for i in word if i.text not in stop_words]
        #if word.dep in np_labels:
    word_new = " ".join(word)
    word_new = nlp(word_new)
    for np in word_new.noun_chunks:
        noun_phrases = noun_phrases + " | " +  np.text
    #print(word.subtree.text)     
    return noun_phrases


def get_keywords(category):
    for index,row in atrs.iterrows():    
        if len(str(row['Description'])) > 3 and row['Website'] == 'HolidayIQ' and row['Category'] == category:
            word_l = get_aspects(row['Description'])
            detail = {'Attraction':str(row['Attraction_name']),'Keywords':str(word_l)}
            bow_l.append(detail)
            for word in word_l:
                _word_list.append({'Category':category,'Word':word})            
    df = pd.DataFrame(bow_l)
    df.to_csv(category + '_bow.csv',header=True)
        

nlp=spacy.load('en')
nlp.max_length = 1200000
atrs = pd.read_csv('Attractions_combined.csv')
bow_l=[]
atrs['Description'].dropna()

for c in atrs['Category'].unique():
    get_keywords(c)
    print(_word_list)

wl=pd.DataFrame(_word_list)


#Top 100 words for Beach
wl.query("Category=='Beach'").groupby(['Word'],as_index=False).count().rename(columns={'Category':'wcount'}).\
sort_values('wcount',ascending=False).head(100).to_csv('Beaches_top_100_words.csv')

#Top 100 words for Heritage
wl.query("Category=='Heritage'").groupby(['Word'],as_index=False).count().rename(columns={'Category':'wcount'}).\
sort_values('wcount',ascending=False).head(100).to_csv('Heritage_top_100_words.csv')


#Top 100 words for Hill-stations
wl.query("Category=='Hill-Station'").groupby(['Word'],as_index=False).count().rename(columns={'Category':'wcount'}).\
sort_values('wcount',ascending=False).head(100).to_csv('Hill-Station_top_100_words.csv')