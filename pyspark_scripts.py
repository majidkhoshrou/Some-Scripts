
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 10:14:48 2020

@author: MajidKhoshrou
"""

from pyspark.sql.window import Window
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

import pyspark.sql.types as T
import pyspark.sql.functions as F

from itertools import compress

# [{k:v} for k,v in config.items()]


# read a table from db
df_all = spark.read.format("jdbc").option("url", insights_config['url']).option("dbtable", "talkwalker_emotion_metrics").option("user", insights_config['user'])\
.option("password", insights_config['password']).load()

df_all = df_all.filter(F.col('movement') != 'Null').withColumn('mood', F.col('mood').cast(T.DoubleType())).withColumn('movement', F.col('movement').cast(T.DoubleType())).sort(F.col('Date'))
display(df_all.collect())

##########################################################################################

# write a table to db
table_name = "talkwalker_change_type"
try:
  # .dropna() 
  spark_df_change_type.write \
          .mode("overwrite")\
          .format("jdbc") \
          .option("url", insights_config['url']) \
          .option("dbtable", table_name) \
          .option("user", insights_config['user']) \
          .option("password", insights_config['password']) \
          .save()

  print('Saving table: ' + table_name)
except:
  print('Error creating table: ' + table_name)

##########################################################################################
# a function

def run_talkwalker_sentiment_endpoint(url): 
  """
  Call talkwalker sentiment endpoint. Returns the corresponding mood and movevent results.
  """
  
  response = requests.request("GET", url)
  json_data = json.loads(response.text)

  output ={}
  output['Date'] = datetime.datetime.now()#         output["uuid"] = str(uuid.uuid4())

  try:
    output['raw_json_data'] = json.dumps(json_data)

    sentiment_results = { json_data["result_histogram"]["data"][i]['ks']: sum(json_data["result_histogram"]["data"][i]["v"]) for i in range(4) }
    total_hits = get_item_nested_dict(json_data, ["result_histogram", "total_hits"])

    output["sentiment_results"] = sentiment_results
    output["hits"] =  str(total_hits)

    neu, pos, neg = sentiment_results["NEUTRAL"], sentiment_results["POSITIVE"], sentiment_results["NEGATIVE"]
    mood = (MoodScoreFromSentiment(neu, pos, neg))
    mood_color= "red" if mood<=0.4 else "green" if mood>0.6 else "yellow" if ~numpy.isnan(mood) else str(numpy.nan)

    movement = json_data["result_histogram"]["total_hits"]
    movement_color = "green" if movement != 0 else 'red' 

    output["mood"] =  "{0:1.3f}".format(mood) if ~numpy.isnan(mood) else str(numpy.nan)
    output["mood_color"] = mood_color

    output["movement"] = str(movement)
    output["movement_color"] = movement_color
    output["status_code"] = json_data["status_code"]

  except:
    output['raw_json_data'] = json_data

    sentiment_results = ""
    total_hits = ""

    output["sentiment_results"] = sentiment_results
    output["hits"] =  str(total_hits)

    output["mood"] =  ""
    output["mood_color"] = ""

    output["movement"] = ""
    output["movement_color"] = ""
    output["status_code"] = json_data["status_code"]

  return output
  

schema = T.StructType([    
    T.StructField("sentiment_results", T.StringType(), True),
    T.StructField("hits", T.StringType(), True),
    T.StructField("status_code", T.StringType(), True),
    T.StructField("Date", T.DateType(), True),
    T.StructField("mood", T.StringType(), True),
    T.StructField("mood_color", T.StringType(), True),
    T.StructField("movement", T.StringType(), True),
    T.StructField("movement_color", T.StringType(), True)    
])

run_talkwalker_sentiment_endpoint_udf = F.udf(run_talkwalker_sentiment_endpoint, schema)

###########################################################################################

def build_url_instant_configured_with_age(topic,  topic_id, queryparam, age):
  """
  Build the corresponding queries for 3 sentiments in order to make a call to age endpoint.
  """
  
  topic = topic.strip()
  
  sentiment = ['positive', 'neutral', 'negative']
  sentiment_url = {}
  for sntmnt in sentiment:
    
    try:
      a = json.loads(queryparam)
      if topic_id:
        b = [" + ".join(["&q="] + [i for i in a[j].split(",")] + ["sentiment:"+ sntmnt ]) for j in range(len(a))] 
        b = list(set(b))  
        qq =  "&topic=" + topic_id + "".join(b)
      else:
        b = [" + ".join(["&q=" + topic] + [i for i in a[j].split(",") if 'sourcetype:SO' not in i and 'sourcetype:BRO' not in i and 'demographic:' not in i ] + ["sentiment:"+sntmnt]) for j in range(len(a))] 
        b = list(set(b))
        qq = "".join(b)

      url = url_base_configured + "age" + "?access_token=" + access_token + qq   # Both age endpoint, url_base_configured should be used in both instant and configured cases.
      
    except:
      if topic_id:
        url = url_base_configured + "age" + "?access_token=" + access_token + "&topic=" + topic_id
      else:
        url = url_base_configured + "age" + "?access_token=" + access_token + "&q=" + topic
        
    sentiment_url[sntmnt] = url
  
  return json.dumps(sentiment_url)
  

build_url_instant_configured_with_age_udf = F.udf(build_url_instant_configured_with_age)

#################################################################################################
df = config_from_db.filter(F.lower(F.col('search_type'))=='instant').filter(F.lower(F.col('active'))=='true')
df = df.withColumn("topic_id", GetTalkwalkerID_udf( df.topic)) # whether the topic has been configured or not
df = df.withColumn("age", get_age_queryjson_udf(df.queryjson))
df = df.filter(F.col('age') == '' )

df = df.withColumn("query_url", build_url_instant_no_age_udf(df.topic, df.queryparam))
df = df.withColumn("emotion", run_talkwalker_sentiment_endpoint_udf(df.query_url))
df = df.withColumn("Date", F.col('emotion.Date'))
df = df.withColumn("status_code", F.col('emotion.status_code'))
df = df.withColumn("sentiment_results", F.col('emotion.sentiment_results'))
df = df.withColumn("hits", F.col('emotion.hits'))
df = df.withColumn("mood", F.col('emotion.mood'))
df = df.withColumn("mood_color", F.col('emotion.mood_color'))
df = df.withColumn("movement", F.col('emotion.movement'))
df = df.withColumn("movement_color", F.col('emotion.movement_color'))
df = df.filter(F.col('status_code')=='0')

df_instant_no_age_group = df
display(df_instant_no_age_group)
#####################################################################################################

# str(uuid.uuid4())


# mySampleConfig = spark.createDataFrame(
#     [
#       (1, 'C8C75F98-7A48-414E-95C3-B6FCC470F475', 'customer_group', 'af8621af-3f03-4dea-bce6-0ddac03f8420', 'sentiment','renewable energy', '', 'configured', 'true', '["lang:en +  demographic:occupation-scientist"]'), # create your data here, be consistent in the types.
#       (2, '8A89E437-5C4A-4F39-94EC-3BF595A90013', 'customer_group', 'ww8621af-3f03-4dea-bce6-0ddac03f8416', 'sentiment','kake', '', 'configured', 'true', '["gender:female + sourcecountry:no"]'),
#       (3, 'E27CD849-2944-45B9-ACA0-BFFDC7F0AEC9', 'customer_group', 'ss8621af-3f03-4dea-bce6-0ddac03f8416', 'sentiment','bakeri', '', 'configured', 'true', '["sourcecountry:no"]'),
#       (4, '46F0281E-0EF1-49EA-8842-D139BB7C3764', 'customer_group', '77d92060-4bbf-422e-b221-54620be4215b', 'sentiment','Covid19', '', 'configured', 'true', '["demographic:occupation-blogger + lang:en","demographic:occupation-scientist"]'), 
#       (5, '56F0281E-0EE1-49EA-8842-D139AA7C3764', 'customer_group', '85d66b45-a6f1-4a3f-ab30-5fd421bff6fe', 'sentiment','Covid19', '', 'configured', 'true', '["sourcetype:SOCIALMEDIA + gender:female","demographic:occupation-scientist"]'),
#       (6, '4340C89D-35FB-4DA1-920A-CB351FFAB6C0', 'customer_group', '6da2b87e-bd24-4f20-8332-15eda6685586', 'sentiment','gender equality', '', 'configured', 'true', '["gender:female +  lang:en +  demographic:interest-advertising_marketing"]'),
#       (7, 'FCC8E7A0-8149-42F7-890E-BF1ADAAB34D9', 'customer_group', '99089188-a017-4539-babd-b802f5b94ca7', 'sentiment','netflix', '', 'instant', 'true', '["gender:female +  lang:en +  demographic:occupation-artist_art", "gender:male +  lang:en +  demographic:interest-advertising_marketing", "gender:male +  lang:en +  sourcetype:SOCIALMEDIA"]'),
#       (8, '9412056A-E90B-4E40-A39F-0259160458F4', 'customer_group', '975525bc-c320-4bb8-9d48-80f1fba97320', 'sentiment','coinbase', '', 'instant', 'true', '["sourcetype:ONLINENEWS +  lang:en","sourcetype:SOCIALMEDIA"]'),
#       (9, '9CBF7725-3759-4509-A6FA-81DA76FA888B', 'customer_group', '13aaa580-ed1e-4723-a777-483fcf2c4436', 'sentiment','spotify', '', 'instant', 'true', '["sourcecountry:us +  sourcetype:ONLINENEWS" , "gender:male +  lang:en "]'),
#       (10, 'D9D85F98-7B48-414E-95C3-B6FCC470F476', 'customer_group', 'af8621af-3f03-4dea-bce6-0ddac03f8420', 'sentiment','renewable energy', '{age:AGE-65}', 'configured', 'true', '["lang:en","sourcetype:SOCIALMEDIA + gender:female"]'),
#       (11, 'D9D85F98-7B48-414E-95C3-B6FCC470F476', 'customer_group', 'af8621af-3f03-4dea-bce6-0ddac03f8420', 'sentiment','trump', '{age:AGE-65}', 'configured', 'true', '["lang:en","sourcetype:SOCIALMEDIA + gender:female"]'),
        
#     ],
#     ['id', 'config_uuid', 'origin_type','origin_id' , 'query_type', 'topic', 'queryjson', 'search_type', 'active', 'queryparam' ] # add your columns label here
# )
# mySampleConfig = mySampleConfig.withColumn("id", mySampleConfig["id"].cast(T.IntegerType()))
# display(mySampleConfig)

############# mySampleConfig.write.mode("overwrite").format("jdbc").option("url", emotion_book_config['url']).option("dbtable", "insights_socialmedia_config").option("user", emotion_book_config['user']).option("password", emotion_book_config['password']).save()
############# drop('id')


########################################################################################################

