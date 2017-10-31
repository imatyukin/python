#!/usr/bin/env python3
import sys

with open("ipv6_prefix_list", 'w') as pl:
    term = '''term prefixes {
    from {
'''
    pl.write(term)
    try:
        while True:
            data = sys.stdin.readline()
            rm_asterisk = data[2:]
            data_split = rm_asterisk.split()
            prefix = data_split[0]
            rf = '''        route-filter '''
            plength = ''' exact;
'''
            pl.write(rf+prefix+plength)
            if not data:
                break
    except KeyboardInterrupt:
        sys.stdout.flush()
    except IndexError:
        sys.stdout.flush()
    then = '''    }
    then next policy;
}
'''
    pl.write(then)

msg = '''IPv6 prefix-list:
-----------------'''
print('\n'+msg)
with open("ipv6_prefix_list") as pl:
    for line in pl:
        print(line, end='')