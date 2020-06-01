# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 22:11:46 2020

@author: MajidKhoshrou
"""
# https://docs.microsoft.com/en-us/azure/event-hubs/get-started-capture-python-v2
# https://docs.microsoft.com/en-us/azure/event-hubs/get-started-capture-python-v2


import time
import os
import uuid
import datetime
import random
import json

from azure.eventhub import EventHubProducerClient
from azure.eventhub import EventHubProducerClient, EventData

# this scripts simulates production of events for 10 devices
devices = []
for x in range(0, 10):
    devices.append(str(uuid.uuid4()))

# create a producer client to produce/publish events to the event hub
producer = EventHubProducerClient.from_connection_string(conn_str="Endpoint=sb://mbv-eventhubs.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=7TWgtybwLH5o31m8+Abhc8EbMU0CH+wbNRtJuylkkXI=", eventhub_name="myeventhub01")


for y in range(0,20):    # for each device, produce 20 events 
    event_data_batch = producer.create_batch() # create a batch. you will add events to the batch later. 
    for dev in devices:
        # create a dummy reading
        reading = {'id': dev, 'timestamp': str(datetime.datetime.utcnow()), 'uv': random.random(), 'temperature': random.randint(70, 100), 'humidity': random.randint(70, 100)}
        s = json.dumps(reading) # convert reading into a JSON string
        event_data_batch.add(EventData(s)) # add event data to the batch
    producer.send_batch(event_data_batch) # send the batch of events to the event hub

# close the producer    
producer.close()



