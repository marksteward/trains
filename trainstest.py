#!/usr/bin/env python

from stompy.simple import Client
import ConfigParser
import sys
import json
import pprint

config = ConfigParser.ConfigParser()
config.read('trains.conf')

topics = {
  'tm': 'TRAIN_MVT_ALL_TOC',
  'td': 'TD_ALL_SIG_AREA',
  'vstp': 'VSTP_ALL',
  'rtppm': 'RTPPM_ALL',
  'tsr': 'TSR_ALL_ROUTE',
}

feedname = sys.argv[1].lower()
if feedname not in topics:
  print 'Valid feeds:'
  print '\n'.join(topics.keys())

dest = '/topic/%s' % topics[feedname]
feed = Client(host='datafeeds.networkrail.co.uk', port=61618)

feed.connect(config.get('user', 'email'), config.get('user', 'password'))
feed.subscribe(dest)
print 'Subscribed'

while True:
  message = feed.get()
  print message
  data = json.loads(message.body)
  pprint.pprint(data)

feed.unsubscribe(dest)
feed.disconnect()
