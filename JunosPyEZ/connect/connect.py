#!/usr/bin/env python3
import sys
from getpass import getpass
from jnpr.junos import Device

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

# NETCONF session over SSH
dev = Device(host=hostname, user=username, passwd=password)
try:
    dev.open()
except Exception as err:
    print (err)
    sys.exit(1)

print (dev.connected)
dev.close()

print (dev.connected)