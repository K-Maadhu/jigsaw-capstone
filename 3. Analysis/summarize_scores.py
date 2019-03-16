# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 15:49:13 2019

@author: AnilNair

"""

import pandas as pd


terms_list=[]


def merge_temp(terms):
    print(type(terms.info()))
    


def merge_dicts(terms):
    s_dict ={}
    m_terms=[]
    pol_dict={}
    atrb_dict={}
    atrb_pol_dict={}

    #Every sentence for the attraction
    for index,x in terms.iterrows():        
       #Merge all terms
       s_dict = eval(x['aspect_terms'])
       
       #Every aspect term from the aspect dictionary
       for key in s_dict:
           m_terms.extend(s_dict[key])           
           pol_dict = eval(x['terms_polarity'])
           atrb_dict = eval(x['attributes'])
           pol_dict = pol_dict[key]
           atrb_dict = atrb_dict[key]
           
           for w in pol_dict.keys():
               if atrb_dict.get(w):
                   if not atrb_pol_dict.get(atrb_dict[w][0]):
                        atrb_pol_dict[atrb_dict[w][0]] = {'positive':0,'negative':0,'neutral':0}
               
           for tm in pol_dict.keys():
               if tm in atrb_dict.keys():
                   atrb_pol_dict[atrb_dict[tm][0]][pol_dict[tm]] += 1
           
    terms_list.append(m_terms)
    return atrb_pol_dict    
           
    
           


_data = pd.read_csv('all_sent_aspects.csv')
out_series = _data.groupby(['Atr_name','category','atr_id'],as_index=True)['aspect_terms','attributes','terms_polarity','category'].apply(merge_dicts)
op_df = pd.DataFrame({'Atr_name':out_series.index.get_level_values(0).tolist(), 'Category':out_series.index.get_level_values(1).tolist(),\
                      'Atr_id':out_series.index.get_level_values(2).tolist(),'Attribute_score':out_series,'Terms':terms_list[1:]})

atrcns=[]
for index,row in op_df.iterrows():
    atrcn_dict={}
    
    atrbs_dict = eval(str(row['Attribute_score']))
    for atrs in atrbs_dict.keys():
        atrcn_dict={}
        atrcn_dict['Atr_name'] = row['Atr_name']
        atrcn_dict['Category'] = row['Category']
        atrcn_dict['Atr_id'] = row['Atr_id']
        atrcn_dict['Attribute'] = str(atrs)
        atrcn_dict['Attribute_score_pos'] = atrbs_dict[atrs]['positive']
        atrcn_dict['Attribute_score_neg'] = atrbs_dict[atrs]['negative']
        atrcn_dict['Attribute_score_neu'] = atrbs_dict[atrs]['neutral']
        atrcn_dict['Attribute_final_score'] = atrbs_dict[atrs]['positive'] / (atrbs_dict[atrs]['negative'] + atrbs_dict[atrs]['positive'] + atrbs_dict[atrs]['neutral']) * 100
        atrcns.append(atrcn_dict) 
      
pd.DataFrame(atrcns).to_csv('Attraction_detail_with_score.csv')        












