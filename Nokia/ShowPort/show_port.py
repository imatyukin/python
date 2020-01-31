#!/usr/bin/env python

from datetime import datetime
from netmiko import ConnectHandler
from my_devices import sr_sros


def check_port(net_connect, cmd='show port'):
    output = net_connect.send_command_expect(cmd)
    print output

def main():
    device_list = [sr_sros]
    start_time = datetime.now()
    print

    for a_device in device_list:
        net_connect = ConnectHandler(**a_device)
#        net_connect.enable()
        print "{}: {}".format(net_connect.device_type, net_connect.find_prompt())
        check_port(net_connect)
    
    print "Time elapsed: {}\n".format(datetime.now() - start_time)


if __name__ == "__main__":
	main()
