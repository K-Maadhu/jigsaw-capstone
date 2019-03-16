# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 23:03:00 2018

@author: AnilNair
"""

#from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
import calc_polarity
import map_terms_to_attributes
import os
import argparse


class DummyLemmatizer:
    def lemmatize(self,word):
        return word

 
point1 = ["VBD", "VB", "VBG", "VBN","VBP", "VBZ", "JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
point2 = ["JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
verb = ["VBD", "VB", "VBG", "VBN","VBP", "VBZ"]
noun = ["NN", "NNS", "NNP", "NNPS"]
adverb =["RB", "RBR", "RBS"]
adjective = ["JJ", "JJR", "JJS"]
auxiliary_verb = ["be" , "am" , "are", "is", "was", "being", "can", "could", "do", "did", "does", "doing", "have", "had",
         "has", "having", "may", "might", "might", "must", "shall", "should", "will", "'ve", "n't", "were"]
asdict={}
forpol=[]
sentic={}
asp_list=[]
pol_list=[]
cat_list=[]
atr_id_list=[]
atr_cat_list=[]
atrs_dict={}

def loadSentic():
    sent_file = open('senticnet5.txt', 'rt',encoding='utf8')
    for line in sent_file.readlines():
        sent = line.split('\t')
        sent=[i.replace('\n','') for i in sent if i != '']
        sentic[sent[0]]=sent[2]
        
    reviews = pd.read_csv('Reviews_combined_cleaned.csv')   
    reviews = reviews.fillna('')
    unq_atrs = reviews.groupby(['Attraction_name','place','Category','attraction_id'], as_index = False)['review_id'].count()
    
        
    for index,row in unq_atrs.iterrows():
       atrs_dict[row['Attraction_name'] + row['place']] = {'Category':row['Category'],'attraction_id':row['attraction_id']}
    
    del reviews,unq_atrs

def extractor(words = {}, sid=0):
    pol=[sid]
    aspect_terms=[]
    has_auiliary = getAuxiliary(words)
    hasNsubj = findNsubj(words)
    if(hasNsubj):
        for word in words.keys():
            if(not words[lem.lemmatize(word)].get("nsubj")):
                continue
            if (words[lem.lemmatize(word)]["pos_tag"] in verb and checkModifiers(words, word)):
                aspect_terms.append(word)
                pol.append(word)
            
                #Point 3
            elif (not has_auiliary and words[lem.lemmatize(word)].get("dobj") and isNoun(words, words[lem.lemmatize(word)]["dobj"])):
                    if (not wordInSentic(words[lem.lemmatize(word)]["dobj"])):
                        aspect_terms.append(words[lem.lemmatize(word)]["dobj"])
                        j = words[lem.lemmatize(word)]["dobj"]
                        pol.append(j)
                    else:
                        aspect_terms.append(words[lem.lemmatize(word)]["dobj"])
                        pol.append(words[lem.lemmatize(word)]["dobj"])
                        word1 = getNounConnectedByAny(words, words[lem.lemmatize(word)]["dobj"])
                        if (word1):
                            aspect_terms.append(word1)
                            pol.append(word1)
                #point 2 
            elif not has_auiliary and getAdverbOrAdjective(words, word) :
                    if(words[lem.lemmatize(word)].get("nsubj") and not ("DT" in words[lem.lemmatize(words[lem.lemmatize(word)]["nsubj"])]["pos_tag"])):
                        aspect_terms.append(words[lem.lemmatize(word)]["nsubj"])
                        pol.append(words[lem.lemmatize(word)]["nsubj"])
                    #if(not ("DT" in words[lem.lemmatize(word)]["pos_tag"] or "PRP" in words[lem.lemmatize(word)]["pos_tag"])):
                    aspect_terms.append(word)
                    pol.append(word)
                #Point 4
            elif not has_auiliary and (words[lem.lemmatize(word)].get("xcomp")):
                    xcomp = words[lem.lemmatize(word)]["xcomp"]
                    word1 = getNounConnectedByAny(words, xcomp)
                    if(word1):
                        aspect_terms.append(word1)
                        pol.append(word1)
            #Point 5 & 6 & 7
            elif(words[lem.lemmatize(word)].get("cop")):
                dep = getDependency(words, word)
                copv = words[lem.lemmatize(word)]["cop"]
                if(words[lem.lemmatize(word)]["pos_tag"] in noun):
                    aspect_terms.append(word)
                    pol.append(word)

                if(words[lem.lemmatize(word)].get("nsubj") and  not ("DT" in words[lem.lemmatize(words[lem.lemmatize(word)]["nsubj"])]["pos_tag"] 
                    or "PRP" in words[lem.lemmatize(words[lem.lemmatize(word)]["nsubj"])]["pos_tag"])):
                    aspect_terms.append(words[lem.lemmatize(word)]["nsubj"])
                    pol.append(words[lem.lemmatize(word)]["nsubj"])
                if(dep):
                    aspect_terms.append(dep)
                    pol.append(dep)

    else:
        for word in words.keys():
            prepN = hasPropositionalNoun(words, word)
            tmp = getVmodorXcomp(words, word)
            if(tmp and wordInSentic(tmp)):
                aspect_terms.append(word)
                pol.append(word)
            elif(prepN):
                if(words[lem.lemmatize(word)].get("appos")):
                    aspect_terms.append(words[lem.lemmatize(word)]["appos"])
                    pol.append(words[lem.lemmatize(word)]["appos"])
                #else:
                #    print word
                aspect_terms.append(prepN)
                pol.append(prepN)
            elif(words[lem.lemmatize(word)].get("dobj")):
                tmp1 = words[lem.lemmatize(words[lem.lemmatize(word)]["dobj"])]["pos_tag"]
                if( not (("DT" in tmp1) or ("PRP" in tmp1))):
                    aspect_terms.append(words[lem.lemmatize(word)]["dobj"])
                    pol.append(words[lem.lemmatize(word)]["dobj"])
             
    forpol.append(pol)
    pol=[]
    return aspect_terms

def getVmodorXcomp(words={}, word=""):
    for key in words[lem.lemmatize(word)].keys():
        if((key == "vmod" or key == "xcomp")):
            tmp =  words[lem.lemmatize(word)][key]
            if(words[tmp]["pos_tag"] in (adverb or adjective)):
                return tmp
    return None

def hasPropositionalNoun(words={}, word=""):
    for key in words[lem.lemmatize(word)].keys():
        if ("prep" in key):
            tmp = words[lem.lemmatize(word)][key]
            tmp=lem.lemmatize(tmp)
            if(words[tmp]["pos_tag"] in noun):
                return tmp
    return None

def getAuxiliary(words={}):
    for word in words.keys():
        for key in words[lem.lemmatize(word)]:
            if("aux" == key):
                return True
    return False

def getDependency(words={}, word=""):
    for key in words[lem.lemmatize(word)].keys():
        try:
            tmp = words[lem.lemmatize(word)][key]
            if(key != "xcomp"):
                continue
            if(words[lem.lemmatize(tmp)]["pos_tag"] in verb):
                return tmp
        except:
            continue
    return None

def findNsubj(words={}):
    for key in words.keys():
        if(words[lem.lemmatize(key)].get("nsubj")):
            return True
    return False

def checkModifiers(words = {}, word=""):
    try:
        tmp = words[lem.lemmatize(word)]["amod"]
        return wordInSentic(tmp)
    except:
        pass
    try:
        tmp = words[lem.lemmatize(word)]["advmod"]
        return wordInSentic(tmp)
    except:
        pass
    return False

def getProposition(words = {}, word=""):
    if (word=="" or len(words)==0):
        return None
    for i in words[lem.lemmatize(word)].keys():
        if "prep" in i:
            return i
    return None

def getAdverbOrAdjective(words = {}, word=""):
    for key in words[lem.lemmatize(word)].keys():
        tmp = words[lem.lemmatize(word)][key]
        try:
            if(key == "advmod"):
                return True
            elif(words[lem.lemmatize(tmp)]["pos_tag"] in (adverb + adjective)):
                return True
        except:
            continue
    return False

def getNounConnectedByAny(words={}, word=""):
    if (word=="" or len(words)==0):
        return None
    for dep in words[lem.lemmatize(word)].keys():    
        try:
            if (words[words[lem.lemmatize(word)][dep]]["pos_tag"] in noun):
                return words[lem.lemmatize(word)][dep]
        except:
            continue

def isNoun(words={}, word=""):
    return (words[lem.lemmatize(word)]["pos_tag"] in noun)


def wordInSentic(word = ""):
    if word in sentic:
        return True
    else: # if: word in sentic xml 
        return False

def isInOpinionlexicon(word = ""):
    return wordInSentic(word)

def isNounSubject(words = {}):
    if (len(words) == 0):
        return None
    for word in words.keys():
        try:
            if words[lem.lemmatize(word)].get("nsubj"):
                return True
        except:
            return False
    return False
    

def check(words={}):
    aspects=extractor(words, '1')
 
def process_atr(sent_dict,atr_category,atr_id,batch_num):    

    for sid in sent_dict.keys():
    #get words as dictionary #graph
        aspects=extractor(sent_dict[sid], sid)
        aspects = list(set(aspects))
        asp_list.append({sid:aspects})
        polarities = calc_polarity.compute_polarity(aspects,sid,{sid:sent_dict[sid]})
        pol_list.append(polarities)
        categories = map_terms_to_attributes.get_attributes({sid:aspects},atr_category)
        cat_list.append(categories)
        atr_cat_list.append(atr_category)
        atr_id_list.append(atr_id)
    
    print('aspects_length', len(asp_list) )   
    print('sent_len' ,sent_dump_tmp.shape[0])    
    
    if len(sent_dump_tmp.columns) == 5:
        sent_dump_tmp.columns = ['Idx','Seq','Atr_name','Atr_place','Sent_id','nlp_parsed_op'] 
        

    
    sent_dump_tmp['aspect_terms'] = asp_list
    sent_dump_tmp['terms_polarity'] = pol_list
    sent_dump_tmp['attributes'] = cat_list
    sent_dump_tmp['category'] = atr_cat_list
    sent_dump_tmp['atr_id'] = atr_id_list
    
    #Write data into csv for the current attraction.
    wrtHdr = False
    try:
        if os.stat('sentence_dump_aspect_terms_'+ str(batch_num) +'.csv').st_size == 0:
            wrtHdr = True
    except:
        wrtHdr=True
        
    with open('sentence_dump_aspect_terms_'+ str(batch_num) +'.csv', 'a') as f:
        pd.DataFrame(sent_dump_tmp).to_csv(f,header=wrtHdr,encoding='utf-8')
        
    # Start from clean slate for the next attraction.    
    sent_dump_tmp.drop(sent_dump_tmp.index, inplace=True)
    asp_list.clear()
    pol_list.clear()
    cat_list.clear()
    atr_cat_list.clear() 
    atr_id_list.clear()  
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('batch_n')
    args = parser.parse_args()
    batch_num = args.batch_n
    
#    global sent_dump , sent_dump_tmp
#    global lem
    lem=DummyLemmatizer()
    loadSentic()
    sent_dict={}
    prev_atr=''
    sent_dump = pd.read_csv('sentence_dump_' + str(batch_num) + '.csv',header=None) 
    sent_dump=sent_dump.fillna('')
    sent_dump_tmp = pd.DataFrame()
    sent_dump.columns = ['Idx','Seq','Atr_name','Atr_place','Sent_id','nlp_parsed_op'] 
    sent_dump=sent_dump.fillna('')
    atr_count=0
    
    for index,row in sent_dump.iterrows():
        
        cur_atr=str(row['Atr_name']) + str(row['Atr_place'])        
        
        if cur_atr != prev_atr and len(sent_dict) > 0:
            atr_count+=1
            atr_category = atrs_dict[prev_atr]['Category']
            atr_id = atrs_dict[prev_atr]['attraction_id']
            process_atr(sent_dict,atr_category,atr_id,batch_num)
            sent_dict.clear()
            print('Processing complete for ' , prev_atr,' Attraction-count ',atr_count)
            
        sent_dump_tmp = sent_dump_tmp.append(row,ignore_index=True)    
        sent_dict.update(eval(row['nlp_parsed_op']))
        prev_atr=str(row['Atr_name']) + str(row['Atr_place'])
    
    if len(sent_dict) > 0:
        atr_category = atrs_dict[cur_atr]['Category']
        atr_id = atrs_dict[cur_atr]['attraction_id']
        process_atr(sent_dict,atr_category,atr_id,batch_num)
    


    