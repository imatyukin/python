#!/usr/bin/env python3
import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.utils.scp import SCP

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

with SCP(dev) as scp:
    scp.get('/var/log/messages', './messages')

dev.close()