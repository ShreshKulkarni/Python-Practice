# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 08:53:57 2018

@author: swagat
"""

from concurrent.futures import ProcessPoolExecutor
import nltk
from nltk.corpus import inaugural
from nltk.corpus import stopwords
from collections import Set
import os

#filter out all punctuations and non-alphabetic characters
def filterPunctAndStopwords(word_list,funct):
    if len(word_list) == 0:
        return []
    
    filtered_list=[]
    if funct == "punct":
        filtered_list= [w for w in word_list if w.isalnum()]
    elif funct == "stopwords":
        if type(word_list[0]) == tuple:
            filtered_list = [(w1,w2) for (w1,w2) in word_list if not w1 in list(stopwords.words('english')) and not w2 in list(stopwords.words('english')) ]
        else:
            filtered_list = [w for w in word_list if not w in list(stopwords.words('english'))]
    elif funct == "both":
        if type(word_list[0]) == tuple:
            filtered_list = [(w1,w2) for (w1,w2) in word_list if w1.isalnum() and w2.isalnum() and not w1 in list(stopwords.words('english')) and not w2 in list(stopwords.words('english')) ]
        else:
            filtered_list = [w for w in word_list if w.isalnum() and not w in list(stopwords.words('english')) ]
    return filtered_list  

def calc_freq_dist(text,size=3):
    """
    Extract unigrams and two-word tuples in the windows and create a 
    FrequencyDist dictionary for both (and returns them in a list)
    """
    print(size)
    unigrams = []
    tuples = []
    # Scan over windows of the appropriate size.
    for center in range(size, len(text)-size):
        # enter the coocurrence (center word and each of all other words) in the dictionary
        wunis = set()
        wtuples = set() # for tuples in this context; set is to count only once
        thisword = text[center]
        
        # iterate though the test of the window
        for i in range(1, size+1): # i starts from 1 (center +/- i)
            nextleft = text[center-i]
            nextright = text[center+i]
            # add them next word in this window's unigram set
            wunis.add(nextleft)
            wunis.add(nextright)
            # create the next left tuple
            if not thisword == nextleft:
                if thisword < nextleft:
                    tup = (thisword,nextleft)
                else:
                    tup = (nextleft,thisword)
                # and add it in this window's tuple set
                wtuples.add(tup) #
            # create the next right tuple
            if not thisword == nextright:
                if thisword < nextright:
                    tup = (thisword,nextright)
                else:
                    tup = (nextright,thisword)
                # and add it in this window's tuple set
                wtuples.add(tup) #
        
        # add all unigrams in the text tuples list
        for wuni in wunis:
            unigrams.append(wuni)
        # add all tuples in the text tuples list
        for wtup in wtuples:
            tuples.append(wtup)
        
       # unigrams = [w for w in unigrams if len(w) > 2]
        #unigrams = filterPunctAndStopwords(unigrams,"stopwords")
        #import pdb;pdb.set_trace()
        #tuples = [(w1,w2) for (w1,w2) in tuples if len(w1) >2 and len(w2) >2]
        #tuples = filterPunctAndStopwords(tuples,"stopwords")
        
        if(i%100 == 0):
            print("Processed %d records.........." %(i))

    unigrams = [w for w in unigrams if len(w) > 2]
    unigrams = filterPunctAndStopwords(unigrams,"stopwords")
    #import pdb;pdb.set_trace()
    tuples = [(w1,w2) for (w1,w2) in tuples if len(w1) >2 and len(w2) >2]
    tuples = filterPunctAndStopwords(tuples,"stopwords")
    # create a frequency dictionary from unigrams and tuples    
    ufd = nltk.FreqDist(unigrams)
    cfd = nltk.FreqDist(tuples)
    # and return the dictionaries in a list
    return [ufd, cfd]

def main():
    #Divide the corpus in pre-post WWI 
    preWWIFileIds=[]
    postWWIFileIds=[]
    for filename in inaugural.fileids():
        if filename.split('-')[0] <= '1913':
            preWWIFileIds.append(filename)
        elif filename.split('-')[0] >'1917':
            postWWIFileIds.append(filename)
    
    print("Items in preWWI corpus = %d\nItems in postWWI corpus = %d" %(len(preWWIFileIds),len(postWWIFileIds)))
    
    #creating unigrams out of preWWI text
    #unigrams_preWWI = nltk.wordpunct_tokenize(preWWIText)
    unigrams_preWWI = [w.lower() for w in inaugural.words(preWWIFileIds)]
    
    #Creating unigrams out of postWWI text
    #unigrams_postWWI = nltk.wordpunct_tokenize(postWWIText)
    unigrams_postWWI = [w.lower() for w in inaugural.words(postWWIFileIds)]
    print("len of preWWI tokens = %d\nlen of postWWI tokens=%d\n" %(len(unigrams_preWWI),len(unigrams_postWWI)))
    
    list_text = []
    step = 1000
    sliding_win_size = 3
    all_token_list = unigrams_postWWI[:10000]
    
    for ind in range(0,len(all_token_list),step):
        start_ind = ind -sliding_win_size if ind > 0 else ind
        end_ind = ind + step + sliding_win_size if ind +step+sliding_win_size < len(all_token_list) else len(all_token_list)
        list_text.append(all_token_list[start_ind:end_ind])
    
    print("Size of partitions = %d" %(len(list_text)))
    postWWI_unigrams_fd = []
    postWWI_bigrams_fd = []
    #sliding_win_size = 3
    #list_text = [unigrams_postWWI[0:100],unigrams_postWWI[97:203]]
    with ProcessPoolExecutor(5) as executor:
        for token_list, token_fds in zip(list_text, executor.map(calc_freq_dist, list_text,[sliding_win_size]*len(list_text))):
            print('Len of tokens processed = %d\nLen of unigrams =%d\nLen of tuples = %d' % (len(token_list), len(token_fds[0]),len(token_fds[1])))
            postWWI_unigrams_fd.extend(token_fds[0])
            postWWI_bigrams_fd.extend(token_fds[1])
        
    print('Len of unigrams processed = %d\nLen of bigrams =%d' % (len(postWWI_unigrams_fd), len(postWWI_bigrams_fd)))

if __name__ == '__main__':
        main()

