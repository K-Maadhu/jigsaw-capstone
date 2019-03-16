# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 00:33:35 2018

@author: MaadhuKanagasabesan
"""

import pandas as pd
import json, requests
from nltk.stem.wordnet import WordNetLemmatizer
import traceback
import re

processed_sents = []
full_comments = pd.read_csv('Reviews_combined_cleaned.csv')

try:
    #processed_sents = pd.read_csv('Processed_sents.csv').take([0], axis=1).values.tolist()
    processed_sents = pd.read_csv('Processed_sents.csv', header = None)
    processed_sents = processed_sents.iloc[:, 1]
    processed_sents = processed_sents.tolist()
except:
    processed_sents.clear()

class StanfordNLP:
    def __init__(self, server_url):
        # TODO: Error handling? More checking on the url?
        if server_url[-1] == '/':
            server_url = server_url[:-1]
        self.server_url = server_url

    def annotate(self, text, properties=None):
        assert isinstance(text, str)
        if properties is None:
            properties = {}
        else:
            assert isinstance(properties, dict)

        # Checks that the Stanford CoreNLP server is started.
        try:
            requests.get(self.server_url)
        except requests.exceptions.ConnectionError:
            raise Exception('Check whether you have started the CoreNLP server e.g.\n'
                            '$ cd <path_to_core_nlp_folder>/stanford-corenlp-full-2016-10-31/ \n'
                            '$ java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port <port> -timeout <timeout_in_ms>')

        data = text.encode()
        r = requests.post(
            self.server_url, params={
                'properties': str(properties)
            }, data=data, headers={'Connection': 'close'})
        output = r.text
        if ('outputFormat' in properties
                and properties['outputFormat'] == 'json'):
            try:
                output = json.loads(output, encoding='utf-8', strict=True)
            except:
                pass
        return output


# ip = open('Restaurants_Train_v2_parsed.txt',)

key_index = 0


def process_nlp(review):
    i = 0
    sentence = {}
    lem = WordNetLemmatizer()
    review = re.sub(r'(?<=[.,])(?=[^\s])', r' ', review)
    sent = [review]
    print("[INFO] Processing comment -", review, "of length ", len(review.strip('')))
    while i < len(sent):
        nlp = StanfordNLP('http://127.0.0.1:9000')
        result = nlp.annotate(sent[i], properties={
            "annotators": "tokenize,ssplit,parse",
            "outputFormat": "json",
            # Only split the sentence at End Of Line. We assume that this method only takes in one single sentence.
            "ssplit.eolonly": "false",
            # Setting enforceRequirements to skip some annotators and make the process faster
            "enforceRequirements": "false"
        })
        words = {}

        for each_sent in result['sentences']:
            words = {}
            for wl in each_sent['tokens']:
                innerd = {}
                innerd['pos_tag'] = wl['pos']
                for depl in each_sent['basicDependencies']:
                    if depl['governorGloss'] == wl['word']:
                        innerd[depl['dep']] = lem.lemmatize(depl['dependentGloss'])
                    elif depl['dependentGloss'] == wl['word']:
                        innerd[depl['dep']] = lem.lemmatize(depl['governorGloss'])
                words[lem.lemmatize(wl['word'])] = innerd
            global key_index
            sentence[key_index] = words
            i += 1
            key_index += 1
    return sentence


def write_processed_recs():
    global _comments
    global sent_dtls
    with open('Processed_sents.csv', 'a') as f:
        pd.DataFrame(_comments).to_csv(f, header=False, encoding='utf-8')
    _comments.clear()

    with open('sentence_dump.csv', 'a') as f:
        pd.DataFrame(sent_dtls).to_csv(f, header=False, encoding='utf-8')
    sent_dtls.clear()


print("\n")
full_comments['place'].fillna('', inplace=True)
method_result = []
prev_attr = ''
sent_dtls = []
row_count = 0
_comments = []

try:

    for index, row in full_comments.iterrows():
        cur_attr = str(row['Attraction_name'] + row['place'])

        # Reset the sentence counter if attraction changes
        if prev_attr != cur_attr:
            key_index = 0

        # Skip if sentence already processed
        if row['Review_text'] in processed_sents or row['Review_text'] in _comments:
            prev_attr = str(row['Attraction_name'] + row['place'])
            continue

        # Incase of exceptions skip and continue to next comment.
        try:
            sent_op = process_nlp(row['Review_text'])
        except Exception as e:
            print(Exception, e)
            traceback.print_exc()
            print('[ERROR] Error occured when processing:- ', row['Review_text'])
            prev_attr = str(row['Attraction_name'] + row['place'])
            continue

        # Populate the dictinoray with the output.
        for skey in sent_op.keys():
            sent_dtls.append({'Atr_name': row['Attraction_name'], 'Atr_place': row['place'], 'sent_id': skey,
                              'sent_nlp': {skey: sent_op[skey]}})
        row_count += 1

        prev_attr = str(row['Attraction_name'] + row['place'])

        # Add processed comment to the list
        _comments.append(row['Review_text'])

        # Write to file for every 100 comments.
        if row_count >= 100:
            write_processed_recs()
            row_count = 0

except Exception as e:
    print(e.__doc__)
    traceback.print_exc()
    print('[ERROR] Unexpected error occured when processing comments')

# Write to file for any remaining records after the batch
if row_count > 0:
    write_processed_recs()


