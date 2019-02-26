#!/usr/bin/env python3

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *
from jinja2 import Template
import yaml

junos_hosts = [ '192.168.139.151', '192.168.139.152']
for host in junos_hosts:
    try:
        # Open and read the YAML file.
        with open(host + '.yml', 'r') as fh:
            data = yaml.load(fh.read())
        # Open and read the Jinja2 template file.
        with open('interface_routing_instance.j2', 'r') as t_fh:
            t_format = t_fh.read()
        # Associate the t_format variable with the jinja2 module
        template = Template(t_format)
        # Merge the data with the template
        myConfig = template.render(data)
        print("\nResults for device " + host)
        print("------------------------")
        print(myConfig)
        dev = Device(host=host, user='lab', password='lab123').open()
        config = Config(dev)
        config.lock()
        config.load(myConfig, merge=True, format="text")
        config.pdiff()
        config.commit()
        config.unlock()
        dev.close()
    except LockError as e:
        print("The config database was locked!")
    except ConnectTimeoutError as e:
        print("Connection timed out!")
