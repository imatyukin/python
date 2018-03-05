#!/usr/bin/env python3
# Find IPv4 address in non-contiguous IP-pools
import numpy as np


def main():
    # IPv4 address (IP)
    ip = '100.82.101.67'
    # Convert IP address to binary
    ip = ''.join([bin(int(x)+256)[3:] for x in ip.split('.')])
    ip_bin = np.fromstring(ip, 'u1') - ord('0')

    # Create dictionary { subnet : mask }
    with open('ip_pools') as f:
        ip_pool_dic = {}
        for line in f.read().split( ):
            line = str(line).split('/')
            key = line[0].strip()
            value = line[1].strip()
            if key in ip_pool_dic:
                ip_pool_dic[key].append(value)
            else:
                ip_pool_dic[key] = value

    for key, value in ip_pool_dic.items():
        # Convert Subnet and Mask to binary
        key = ''.join([bin(int(x)+256)[3:] for x in key.split('.')])
        key_bin = np.fromstring(key, 'u1') - ord('0')
        value = ''.join([bin(int(x) + 256)[3:] for x in value.split('.')])
        value_bin = np.fromstring(value, 'u1') - ord('0')

        if str(np.bitwise_and(ip_bin, value_bin)) == str(np.bitwise_and(key_bin, value_bin)):
            # Convert Subnet and Mask back to decimal
            key_bin = np.split(key_bin, 4)
            key_dec = np.packbits(key_bin)
            key = ".".join(str(x) for x in key_dec)
            value_bin = np.split(value_bin, 4)
            value_dec = np.packbits(value_bin)
            value = ".".join(str(x) for x in value_dec)
            print(key + '/' + value)


if __name__ == "__main__":
    main()
