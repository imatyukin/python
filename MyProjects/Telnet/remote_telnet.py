#!/usr/bin/env python3
import getpass
import telnetlib

print('''________________________________________________________________________________

        Warning : Authorized access only !!!
        Disconnect IMMEDIATELY if you are not an authorized person !!!

        You can be prosecuted for any other actions.
________________________________________________________________________________''')

terminal = 'XXX.XXX.XXX.XXX'
user = input('Enter your remote account: ')
password = getpass.getpass()

with open('hosts') as devices:
    hosts = devices.read().split( )

try:
    tn = telnetlib.Telnet(terminal, 23, 50)
    tn.set_debuglevel(1)
except:
    print('Connection failed', terminal)
    exit(0)
else:
    print('Connection successful', terminal)
    tn.read_until(b'login: ')
    tn.write(user.encode('ascii') + b'\n')
    if password:
        tn.read_until(b'Password: ')
        tn.write(password.encode('ascii') + b'\n')

    for host in hosts:
        cmd = 'telnet routing-instance ri-is-l3vpn-dslam-ctrl ' + host + '\n'
        tn.write(cmd.encode())
        try:
            tn.read_until(b'login: ')
            login = user + '\n'
            tn.write(login.encode())
            tn.read_until(b'Password: ')
            passwd = password + '\n'
            tn.write(passwd.encode())
            with open('telnet.log', 'a') as log:
                log.write('\nIP-address: ' + str(host) + '\n')
                tn.read_until(b'> ')
                tn.write(b'show version | no-more\n')
                output = tn.read_until(b'> ')
                print(output.decode('ascii'))
                log.write(output.decode('ascii'))
                tn.write(b"exit\n")
                tn.read_until(b'> ')
        except:
            continue
    tn.write(b"exit\n")
    tn.close()
