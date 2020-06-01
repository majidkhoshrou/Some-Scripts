# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 11:53:03 2019

@author: MajidKhoshrou
"""
import numpy as np

from scipy.stats import norm

pos = 600
neu = 100
neg = 400

c = np.array([neg, neu, pos])
d2 = norm.cdf(c, loc=neu, scale = np.std(c) )
d2
neg1, neu1, pos1 = d2
score=neu1+pos1-neg1

score = max(score,0) and min(score, 1)
print("score: ", score)

myDict = {"a":5,"d":3,"c":6,"b":1}

sorted(myDict, key=lambda x: myDict[x], reverse=True)

sorted_keys = sorted(myDict, key=myDict.__getitem__, reverse=True)

{k:myDict[k] for k in sorted_keys }
    

import datetime
a = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")   
print(a) 

val = 1.0
isinstance(val, float)



x = int(input('enter a number:'))
if x%10 !=0:
    print(((x//10)+1)*10)
else:
    print(x)


#####################################################
    
r = {"Q2":"3","quest":"2","Q4":}

[val for val in r.values() if val.isdigit() and 1<= int(val) <= 5]

def get_score(r):
  """Get a dictionary of survey responses and returns a score."""
  return numpy.nanmean([int(val) for val in r.values() if val.isdigit() and 1<= int(val) <= 5])
  
get_score(r)


import numpy

mood = 1
while mood !=0:
    mood = float(input("enter mood: "))

    mood_color= "red" if (mood<0.4) else "green" if (mood>.6) else "yellow" if ~numpy.isnan(mood) else str(mood).lower()
    print("mood colour is: ", mood_color)



winnumber= 0
score=0
total_number=0
while total_number<30:
    num=int(input("enter the value:"))
    total_number=total_number+1
    score=score+num
    if num==3:
        winnumber=winnumber+1
print(score, winnumber)



    
def divisor_count(num):
    count = 0
    for i in range(1,num+1):
        if num%i==0:
            count += 1
    return count

    
input_count =0
max_count =0
while input_count <5:
    num = int(input())
    if divisor_count(num) >= max_count:
        max_count = divisor_count(num)
        max_num = max(num, max_num)
    input_count +=1
    
print(max_count, max_num )

import numpy
import datetime
import json

timestamp = str(datetime.datetime.now())
event_json = [{"id":"person1","Timestamp":timestamp},{"id":"person2","Timestamp":timestamp}]
event_json2 = json.dumps(event_json)

len_events = 3
random_vars = numpy.random.randint(-1,2, size=len_events)
print(random_vars)
for i in range(len_events):
  timestamp = str(datetime.datetime.now())
  val = str(random_vars[i])
  aux_var = json.dumps({"timestamp":timestamp, "value":val})
  print(aux_var)

rv1, rv2, rv3 = 1,2,3

import random

random.randint(1,3)

for ii in range(10):
    if not (ii %4):
        print(ii, "heyy")


from skimage.feature import match_template
    
    







































