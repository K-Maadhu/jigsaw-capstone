# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 18:22:06 2019

@author: AnilNair
"""
import pandas as pd
import extract_terms as et
from threading import Thread
import os


sent_dump = pd.read_csv(r'C:\Users\Administrator\PycharmProjects\CoreNLP\sentence_dump.csv',header=None)
beg=0
end=0


if __name__ == '__main__':
    
        
    tot_recs = sent_dump.shape[0]
    nbr_batches = 5
    
    i=0
    batch_count=1
    while 1==1:
        if i >= tot_recs:
            break
        
        i += int(tot_recs/nbr_batches)    
        end = i
        
        if end > tot_recs:
            end = tot_recs
            
        print(beg ,end)
        
            
        sent_tmp = sent_dump.iloc[beg:end,:]
        sent_tmp.to_csv('sentence_dump_' + str(batch_count) + '.csv', header=False)
        
        
        cmd = 'python -u extract_terms.py ' + str(batch_count) + ' > logfile_' + str(batch_count) + '.log'
        
        t1= Thread(target=os.system,args=(cmd,))
        t1.start()
        
        batch_count+=1
        beg = i
        


