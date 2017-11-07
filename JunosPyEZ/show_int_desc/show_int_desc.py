#!/usr/bin/env python3
""" Gather interface description """
import sys
from getpass import getpass

from jnpr.junos import Device
import jnpr.junos.exception

# package: jxmlease
import jxmlease

# Create a jxmlease parser with desired defaults.
parser = jxmlease.EtreeParser()

class DoneWithDevice(Exception): pass

def main():
    """ The main loop.
    Prompt for a username and password.
    Loop over each device specified on the command line.
    Perform the following step on each device:
    Get interface descriptions from the device configuration.

    Return an integer suitable for passing to sys.exit(). """

    if len(sys.argv) == 1:
        print("\nUsage: %s device1 [device2 [...]]\n\n" % sys.argv[0])
        return 1

    rc = 0

    # Get username and password as user input.
    username = input("Device username: ")
    password = getpass("Device password: ")

    for hostname in sys.argv[1:]:
        try:
            print("Connecting to %s..." % hostname)

            # Telnet connection
            dev = Device(host=hostname,
                         user=username,
                         passwd=password,
                         mode='telnet',
                         port='23')
            dev.open()

            print("Getting interface descriptions from %s...\n" % hostname)
            desc_info = get_description_info_for_interfaces(device=dev)
            if desc_info == None:
                print("Error retrieving interface descriptions on %s." %
                      hostname)
                rc = 1
                raise DoneWithDevice
            print(''.join('{} {}\n'.format(key, val) for key, val in desc_info.items()))

        except jnpr.junos.exception.ConnectError as err:
            print("Error connecting: " + repr(err))
            rc = 1
        except DoneWithDevice:
            pass
        finally:
            print("Closing connection to %s.\n" % hostname)
            try:
                dev.close()
            except:
                pass
    return rc

def get_description_info_for_interfaces(device):
    """ Get current interface description for each interface.
    Return a dictionary. The key is the local port (aka interface)
    name. The value is the user-configured description.
    On error, return None. """

    desc_info = {}

    try:
        resp = parser(device.rpc.get_interface_information(descriptions=True))
    except (jnpr.junos.exception.RpcError,
            jnpr.junos.exception.ConnectError) as err:
        print (repr(err))
        return None

    try:
        pi = resp['interface-information']['physical-interface'].jdict()
    except KeyError:
        return desc_info

    for (local_port, port_info) in pi.items():
        try:
            (udesc, _, ldesc) = port_info['description'].partition(':')
            udesc = udesc.rstrip()
            desc_info[local_port] = udesc
        except (KeyError, TypeError):
            pass
    return desc_info

if __name__ == "__main__":
  sys.exit(main())