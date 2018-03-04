#!/usr/bin/env python3
# RFC 950
# Calculate:
# Network-ID address (First IPv4 address)
# Broadcast address (Last IPv4 address)
import numpy as np


def main():
    # IPv4 address (IP)
    ip = '192.1.127.50'
    print('IPv4 address:', ip)
    # Non-contiguous subnet mask (SM)
    sm = '255.255.255.88'
    print('Non-contiguous subnet mask:', sm)

    # Convert IP address and Subnet Mask to binary
    ip_bin_str = ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    ip_bin = np.fromstring(ip_bin_str, 'u1') - ord('0')
    sm_bin_str = ''.join([bin(int(x)+256)[3:] for x in sm.split('.')])
    sm_bin = np.fromstring(sm_bin_str, 'u1') - ord('0')

    # Network ID address (NET_ID)
    # bitwise AND (between IP and SM)
    net_id_bin = np.bitwise_and(ip_bin, sm_bin)

    # convert NET_ID back to decimal
    net_id_bin_split = np.split(net_id_bin, 4)
    net_id_dec = np.packbits(net_id_bin_split)
    net_id = ".".join(str(x) for x in net_id_dec)
    print('NET-ID:', net_id)

    # Broadcast address (BA)
    # bitwise XOR (between Network ID address and the inverse subnet mask (ISM)
    ism = (~sm_bin.astype(bool)).astype(int)
    ba_bin = np.bitwise_xor(net_id_bin, ism)

    # convert BA back to decimal
    ba_bin_split = np.split(ba_bin, 4)
    ba_dec = np.packbits(ba_bin_split)
    ba = ".".join(str(x) for x in ba_dec)
    print('Broadcast address:', ba)


if __name__ == "__main__":
    main()
