#!/usr/bin/env python3

import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
import xlsxwriter

username = input("Device username: ")
password = getpass("Device password: ")

hosts = ["XXX.XXX.XXX.XXX", "YYY.YYY.YYY.YYY"]

inventory = {}

# Telnet connection
for host in hosts:
    dev = Device(host=host, user=username, passwd=password, mode='telnet', port='23')

    try:
        dev.open()
        print("Connected to " + host)
    except:
        print("Connection failed.")
        sys.exit(1)

    yml_file = "jinventory.yml"
    globals().update(loadyaml(yml_file))

    tbl = JModuleTable(dev).get()
    for item in tbl:
        # print("%s\t%s" % (item.type, item.mn))
        if not item.mn in inventory:
            if item.mn is not None:
                count = 1
                inventory.setdefault(item.mn, []).append(item.type)
                inventory[item.mn].append(count)
        else:
            if item.mn is not None:
                count = inventory[item.mn][-1]
                count += 1
                del inventory[item.mn][:]
                inventory[item.mn].append(item.type)
                inventory[item.mn].append(count)


# Write dictionary values in an excel file
workbook = xlsxwriter.Workbook('zip.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0

# Write column names
worksheet.write(0, 0, "FRU model number")
worksheet.write(0, 1, "Description")
worksheet.write(0, 2, "Count")

order = sorted(inventory.keys())
for key in order:
    row += 1
    worksheet.write(row, col, key)
    i = 1
    for item in inventory[key]:
        worksheet.write(row, col + i, item)
        i += 1

workbook.close()
