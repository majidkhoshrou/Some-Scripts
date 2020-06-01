# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 16:50:46 2020

@author: MajidKhoshrou
"""

import sys
import logging
import datetime
import time
import os

from azure.eventhub import EventData
#from azure.eventhub import Sender
from azure.eventhub import EventHubClient
 


logger = logging.getLogger("azure")

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<namespace>.servicebus.windows.net/eventhub"
# "amqps://<namespace>.servicebus.windows.net/<eventhub>"
# SAS policy and key are not required if they are encoded in the URL

ADDRESS = "amqps://<mbv-eventhubs>.servicebus.windows.net/myeventhub01"
USER = "RootManageSharedAccessKey"
KEY = "7TWgtybwLH5o31m8+Abhc8EbMU0CH+wbNRtJuylkkXI="

try:
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")

    # Create Event Hubs client
    client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
    sender = client.add_sender(partition="0")
    client.run()
    try:
        start_time = time.time()
        for i in range(100):
            print("Sending message: {}".format(i))
            message = "Message {}".format(i)
            sender.send(EventData(message))
    except:
        raise
    finally:
        end_time = time.time()
        client.stop()
        run_time = end_time - start_time
        logger.info("Runtime: {} seconds".format(run_time))

except KeyboardInterrupt:
    pass


















