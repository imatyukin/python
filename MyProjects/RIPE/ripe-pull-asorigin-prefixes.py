#!/usr/bin/python3
import urllib.request as urllib2
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# Variables which changes per request
as_to_pull_prefixes = "AS12389"
url = "http://rest.db.ripe.net/search.xml?query-string=%s&inverse-attribute=origin" % as_to_pull_prefixes

# Pull Info From IRR (RIPE) and assign it to a variable as string
fp = urllib2.urlopen(url)
response = fp.read()

# Parse xml from string into an element
tree = ET.fromstring(response)
fp.close()

# Get interested data from element
interested = tree.findall("./objects/object[@type='route']/primary-key/attribute[@name='route']")
for child in interested:
    print(child.get('value'))