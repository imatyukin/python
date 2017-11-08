#!/usr/bin/env python3
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell

hostname = input("Device hostname: ")
username = input("Device username: ")
password = getpass("Device password: ")

# NETCONF session over SSH
dev = Device(host=hostname, user=username, passwd=password)
dev.open()

with StartShell(dev, timeout=60) as ss:
    ss.run('cli -c "request support information | no-more | save /var/tmp/information.txt"')
    version = ss.run('cli -c "show version | no-more"')
    print (version)

dev.close()