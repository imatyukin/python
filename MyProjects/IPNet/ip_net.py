#!/usr/bin/env python3
""" python3 ip_net.py 192.168.0.0/24 27 """

from netaddr import *
from pprint import pprint
from sys import argv

net = argv[1]
split_mask = int(argv[2])


def calc_net(net, split_mask):
    num = 0
    ip = IPNetwork(net)
    subnets = list(ip.subnet(split_mask))
    for l in subnets:
        k = str(l)
        print(k)
        num += k.count('/')
    print('Total are ', num, ' subnets')


if __name__ == "__main__":
    calc_net(net, split_mask)