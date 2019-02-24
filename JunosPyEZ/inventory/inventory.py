#!/usr/bin/env python3

import sys
from getpass import getpass
from jnpr.junos import Device
from jnpr.junos.factory import loadyaml
import xlsxwriter

password = getpass("Device password: ")

# Arkhangelsk
with open('arkh_core.txt') as arkh_core_hosts:
    arkh_core = arkh_core_hosts.read().split( )
with open('arkh_aggr.txt') as arkh_aggr_hosts:
    arkh_aggr = arkh_aggr_hosts.read().split( )
# Vologda
with open('vlgd_core.txt') as vlgd_core_hosts:
    vlgd_core = vlgd_core_hosts.read().split( )
with open('vlgd_aggr.txt') as vlgd_aggr_hosts:
    vlgd_aggr = vlgd_aggr_hosts.read().split( )
# Kaliningrad
with open('klng_core.txt') as klng_core_hosts:
    klng_core = klng_core_hosts.read().split( )
with open('klng_aggr.txt') as klng_aggr_hosts:
    klng_aggr= klng_aggr_hosts.read().split( )
# Karelia
with open('ptzv_core.txt') as ptzv_core_hosts:
    ptzv_core = ptzv_core_hosts.read().split( )
with open('ptzv_aggr.txt') as ptzv_aggr_hosts:
    ptzv_aggr = ptzv_aggr_hosts.read().split( )
# Komi
with open('sktv_core.txt') as sktv_core_hosts:
    sktv_core = sktv_core_hosts.read().split( )
with open('sktv_aggr.txt') as sktv_aggr_hosts:
    sktv_aggr = sktv_aggr_hosts.read().split( )
# Murmansk
with open('mrsk_core.txt') as mrsk_core_hosts:
    mrsk_core = mrsk_core_hosts.read().split( )
with open('mrsk_aggr.txt') as mrsk_aggr_hosts:
    mrsk_aggr = mrsk_aggr_hosts.read().split( )
# Novgorod/Pskov
with open('vnov_core.txt') as vnov_core_hosts:
    vnov_core = vnov_core_hosts.read().split( )
with open('vnov_aggr.txt') as vnov_aggr_hosts:
    vnov_aggr = vnov_aggr_hosts.read().split( )
# SPb/LO
with open('spbr_core.txt') as spbr_core_hosts:
    spbr_core = spbr_core_hosts.read().split( )
with open('spbr_aggr.txt') as spbr_aggr_hosts:
    spbr_aggr = spbr_aggr_hosts.read().split( )

dict_inventory = {}

yml_file = "jinventory.yml"
globals().update(loadyaml(yml_file))

def func_inventory(tag):
    tbl = JModuleTable(dev).get()
    for item in tbl:
            # print("%s\t%s" % (item.type, item.mn))
            if not item.mn in dict_inventory:
                if item.mn is not None:
                    if tag == 29:
                        arkh_count = 1
                        vlgd_count = 0
                        klng_count = 0
                        ptzv_count = 0
                        sktv_count = 0
                        mrsk_count = 0
                        vnov_count = 0
                        spbr_count = 0
                    elif tag == 35:
                        vlgd_count = 1
                        arkh_count = 0
                        klng_count = 0
                        ptzv_count = 0
                        sktv_count = 0
                        mrsk_count = 0
                        vnov_count = 0
                        spbr_count = 0
                    elif tag == 39:
                        klng_count = 1
                        arkh_count = 0
                        vlgd_count = 0
                        ptzv_count = 0
                        sktv_count = 0
                        mrsk_count = 0
                        vnov_count = 0
                        spbr_count = 0
                    elif tag == 10:
                        ptzv_count = 1
                        arkh_count = 0
                        vlgd_count = 0
                        klng_count = 0
                        sktv_count = 0
                        mrsk_count = 0
                        vnov_count = 0
                        spbr_count = 0
                    elif tag == 11:
                        sktv_count = 1
                        arkh_count = 0
                        vlgd_count = 0
                        klng_count = 0
                        ptzv_count = 0
                        mrsk_count = 0
                        vnov_count = 0
                        spbr_count = 0
                    elif tag == 51:
                        mrsk_count = 1
                        arkh_count = 0
                        vlgd_count = 0
                        klng_count = 0
                        ptzv_count = 0
                        sktv_count = 0
                        vnov_count = 0
                        spbr_count = 0
                    elif tag == 53:
                        vnov_count = 1
                        arkh_count = 0
                        vlgd_count = 0
                        klng_count = 0
                        ptzv_count = 0
                        sktv_count = 0
                        mrsk_count = 0
                        spbr_count = 0
                    elif tag == 78:
                        spbr_count = 1
                        arkh_count = 0
                        vlgd_count = 0
                        klng_count = 0
                        ptzv_count = 0
                        sktv_count = 0
                        mrsk_count = 0
                        vnov_count = 0
                    count = 1
                    dict_inventory.setdefault(item.mn, []).append(item.type)
                    dict_inventory[item.mn].append(count)
                    dict_inventory[item.mn].append(arkh_count)
                    dict_inventory[item.mn].append(vlgd_count)
                    dict_inventory[item.mn].append(klng_count)
                    dict_inventory[item.mn].append(ptzv_count)
                    dict_inventory[item.mn].append(sktv_count)
                    dict_inventory[item.mn].append(mrsk_count)
                    dict_inventory[item.mn].append(vnov_count)
                    dict_inventory[item.mn].append(spbr_count)
            else:
                if item.mn is not None:
                    count = dict_inventory[item.mn][1]
                    arkh_count = dict_inventory[item.mn][2]
                    vlgd_count = dict_inventory[item.mn][3]
                    klng_count = dict_inventory[item.mn][4]
                    ptzv_count = dict_inventory[item.mn][5]
                    sktv_count = dict_inventory[item.mn][6]
                    mrsk_count = dict_inventory[item.mn][7]
                    vnov_count = dict_inventory[item.mn][8]
                    spbr_count = dict_inventory[item.mn][9]
                    if tag == 29:
                        arkh_count += 1
                    if tag == 35:
                        vlgd_count += 1
                    if tag == 39:
                        klng_count += 1
                    if tag == 10:
                        ptzv_count += 1
                    if tag == 11:
                        sktv_count += 1
                    if tag == 51:
                        mrsk_count += 1
                    if tag == 53:
                        vnov_count += 1
                    if tag == 78:
                        spbr_count += 1
                    count += 1
                    del dict_inventory[item.mn][:]
                    dict_inventory[item.mn].append(item.type)
                    dict_inventory[item.mn].append(count)
                    dict_inventory[item.mn].append(arkh_count)
                    dict_inventory[item.mn].append(vlgd_count)
                    dict_inventory[item.mn].append(klng_count)
                    dict_inventory[item.mn].append(ptzv_count)
                    dict_inventory[item.mn].append(sktv_count)
                    dict_inventory[item.mn].append(mrsk_count)
                    dict_inventory[item.mn].append(vnov_count)
                    dict_inventory[item.mn].append(spbr_count)

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
# Arkhangelsk
for arkh_core_host in arkh_core:
    tag = 29
    username = 'login'
    dev = Device(host=arkh_core_host, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + arkh_core_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

for arkh_aggr_host in arkh_aggr:
    tag = 29
    username = 'username'
    dev = Device(host=arkh_aggr_host, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + arkh_aggr_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

# Vologda
for vlgd_core_host in vlgd_core:
    tag = 35
    username = 'login'
    dev = Device(host=vlgd_core_host, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + vlgd_core_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

for vlgd_aggr_host in vlgd_aggr:
    tag = 35
    username = 'username'
    dev = Device(host=vlgd_aggr_host, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + vlgd_aggr_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

# Kaliningrad
for klng_core_host in klng_core:
    tag = 39
    username = 'login'
    dev = Device(host=klng_core_host, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + klng_core_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

for klng_aggr_host in klng_aggr:
    tag = 39
    username = 'username'
    dev = Device(host=klng_aggr_host, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + klng_aggr_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

# Karelia
for ptzv_core_host in ptzv_core:
    tag = 10
    username = 'login'
    dev = Device(host=ptzv_core_host, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + ptzv_core_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

for ptzv_aggr_host in ptzv_aggr:
    tag = 10
    username = 'username'
    dev = Device(host=ptzv_aggr_host, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + ptzv_aggr_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

# Komi
for sktv_core_host in sktv_core:
    tag = 11
    username = 'login'
    dev = Device(host=sktv_core_host, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + sktv_core_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

for sktv_aggr_host in sktv_aggr:
    tag = 11
    username = 'username'
    dev = Device(host=sktv_aggr_host, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + sktv_aggr_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

# Murmansk
for mrsk_core_host in mrsk_core:
    tag = 51
    username = 'login'
    dev = Device(host=mrsk_core_host, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + mrsk_core_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

for mrsk_aggr_host in mrsk_aggr:
    tag = 51
    username = 'username'
    dev = Device(host=mrsk_aggr_host, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + mrsk_aggr_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

# Novgorod/Pskov
for vnov_core_host in vnov_core:
    tag = 53
    username = 'login'
    dev = Device(host=vnov_core_host, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + vnov_core_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

for vnov_aggr_host in vnov_aggr:
    tag = 53
    username = 'username'
    dev = Device(host=vnov_aggr_host, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + vnov_aggr_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

# SPb/LO
for spbr_core_host in spbr_core:
    tag = 78
    username = 'login'
    dev = Device(host=spbr_core_host, user=username, passwd=password, mode='telnet', port='23')
    try:
            dev.open()
            print("Connected to " + spbr_core_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)

for spbr_aggr_host in spbr_aggr:
    tag = 78
    username = 'username'
    dev = Device(host=spbr_aggr_host, user=username, passwd=password, port='22')
    try:
            dev.open()
            print("Connected to " + spbr_aggr_host)
    except:
            print("Connection failed.")
            sys.exit(1)

    func_inventory(tag)


func_excel()
