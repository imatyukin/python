#!/usr/bin/env python3

import getpass
import pexpect
import sys

print('''-----===== Juniper E320 =====-----''')

fclear = open('telnet.log', 'w')
fclear.close()

user = 'usr'
password = getpass.getpass()

enable_spb = 'passwd1'
enable_arkh_murm = 'passwd2'
enable_novg = 'passwd3'
enable_pskv_vlgd = 'passwd4'
enable_klnd = 'passwd5'
enable_ptzk = 'passwd6'
enable_sykt = 'passwd7'

fhosts = open("hosts", 'r')
hosts = fhosts.read().split()

for h in hosts:
    print(h)
    tn = pexpect.spawn('telnet %s' % (h))
    fout = open('telnet.out', 'ab')
    tn.logfile_read = fout

    try:
        i = tn.expect([pexpect.TIMEOUT, 'Username:'])
        if i == 0:  # Timeout
            print('ERROR!')
            print('Telnet could not login. Here is what telnet said:')
            print(tn.before, tn.after)
            sys.exit(1)

        tn.sendline(user)
        tn.expect(['Password:'])
        tn.sendline(password)

        e = tn.expect(
            ['210>', '233>', '273>', '343>', '388>', '543>', '588>', '705>', '712>', '742>', 'MMT>', 'ARKH>', 'NMAR>',
             'SVDV>', 'NOVG>', 'BOROV>', 'PSKV>', 'CHER>', 'VLGD>', 'CHERN>', 'SOVET>', 'KLGD>', 'PTZK>', 'SYKT>',
             'UHTA>', 'VORK>', 'KOLA>', 'MONC>', 'MURM>'])
        if e in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
            tn.sendline('enable')
            tn.expect('Password:')
            tn.sendline(enable_spb)
        elif e in (11, 12, 13, 26, 27, 28):
            tn.sendline('enable')
            tn.expect('Password:')
            tn.sendline(enable_arkh_murm)
        elif e in (14, 15):
            tn.sendline('enable')
            tn.expect('Password:')
            tn.sendline(enable_novg)
        elif e in (16, 17, 18):
            tn.sendline('enable')
            tn.expect('Password:')
            tn.sendline(enable_pskv_vlgd)
        elif e in (19, 20, 21):
            tn.sendline('enable')
            tn.expect('Password:')
            tn.sendline(enable_klnd)
        elif e == 22:
            tn.sendline('enable')
            tn.expect('Password:')
            tn.sendline(enable_ptzk)
        elif e in (23, 24, 25):
            tn.sendline('enable')
            tn.expect('Password:')
            tn.sendline(enable_sykt)

        tn.expect('#')
        tn.sendline('terminal length 0')
        tn.expect('#')
        tn.sendline('terminal width 512')

        tn.expect('#')
        tn.sendline('show ip local pool')
        tn.expect('#')
        tn.sendline('exit')
        print(tn.before.decode('UTF-8'))
        # tn.interact()

    except:
        print("Error")