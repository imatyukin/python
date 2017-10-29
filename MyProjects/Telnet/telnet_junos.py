#!/usr/bin/env python3
import getpass
import telnetlib

print('''________________________________________________________________________________

        Warning : Authorized access only !!!
        Disconnect IMMEDIATELY if you are not an authorized person !!!

        You can be prosecuted for any other actions.
________________________________________________________________________________''')

user = input("login: ")
password = getpass.getpass()

with open('hosts') as devices:
    hosts = devices.read().split( )

with open('telnet.log', 'w') as log:
    for host in hosts:
        try:
            tn = telnetlib.Telnet(host, 23, 50)
        except:
            print('Connection failed', host)
            continue
        else:
            print('Connection successful', host)
            tn.read_until(b"login: ")
            tn.write(user.encode('ascii') + b"\n")
            if password:
                tn.read_until(b"Password: ")
                tn.write(password.encode('ascii') + b"\n")

            tn.write(b"show version | no-more\n")
            tn.write(b"exit\n")

            log.write(tn.read_all().decode('ascii'))

            tn.close()