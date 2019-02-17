# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 13:39:32 2019

@author: nagralegaurav18
"""

import re
import pandas as pd

def pre_processing(sentence):
    
    sentence = sentence.replace('amp','')
    sentence = re.sub('[@#]','',sentence)
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    sentence = pattern.sub('',sentence)
    sentence = re.split('[^a-zA-Z\']', sentence)
    
    return sentence

#calculate probability of a word for a category
def calc_prob(word, category):
    
    if word not in feature_set or word not in dataset[category]:
        
        return float(1/no_of_items[category])
    
    return float(dataset[category][word] + 1)/no_of_items[category]

def sentence_prob(test, category):
    
    spl_data = pre_processing(test)
    sp = 1
    
    for i in spl_data:
        
        if len(i) > 2:
            
            sp *= calc_prob(i.lower(),category)
            
    return sp

def naive_bayes_classifier(test):
    
    results = {}
    
    for i in dataset.keys():
        
        cat_prob = float(no_of_items[i]) / sum(no_of_items.values())
        test_prob = sentence_prob(test, i)
        results[i] = test_prob * cat_prob
        
    return results

if __name__ == '__main__':
    
    reader = pd.read_csv("basic_data.csv")
    
    #if polarity is NaN, replace it with 0
    reader['POLARITY'] = reader['POLARITY'].fillna(0).astype(int)
    
    #label(positive/negative) : {word : count of number of occurences of the word}
    dataset = {}
    
    #label l : No. of records that are labeled l
    no_of_items = {}
    
    #word : {label l : count of the occurence of word with label l}
    feature_set = {}
    
    for row in reader.iterrows():
        
        no_of_items.setdefault(row[1][1] + 1,0)
        no_of_items[row[1][1] + 1] += 1
        dataset.setdefault(row[1][1] + 1, {})
        split_data = pre_processing(row[1][0])
        
        for i in split_data:
        
            if len(i) > 2:
                
                dataset[row[1][1] + 1].setdefault(i.lower(), 0)
                dataset[row[1][1] + 1][i.lower()] += 1
                feature_set.setdefault(i.lower(), {})
                feature_set[i.lower()].setdefault(row[1][1] + 1, 0)
                feature_set[i.lower()][row[1][1] + 1] += 1
            
