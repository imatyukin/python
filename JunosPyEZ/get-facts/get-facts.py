#!/usr/bin/env python3
from jnpr.junos import Device
from getpass import getpass
from pprint import pprint
import sys

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

try:
   # NETCONF session over SSH
   with Device(host=hostname, user=username, passwd=password) as dev:
       pprint (dev.facts)
except Exception as err:
    print (err)
    sys.exit(1)