# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 22:39:44 2018

@author: Shreshtha
"""

import pp
import time
import pandas as pd

#function to join the text from to columns
def test_func(df):
    x = []
    text=''
    df.reset_index(drop=True,inplace=True)
    for k in range(0,len(df)):
        if df['Body_emoji_desc'][k] == 'BODY_NA' and df['Subject_emoji_desc'][k]  == 'SUB_NA':
            text = str(df['Translated Subject'][k])  + " " + str(df['Translated Body'][k] )
        else:
            text = str(df['Subject_emoji_desc'][k]) + " " +str(df['Body_emoji_desc'][k]) 
        x.append(text)
    return x


#Initial data processing
data = pd.read_csv("../data/cleaned_data_w_translations.csv")
data.shape

data['Body_no_emoji'].fillna('BODY_NA',inplace=True)
data['Body_emoji_desc'].fillna('BODY_NA',inplace=True)
data['Subject_no_emoji'].fillna('SUB_NA',inplace=True)
data['Subject_emoji_desc'].fillna('SUB_NA',inplace=True)

data.drop(data[data['Translated Subject'].isnull() & data['Translated Body'].isnull() \
      &(data.Body.isnull()) & (data.Subject.isnull()) ].index,axis=0,inplace=True)

#serial processing time for benchmarking
print(time.time())
ll = test_func(data[60000:120000])
print(time.time())

#parallel processing code with pp
ppservers = () #this is mainly used in clustered env and names of the nodes are given here.
                #used here for demonstration purposes only
job_server = pp.Server(ncpus =5,ppservers=ppservers) #start the job with 5 workers
print ("Starting pp with %d workers" %( job_server.get_ncpus()))
start_time = time.time()
x_all = []
#input load division
inputs = (data[0:60000],data[60000:120000],data[120000:180000],data[180000:240000],data[240000:300000],data[300000:360000],data[360000:len(data)])
#job submission
jobs = [(input_x,job_server.submit(test_func,(input_x,),(None,),("pandas",))) for input_x in inputs]
#result accumulation
for input_x,job in jobs:
    x_all.append(job())
len(x_all)
print ("Time elapsed: %f s" %(time.time() - start_time))
job_server.print_stats()