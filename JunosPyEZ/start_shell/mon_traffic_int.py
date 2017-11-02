#!/usr/bin/env python3
from jnpr.junos import Device
from getpass import getpass
from jnpr.junos.utils.start_shell import StartShell

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

# NETCONF session over SSH
dev = Device(host=hostname, user=username, passwd=password)
dev.open()

with StartShell(dev) as ss:
    print(ss.run('cli -c "monitor traffic interface ae0"', this=None, timeout=15))

dev.close()