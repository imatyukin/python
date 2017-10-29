#!/usr/bin/env python3
import os
# package: dnspython
import dns.resolver

with open('hostnames') as hostnames:
    hostname = hostnames.read().split( )

def query(hosts_list=hostname):
    collection = []
    for host in hosts_list:
        ip = dns.resolver.query(host, "A")
        for i in ip:
            collection.append(str(i))
    return collection

with open('ip.tmp', 'w') as ip_tmp:
    for arec in query():
        ip_tmp.write(arec+'\n')

with open('ip.tmp') as ip_tmp:
    ip = ip_tmp.read().split()

with open('ip-addresses', 'w') as ip_addresses:
    for ip_tmp, hostnames in zip(ip, hostname):
        print(ip_tmp, hostnames, file=ip_addresses)

with open('ip-addresses') as ip_addresses:
    print(ip_addresses.read())

os.remove("ip.tmp")