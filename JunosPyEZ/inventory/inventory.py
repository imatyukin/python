#!/usr/bin/env python3

import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
import xlsxwriter

password = getpass("Device password: ")

hosts_tacacs_core = ["XXX.XXX.XXX.XXX", "XXX.XXX.XXX.XXX"]
hosts_tacacs_ag = ["YYY.YYY.YYY.YYY", "YYY.YYY.YYY.YYY"]

dict_inventory = {}

yml_file = "jinventory.yml"
globals().update(loadyaml(yml_file))

def func_inventory():
    tbl = JModuleTable(dev).get()
    for item in tbl:
            # print("%s\t%s" % (item.type, item.mn))
            if not item.mn in dict_inventory:
                if item.mn is not None:
                    count = 1
                    dict_inventory.setdefault(item.mn, []).append(item.type)
                    dict_inventory[item.mn].append(count)
            else:
                if item.mn is not None:
                    count = dict_inventory[item.mn][-1]
                    count += 1
                    del dict_inventory[item.mn][:]
                    dict_inventory[item.mn].append(item.type)
                    dict_inventory[item.mn].append(count)

def func_excel():
    # Write dictionary values in an excel file
    workbook = xlsxwriter.Workbook('zip.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0

    # Write column names
    worksheet.write(0, 0,  "FRU model number")
    worksheet.write(0, 1,  "Description")
    worksheet.write(0, 2,  "QTY")
    worksheet.write(0, 3,  "QTY Arkhangelsk")
    worksheet.write(0, 4,  "QTY Vologda")
    worksheet.write(0, 5,  "QTY Kaliningrad")
    worksheet.write(0, 6,  "QTY Karelia")
    worksheet.write(0, 7,  "QTY Komi")
    worksheet.write(0, 8,  "QTY Murmansk")
    worksheet.write(0, 9,  "QTY Novgorod/Pskov")
    worksheet.write(0, 10, "QTY SPb/LO")
    worksheet.write(0, 11, "Calc ZIP")
    worksheet.write(0, 12, "MB Arkhangelsk")
    worksheet.write(0, 13, "MB Vologda")
    worksheet.write(0, 14, "MB Kaliningrad")
    worksheet.write(0, 15, "MB Karelia")
    worksheet.write(0, 16, "MB Komi")
    worksheet.write(0, 17, "MB Murmansk")
    worksheet.write(0, 18, "MB Novgorod/Pskov")
    worksheet.write(0, 19, "MB SPb/LO")
    worksheet.write(0, 20, "CZIP SPb")
    worksheet.write(0, 21, "Interchangeability")

    order = sorted(dict_inventory.keys())
    for key in order:
        row += 1
        worksheet.write(row, col, key)
        i = 1
        for item in dict_inventory[key]:
            worksheet.write(row, col + i, item)
            i += 1

    # worksheet.write_array_formula('L2:L23', '{=IF(ROUND((C2/25);0)<1;1;ROUND((C2/25);0))}')

    workbook.close()


# Telnet connection
for host_core in hosts_tacacs_core:
    username = 'LoginX'
    dev = Device(host=host_core, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + host_core)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory()

for host_ag in hosts_tacacs_ag:
    username = 'LoginY'
    dev = Device(host=host_ag, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + host_ag)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory()


func_excel()
