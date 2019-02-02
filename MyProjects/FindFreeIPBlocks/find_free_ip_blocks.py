#!/usr/bin/env python3

"""
Find free IP blocks.
"""

import argparse
import math
import sys
import struct
from re import match, compile, findall
from socket import inet_aton, inet_ntoa
import getpass
import telnetlib
import codecs


class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # The output to be visible immediately

    def flush(self):
        for f in self.files:
            f.flush()


def cidr_to_range(cidr, descr=None):
        """
        cidr_to_range return a tuple countaining the lower and upper bound of a
        CIDR block as 32bit integers.
        """

        addr_str, mask_str = cidr.split('/')
        addr = struct.unpack("!I", inet_aton(addr_str))[0]
        mask = int(mask_str)
        return (addr, addr + 2 ** (32 - mask) - 1, descr)


def range_to_info(cidr, compute_best=False):
        """
        range_to_info converts a tuple containing the integral lower and upper
        bound of a CIDR block into a tuple containing printable IP information.
        """

        min_addr = inet_ntoa(struct.pack("!I", cidr[0]))
        max_addr = inet_ntoa(struct.pack("!I", cidr[1]))
        size = cidr[1] - cidr[0] + 1

        mask_str = ''
        best_str = ''
        mask = 32 - int(math.log(cidr[1] - cidr[0] + 1, 2))
        snmask = 0xFFFFFFFF ^ (1 << 32 - mask) - 1
        n_addr = cidr[0] & snmask
        if cidr[0] == n_addr:
            if compute_best:
                best_str = '{}/{}'.format(min_addr, mask)

            bcast = cidr[0] | (0xFFFFFFFF ^ snmask)
            if cidr[1] == bcast:
                mask_str = '/{}'.format(mask)

        elif compute_best:
            # increment network by 1
            n_addr += 2 ** (32 - mask)
            mask = 32 - int(math.log(cidr[1] - n_addr + 1, 2))
            best_str = '{}/{}'.format(inet_ntoa(struct.pack("!I", n_addr)), mask)

        return (min_addr, max_addr, mask_str, size, best_str)


def is_overlap(parent, child):
        """
        is_overlap returns True if the child IP range overlaps the parent in any way.
        """

        if child[0] >= parent[0] and child[0] <= parent[1]:
            return True
        if child[1] >= parent[0] and child[1] <= parent[1]:
            return True
        return False


def get_free(parent, taken):
        """
        get_free returns an array of tuples containing all taken and free IP blocks
        for the given parent IP range.
        """

        if not taken:
            return [(parent[0], parent[1], 'FREE')]

        taken.sort(key=lambda tup: tup[0])
        blocks = []

        first = True
        all_free = True
        for i in range(0, len(taken)):
            block = taken[i]
            if is_overlap(parent, block):
                all_free = False
                if first:
                    if block[0] > parent[0]:
                        blocks.append((parent[0], block[0] - 1, 'FREE'))
                    first = False

                blocks.append(block)

                if i < len(taken) - 1:
                    upper = min(parent[1], taken[i + 1][0] - 1)
                else:
                    upper = parent[1]

                if block[1] < upper:
                    blocks.append((block[1] + 1, upper, 'FREE'))

        if all_free:
            blocks.append((parent[0], parent[1], 'FREE'))

        return blocks


def print_table(data, headers=None, colored=False):
        """
        print_table prints the given dataset as a formatted table.
        """

        first_column = 0
        if colored:
            first_column = 1
        columns = [0]

        def print_row(row):
            """
            print_row prints a single row in a dataset.
            """

            sys.stdout.write('\x1b[{}m'.format(row[0]))
            for i in range(1, len(row)):
                if i > 1:
                    sys.stdout.write(' ')
                sys.stdout.write('%-*s' % (columns[i], row[i]))
            sys.stdout.write('\x1b[0m\n')

        if headers:
            for i in range(0, len(headers)):
                columns.append(len(headers[i]))
            if colored:
                headers.insert(0, '')

        for row in data:
            for i in range(first_column, len(row)):
                while len(columns) < len(row):
                    columns.append(0)
                width = len(str(row[i]))
                if columns[i] < width:
                    columns[i] = width

        if headers:
            print_row(headers)

        for row in data:
            print_row(row)

        sys.stdout.flush()


def print_blocks(blocks):
        """
        print_blocks prints a list of IP blocks in colored, tabular format.
        """

        data = []
        for block in blocks:
            compute_best = False
            color = 90  # dark gray
            if block[2] == 'FREE':
                compute_best = True
                color = 32  # green
            iprange = range_to_info(block, compute_best)
            data.append((color, iprange[0], iprange[1], iprange[2], iprange[3], iprange[4], block[2]))

        print_table(data,
                    headers=['MIN IP', 'MAX IP', 'MASK', 'SIZE', 'BEST', 'LABEL'],
                    colored=True)


def telnet(cidr):

        user = input("login: ")
        password = getpass.getpass()
        host = '212.48.198.56'

        with open('telnet.log', 'w') as log:
            try:
                tn = telnetlib.Telnet(host, 23, 50)
            except:
                print('Connection failed', host)
            else:
                print('Connection successful', host)
                tn.read_until(b"login: ")
                tn.write(user.encode('ascii') + b"\n")
                if password:
                    tn.read_until(b"Password: ")
                    tn.write(password.encode('ascii') + b"\n")

                cmd = 'show route ' + cidr + ' terse table inet.0 | match "[0-9\.]+/[0-9]" | no-more' + '\n'
                tn.write(cmd.encode())
                tn.write(b"exit\n")

                log.write(tn.read_all().decode('ascii'))

                tn.close()


def do_cidr(cidr):
        """
        do_cidr find and prints free ip blocks in a CIDR block.
        """

        # telnet(cidr)
        cidr_r = cidr_to_range(cidr)
        subnets = []

        prefex_regex = compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        log = codecs.open('telnet.log', 'r', encoding='utf-8', errors='ignore').read()
        log_line = log.splitlines()
        for line in log_line:
            if findall(prefex_regex, line):
                subnets.extend(([fields.split()[2] for fields in line.splitlines()]))

        taken = []
        for subnet in subnets:
            subnet_r = cidr_to_range(subnet, None)
            taken.append(subnet_r)

        print_blocks(get_free(cidr_r, taken))


def main():
        """
        main executes the main thread
        """

        parser = argparse.ArgumentParser(
            description='Find free IP blocks.')

        parser.add_argument('target',
                            metavar='TARGET',
                            help='CIDR to search')

        args = parser.parse_args()

        if match(r"^[0-9\.]+/[0-9]+$", args.target):
            do_cidr(args.target)


if __name__ == '__main__':
    main()
