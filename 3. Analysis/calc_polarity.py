import pickle
sentword=pickle.load(open('sentiword_dump.p','rb'))        
adav=["JJ", "JJR", "JJS", "RB", "RBR", "RBS"]
nnegative = ['not', 'Not', "n't"]
noun = ["NN", "NNS", "NNP", "NNPS"]
positive =1
negative = -1
neutral=0
polarity_dict={}
sentic={}
sentic_loaded = False

def load_Sentic():
    global sentic_loaded
    sent_file = open('senticnet5.txt', 'rt',encoding='utf8')
    print('Loading Sentic word list...')
    for line in sent_file.readlines():
        sent = line.split('\t')
        sent=[i.replace('\n','') for i in sent if i != '']
        sentic[sent[0]]=sent[2]
        sentic_loaded = True
        
def extractor(words = [], sid=0,sentence={}):               
    inner={}
    polarity_dict={}
    for j in words:                        
        lit=[]
        flag=0
        p =  sentence[sid][j]                
        if sentence[sid][j]['pos_tag'] in noun:        
            for i in p:
                if i != 'pos_tag':               
                    if wordInSentic(p[i]):           
                        flag=1                
                        if float(sentic[p[i]])>0:   
                            lit.append(positive)    
                        elif float(sentic[p[i]])<0:
                            lit.append(negative)
                        else:
                            lit.append(neutral)
                    elif p[i] in nnegative:           
                        flag=1
                        lit.append(negative)
                    
                    elif wordInsentiwordnet(p[i]):        
                        flag=1                
                        if sentword[p[i]] =='1':
                            lit.append(positive)
                        elif sentword[p[i]] == '0':
                            lit.append(neutral)
                        else:
                            lit.append(negative)
                
            if flag==0:                
                if wordInSentic(j):
                    flag=1
                    if float(sentic[j])>0:
                        lit.append(positive)
                    elif float(sentic[j])<0:
                        lit.append(negative)
                    else:
                        lit.append(neutral)
                elif j in nnegative:
                    lit.append(negative)
                elif wordInsentiwordnet(j):
        
                    if sentword[j] =='1':
                        lit.append(positive)
                    elif sentword[j] == '0':
                        lit.append(neutral)
                    else:
                        lit.append(negative)
            if flag == 0:                    
                lit.append(neutral)
        k=0
        for i in lit:                          
            k=k+i                            
            if k >0:
                inner[j]='positive'
            if k == 0:
                inner[j]='neutral'
            if k < 0:
                inner[j]='negative'
    polarity_dict[sid]=inner
    return(polarity_dict)
    
def wordInsentiwordnet(i):
    if i in sentword:
        return True
    else:
        return False

def wordInSentic(word = ""):
    if word in sentic:
        return True
    else: # if: word in sentic xml 
        return False

def compute_polarity(aspects,sid,sentence):
    global sentic_loaded
    if not sentic_loaded:
        load_Sentic()
    #get words as dictionary #graph            
    return(extractor(aspects, sid,sentence))

