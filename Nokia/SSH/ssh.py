#!/usr/bin/env python

# This program logs into all our lab nodes and collects 'show version'
# At the end it prints the name and the current running version of each router
# It does it using 'getpass' so the password is prompted for but not echo'd to the screen

import paramiko
import time
import re
import getpass

username = input("Enter your username : ")
password = getpass.getpass("Enter your password : ")


def open_ssh_connection(ip):
    """
    This function logs into a node using SSH
    Then issues fixed value commands
    Then returns the full output and converts it from a bytes object into a string
    If authentication fails then it prints a custom message
    """
    try:
        # Define the command to collect
        command = "show version"

        # Logging into the device
        session = paramiko.SSHClient()

        # This is recommended for testing only. If the key is not found
        # then it is auto added.
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the device using the default username and password
        session.connect(ip, username=username, password=password)

        # Start an interactive shell
        connection = session.invoke_shell()

        # Disable pagination then sleep for a second
        connection.send("environment no more\n")
        time.sleep(0.5)

        # Collect the command, press enter and sleep for 2 seconds
        connection.send(command)
        connection.send("\n")
        time.sleep(0.5)

        # Make a variable with the entire session output (up to 65535)
        router_output = connection.recv(65535)

        # Close our session
        connection.close()

        # Print the output and convert it from a bytes object to a string object
        return (router_output.decode("utf-8"))

    except paramiko.AuthenticationException:
        print("###### Invalid Username or Password ######")


all_lab_routers = ["135.221.38.101",
                   "135.221.38.102",
                   "135.221.38.103",
                   "135.221.38.104",
                   "135.221.38.105",
                   "135.221.38.107",
                   "135.221.38.108",
                   "135.221.38.109",
                   "135.221.38.110",
                   "135.221.38.111",
                   "135.221.38.112",
                   "135.221.38.113",
                   "135.221.38.114",
                   "135.221.38.115",
                   "135.221.38.116",
                   "135.221.38.117",
                   "135.221.38.118",
                   "135.221.38.119"]

for router in all_lab_routers:
    output = open_ssh_connection(router)
    name = re.findall(r".*[A|B]:(\S+)#.*", output, re.S)[0]
    version = re.findall(r".*TiMOS-[C|B]-(\S+).*", output, re.S)[0]
    print("Router " + name + " is running version " + version)
