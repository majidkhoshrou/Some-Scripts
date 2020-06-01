# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:02:35 2019

@author: MajidKhoshrou
"""

import time, uuid, urllib, json
import hmac, hashlib
from base64 import b64encode

app_id = '498DnA3e'
consumer_key = 'dj0yJmk9Yzh6T3M5RnJSdTc5JmQ9WVdrOU5EazRSRzVCTTJVbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmc3Y9MCZ4PTJi'
consumer_secret = '746b1f63d69deaf121b4f72e2bf30bb988fbe776'

query = {'location': 'Rotterdam', 'format': 'json', 'u': 'c'}

url = 'https://weather-ydn-yql.media.yahoo.com/forecastrss'
method = 'GET'

concat = '&'

oauth = {
'oauth_consumer_key': consumer_key,
'oauth_nonce': uuid.uuid4().hex,
'oauth_signature_method': 'HMAC-SHA1',
'oauth_timestamp': str(int(time.time())),
'oauth_version': '1.0'
}

merged_params = query.copy()
merged_params.update(oauth)
sorted_params = [ k + '=' + urllib.parse.quote(merged_params[k], safe='') for k in sorted(merged_params.keys()) ]
signature_base_str = method + concat + urllib.parse.quote(url, safe='') + concat + urllib.parse.quote(concat.join(sorted_params), safe='')


composite_key = urllib.parse.quote(consumer_secret, safe='') + concat
oauth_signature = b64encode(hmac.new(composite_key.encode('utf-8'), signature_base_str.encode('utf-8'), hashlib.sha1).digest())

oauth['oauth_signature'] = oauth_signature.decode('utf-8')
auth_header = 'OAuth ' + ', '.join(['{}="{}"'.format(k,v) for k,v in oauth.items()])

url = url + '?' + urllib.parse.urlencode(query)

request = urllib.request.Request(url)
request.headers['Authorization'] = auth_header
request.headers['X-Yahoo-App-Id']= app_id

response = urllib.request.urlopen(request).read()
print(json.loads(response))


bag = {"a": 2, "b": {"c":{"d":6}}}
bag["b"]["c"]["d"]

movement=.5
mood_color= "red" if movement<0.4 else "green" if movement>.6 else "yellow"
mood_color
















































