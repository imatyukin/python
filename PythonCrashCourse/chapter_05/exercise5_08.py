#!/usr/bin/env python3

usernames = ['root', 'admin', 'master', 'igor', 'tanya']

for user in usernames:
    if (user == 'admin'):
        print ("Hello admin, would you like to see a status report?")
    else:
        print ("Hello " + user + ", thank you for logging in again.")
