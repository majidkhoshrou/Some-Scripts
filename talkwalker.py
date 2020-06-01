# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 12:59:05 2020

@author: MajidKhoshrou
"""

import datetime
import re
import numpy
numpy.seterr(divide='ignore', invalid='ignore')
import logging
from functools import reduce
from operator import getitem

from scipy import stats
from scipy.stats import zscore
import requests
import json
import uuid

import itertools

from itertools import compress



s = "philips+sourcecountry:us, gender:male+ sentiment:neutral"
s = " + ".join(s.split("+"))
s = " + ".join(s.split(","))



json_param = {"sourcecountry":["nl","uk"], "gender":["male"], "lang":["en", "es"]}
mydict = []
for c in json_param.keys():
    for i in range(len(json_param[c])):
        mydict.append({c:json_param[c][i]})
  

l1 = []
d1 = {}
l2=[]

for i in range(len(mydict)):
    d1 = {}
    for j in range(len(mydict)):
        print(d1.keys())
        if [*mydict[j]][0] not in list(d1.keys()):
            d1.update(mydict[j])
        l1.append(d1)
        
[*mydict[0]][0]


s = "&q=times  + sourcetype:SOCIALMEDIA + sourcetype:ONLINENEWS +  demographic:occupation-artist_art"
a = s.split("+")  
[i for i in a if 'demographic:' not in i ]

[i for i in a if 'sourcetype:SO' not in i and 'sourcetype:BRO' not in i and 'demographic:' not in i ]

re.sub('demographic:\w\s]+', '', a[-1])
    
    
    
    
    
url = 'https://api.talkwalker.com/api/v2/talkwalker/p/9f7ec52e-d136-411e-9357-8237608201c2/resources?access_token=d11e703e-0cd4-489d-b07b-0833ff6d2560_cg2phCvSlsilq-ZXFANPNhWBdtngASp6BPjBLwuSFqnJVghqNBf-Hh2pgrCbOTTJuORPX57BZVjZ-Ej8Ps6u3ILe9pP8XUN7k07B5kAWRhx9oY93VUHPqkV2QwhEUQHuLvQUuw0oNrdQ1a9CmZ33zz3AcV4XrRoK2vzMzmPgFZs'

response = requests.request("GET", url)
json_data = json.loads(response.text)
json_data

json_data.keys()

all_resources = json_data['result_resources']['projects'][0]

all_resources['topics']
all_resources['filters']
all_resources['channels']
all_resources['events']

keys_list = ['topics', 'filters','channels']

results = []
for k in keys_list:
    try:
        results += list(filter(len,([list(compress(all_resources[k][i]['nodes'],[d['title'] == 'Bakeri' for d in all_resources[k][i]['nodes']])) for i in range(len(all_resources[k]))])))
    except:
        pass
 

results[0][0].get('id','')



results[0][0]['id']



results_dict ={}       
for k in keys_list:
    try:
        results_dict[k]= list(filter(len,([list(compress(a[k][i]['nodes'],[d['title'] == 'Bakeri' for d in a[k][i]['nodes']])) for i in range(len(a[k]))])))
    except:
        pass     
results_dict['topics']    
    
    
    
x  = list(filter(len, results))

[[]l for l in x]


[list(compress(a[0]['filters'][i]['nodes'],[d['title'] == 'Bakeri' for d in a[0]['filters'][i]['nodes']])) for i in range(len(a[0]['filters']))]


list(compress(a[0]['filters'][0]['nodes'],[d['title'] == 'bakeri' for d in a[0]['filters'][0]['nodes']]))

[list(compress(a[i]['topics'][0]['nodes'],[d['title'] == 'bakeri' for d in a[i]['topics'][0]['nodes']])) for i in range(len(a))]
    
k = 'topics'
    
aux = [ {i['title']:i['id'] for i in b[j]['topics'][0]['nodes'] } for j in range(len(a))]

[j.get('bakeri', '1') for j in [ {i['title']:i['id'] for i in a[j]['topics'][0]['nodes'] } for j in range(len(a))]]

range(len(a))


{i['title']:i['id'] for i in a[0]['topics'][0]['nodes'] }
    

    
    
a = 1
b= ''
if a == 1 and b:
    print('Yes!')
else:
    print('No!')
    
####################################################################################
######################################################
queryjson = json.dumps({

"gender": ["female"],

"lang":["en", "es"],

"demographic":["occupation-artist_art", "interst-advertisting_marketing"],

"sourcetype":["SOCIALMEDIA"],

})
  
a = json.loads(queryjson)

b = [[{k:v} for v in a[k]] for k in a.keys()]
res = list(itertools.product(*b))
m = res[-1]

merged_dcit = [{k:v for d in res[j] for k, v in d.items()} for j in range(len(res))] 
" + ".join(json.dumps(merged_dcit[0]).replace('{',"").replace('}',"").split(','))

#########################################################################
#############################################################




"age":["AGE-65+"]
    
not a['sourcecountry']

L =[]
for k in a.keys():
    L.append([{k:v for v in a[k]}])
    
 

from collections import ChainMap

b = [[{"gender:male"}],[{"demographic":"occupation-artist_art"}, {"demographic":"interst-advertisting_marketing"}], [{"lang":"en"}, {"lang":"es"}]]
res = list(itertools.product(*b))

[dict(ChainMap(*d)) for d in [list(r) for r in res]]

ex = [{'gender:male'}, {'demographic': 'occupation-artist_art'}, {'lang': 'en'}]

dict(ChainMap(*ex))
    

f = str(2)
    
 str('2')   
    
    
    
import requests

url = "http://mbvapi-dev.maistering.com/notification/api/Notification/Notification"

payload = "{\r\n        \"NotificationType\": 1,\r\n        \"publisherId\": 7,\r\n        \"Title\": \"coinbase sucks!\",\r\n        \"Body\": \"Mohita Shrivastava added you to  Ideation - Q2 2020 Planning\",\r\n        \"Priority\": 1,\r\n        \"MessageTargets\": [\r\n            {\r\n                \"TargetSource\": 1,\r\n                \"UserInfo\": [\r\n                    {\r\n                        \"UserName\": \"Muralidaran Sankaralingam\",\r\n                        \"Email\": \"muralidaran.sankaralingam@m365x119746.onmicrosoft.com\",\r\n                        \"isRead\": false\r\n                    }\r\n                ]               \r\n            }\r\n        ],\r\n        \"IconUrl\": \"https://devmccdnblobs.blob.core.windows.net/journey/Journey_icon-01.svg\",\r\n        \"ImageUrl\": \"https://mbvmaisteringdataadls.blob.core.windows.net/dynamicimages/Finance87.jpg\",\r\n        \"BadgeUrl\": null,\r\n        \"Action\": [\r\n            {\r\n                \"Title\": \"Join Ideation\",\r\n                \"Action\": 2,\r\n                \"ActionIcon\": \"https://devmccdnblobs.blob.core.windows.net/journey/Journey_icon-01.svg\",\r\n                \"ActionData\": {\r\n                     \"journeyId\": \"b3a569e7-64db-424b-b678-5ae255728d84\",\r\n                     \"journeyName\": \"Aaa_Test\"\r\n                }\r\n            },\r\n            {\r\n                \"Title\": \"Send Idea\",\r\n                \"Action\": 2,\r\n                \"ActionIcon\": \"https://devmccdnblobs.blob.core.windows.net/journey/Journey_icon-01.svg\",\r\n                \"ActionData\": {\r\n                     \"journeyId\": \"b3a569e7-64db-424b-b678-5ae255728d84\",\r\n                     \"journeyName\": \"Aaa_Test\"\r\n                }\r\n            }],\r\n        \"Data\": null,\r\n        \"created_by\": \"mohita.shrivastava@m365x691793.onmicrosoft.com\"\r\n    }"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
