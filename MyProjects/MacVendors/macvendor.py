#!/usr/bin/env python3
from urllib.request import urlopen

url = "http://api.macvendors.com/"
macOUI = input()
print(urlopen(url+macOUI).read().decode('ascii'))