#!/usr/bin/python
# -*- coding: utf-8 -*-

""" MTU killer

What does it do?

    1. Enumerates all interfaces, skips lo and loops over them.
    2. Gets MTU for interface.
    3. Read all IP addresses from ARP table, we assuming these hosts are
       available and should respond on ICMP req.
    4. Ping host from ARP table over specific interface with "small ping"
       64 bytes.
    5. Ping host from ARP table over specific interface with "big ping",
       which is equal to MTU of interface.

If ping fails, it prints exact command which can be used to re-test.

"""

from __future__ import print_function

import logging
import netifaces
import socket
import struct
import subprocess

from collections import defaultdict
from fcntl import ioctl


SIOCGIFMTU = 0x8921
SIOCSIFMTU = 0x8922

log = logging.getLogger(__name__)

""" TODO:
    - install arp_table and use it in read_arp_table()
    - install ifcfg to validate MTU settings on interfaces in in config files
"""


def read_arp_table():
    arp_table = defaultdict(set)
    arp_file_raw = open('/proc/net/arp', 'r').readlines()[1:]
    for arp_entry in arp_file_raw:
            arp_table[arp_entry.split()[5]].add(arp_entry.split()[0])
    return arp_table


class interface(object):
    def __init__(self, interface):
        self.interface = interface
        self.arp_table = read_arp_table()
        self.mtu = self.get_mtu()

    def get_mtu(self):
        """Use socket ioctl call to get MTU size"""
        s = socket.socket(type=socket.SOCK_DGRAM)
        ifr = self.interface + '\x00'*(32-len(self.interface))
        try:
            ifs = ioctl(s, SIOCGIFMTU, ifr)
            mtu = struct.unpack('<H', ifs[16:18])[0]
        except Exception, s:
            log.critical('socket ioctl call failed: {0}'.format(s))
            raise

        log.debug('get_mtu: mtu of {0} = {1}'.format(self.interface, mtu))
        return mtu

    def ping(self, host, ping_size, count=10, timeout=0.2):
        # (20 for the IP header) + (8 for the ICMP header)
        _header_size = 28
        mtu = ping_size - _header_size
        ping_cmd = "ping  -A -w 4 -W {} -i {} -c {} -s {} {}".format(
                timeout, timeout, count, mtu, host)
        # import pdb; pdb.set_trace()
        proc = subprocess.Popen(ping_cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                shell=True,
                                close_fds=True)
        (out, err) = proc.communicate()
        return (proc.returncode, out, err, ping_cmd)

    def check_link(self, ifce_name, target, ping_size):
        small_ping = 64
        # import pdb; pdb.set_trace()
        try:
            # import pdb; pdb.set_trace()
            print("Cheking link {} to {} with {} bytes -> link ".\
                  format(ifce_name, target, small_ping), end=' ')
            (returncode, out, err, ping_cmd) = self.ping(target, small_ping)
            if returncode != 0:
                print("FAILED! CMD: {}".format(ping_cmd))
                return False
            else:
                print("OK")

            print("Cheking link {} to {} with {} bytes -> link ".\
                  format(ifce_name, target, ping_size), end=' ')
            (returncode, out, err, ping_cmd) = self.ping(target, ping_size)
            if returncode != 0:
                print("FAILED! CMD: {}".format(ping_cmd))
                return False
            else:
                print("OK")
            return True
        except KeyboardInterrupt as kex:
            print("Skipping {} cmd: {}".format(target, ping_cmd))
        return False


def main():
    read_arp_table()
    for ifce_name in netifaces.interfaces():
        """ Ignore some of the interfaces """
        ifc = interface(ifce_name)
        if ifce_name in ['lo'] or ifc.arp_table.get(ifce_name) is None:
            continue
        print("Interface: {} MTU: {} neighbors: {}".format(
            ifce_name,
            ifc.mtu,
            ifc.arp_table.get(ifce_name)))
        for target in ifc.arp_table.get(ifce_name):
            ifc.check_link(ifce_name, target, ifc.mtu)


if __name__ == '__main__':
    main()
