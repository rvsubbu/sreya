import ipytest
import traceback

#ipytest.autoconfig()
import pandas as pd
#import pdb; pdb.set_trace()
requests = pd.read_csv("http://storage.googleapis.com/python-public-policy/data/cleaned_311_data_hw2.csv.zip")
print(type(requests))
print(requests.columns.tolist())
#for index, row in requests.iterrows():
    #print(index, row)
