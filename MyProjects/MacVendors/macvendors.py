#!/usr/bin/env python3
import urllib.request as urllib2
import json
import codecs

# API base url
url = "http://macvendors.co/api/"

# Mac address to lookup vendor from
print("Mac address: ", end='')
mac_address = input()

request = urllib2.Request(url + mac_address, headers={'User-Agent' : "API Browser"})
response = urllib2.urlopen(request)

# Fix: json object must be str, not 'bytes'
reader = codecs.getreader("utf-8")
obj = json.load(reader(response))

# Print company name
print("Company Name: " + obj['result']['company']);

# Print company address
print("Address: " + obj['result']['address']);