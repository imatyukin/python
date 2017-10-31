#!/usr/bin/env python3
import sys

with open("ipv6_prefix_list", 'w') as pl:
    msg_begin = '''term prefixes {
    from {
'''
    pl.write(msg_begin)
    try:
        while True:
            data = sys.stdin.readline()
            rm_asterisk = data[2:]
            data_split = rm_asterisk.split()
            prefix = data_split[0]
            msg1 = '''        route-filter '''
            msg2 = ''' exact;
'''
            pl.write(msg1+prefix+msg2)
            if not data:
                break
    except KeyboardInterrupt:
        sys.stdout.flush()
    except IndexError:
        sys.stdout.flush()
    msg_end = '''    }
    then next policy;
}
'''
    pl.write(msg_end)

msg_stdout = '''Prefix-list.out:
----------------'''
print(msg_stdout)
with open("ipv6_prefix_list") as pl:
    for line in pl:
        print(line, end='')