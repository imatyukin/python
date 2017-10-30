#!/usr/bin/env python3
import sys, os

# package: dnspython
import dns.resolver

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # The output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

with open('hostnames') as host_names:
    hostname = host_names.read().split( )

def query(hosts_list=hostname):
    collection = []
    for host in hosts_list:
        ip = dns.resolver.query(host, "A")
        for i in ip:
            collection.append(str(i) + '    ' + host)
    return collection

with open('ip-addresses', 'w') as ip_addresses:
    original = sys.stdout
    sys.stdout = Tee(sys.stdout, ip_addresses)
    for arec in query():
        print(arec)
    sys.stdout = original