#!/usr/bin/env python3
import sys
from jnpr.junos import Device
from getpass import getpass
from jnpr.junos.factory import loadyaml

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

yml_file = "stp.yml"
globals().update(loadyaml(yml_file))

# Telnet connection
dev = Device(host=hostname, user=username, passwd=password, mode='telnet', port='23')

try:
    dev.open()
except Exception as err:
    print (err)
    sys.exit(1)

tbl = STPInterfaces(dev)
tbl.get()
for key in tbl:
    print (key.name, key.role, key.state)

dev.close()