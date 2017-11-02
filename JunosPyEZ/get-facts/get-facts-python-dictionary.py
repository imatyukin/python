#!/usr/bin/env python3
import sys
from jnpr.junos import Device
from getpass import getpass
from jnpr.junos.exception import ConnectError

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

# NETCONF session over SSH
dev = Device(host=hostname, user=username, passwd=password)

try:
    dev.open()
except ConnectError as err:
    print ("Cannot connect to device: {0}".format(err))
    sys.exit(1)

print (dev.facts)
dev.close()