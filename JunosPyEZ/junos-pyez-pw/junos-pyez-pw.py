#!/usr/bin/env python3
from jnpr.junos import Device
from getpass import getpass
import sys

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

# NETCONF session over SSH
#dev = Device(host=hostname, user=username, passwd=password)

# Telnet connection
dev = Device(host=hostname, user=username, passwd=password, mode='telnet', port='23')

# Serial console connection
#dev = Device(host=hostname, user=username, passwd=password, mode='serial', port='/dev/ttyUSB0')

try:
    dev.open()
except Exception as err:
    print (err)
    sys.exit(1)

print (dev.facts)
dev.close()