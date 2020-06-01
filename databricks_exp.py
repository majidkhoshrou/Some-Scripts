# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:31:18 2020

@author: MajidKhoshrou
"""

import pandas as pd



import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'df.csv')

df = pd.read_excel(my_file)




# 1: Old skool!
word = input("enter the word: ")
lower_count = 0
upper_count = 0
for c in word:
    lower_count = lower_count + int(c.islower())
    upper_count = upper_count + int(c.isupper())
    
if lower_count > upper_count:
    word = word.lower()
else:
    word = word.upper()
print("ouuput: ", word)

# 2: Doing list comprehensions
word = input("enter the word: ")
lower_count = sum([c.islower() for c in word])
upper_count = sum([c.isupper() for c in word])
if lower_count > upper_count:
    word = word.lower()
else:
    word = word.upper()
print("ouuput: ", word)

# 3: 
word = input("enter the word: ")
output = word.lower() if  sum([c.islower() for c in word]) > sum([c.isupper() for c in word]) else word.upper()
print(output)

my_input = "1+1+3+1+3"
seperator = "+"
numList = [str(j) for j in sorted([int(i) for i in my_input.split("+")])]
seperator.join(numList)





















