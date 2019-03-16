# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 22:27:31 2018

@author: AnilNair
"""

from nltk.corpus import wordnet
from operator import itemgetter
from itertools import product

aspects={}
list_heritage=[u'history','architecture','religion','culture','art']
list_beach=[u'cleanliness', u'view',u'activity',u'food']
list_hills = [u'view',u'landscape',u'activity',u'climate']
cats_dict={}
new_file={}
list_words=[]

def get_attributes(aspects,category):
    
    cats_dict={}
    new_file={}

    if category == 'Beach':
        list1=list_beach
    elif category == 'Hill-Station':
        list1 = list_hills
    elif category == 'Heritage':
        list1 = list_heritage    
    
#    print('Input category ',category, ' Attributes used are ', list1)
    
    for sid in aspects.keys():
        l=aspects[sid]
        g={}
        inner=[]
        categories_s=[]
        for asp in l:
            new={}
            inner=[]
            inner_new=[]
            categories=[]
            sense1=wordnet.synsets(asp.strip())
            for cat in list1:
                sense2=wordnet.synsets(cat)
                for s1,s2 in product(sense1,sense2):
                    score=wordnet.wup_similarity(s1,s2)
                    inner.append((score,s2))
            inner_new = [x for x in inner if x[0] is not None and x[0] > 0.5]
            inner_new = [x for x in inner_new if x[1].name().split('.')[0]  in list1]
            if len(inner_new)>0:
                topcat=sorted(inner_new,key=itemgetter(0),reverse=True)[0]
                print('score',sorted(inner_new,key=itemgetter(1),reverse=True)[0])
                categories.append(topcat[1].name()[:topcat[1].name().index('.')])
                new[asp]=list(set(categories))
                g.update(new)
                categories_s.extend(categories) 
            if len(categories) > 0:
                list_words.append({'word':str(asp),'Category':str(categories[0])})
        new_file[sid]=g
        cats_dict[sid]=list(set(categories_s))
    return(new_file)

