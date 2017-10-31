#!/usr/bin/env python3

import sys

lcc = {'0':'0','1':'1','2':'2','3':'3'}
select_lcc = input('Select LCC (0..3): ')
if select_lcc in lcc:
    the_lcc = int(lcc[select_lcc])
else:
    print('LCC %s not exist' % select_lcc)
    sys.exit()

fpc = {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7'}
select_fpc = input("Select FPC (0..7): ")
if select_fpc in fpc:
    the_fpc = int(fpc[select_fpc])
else:
    print('FPC %s not exist' % select_fpc)
    sys.exit()

pic = {'0':'0','1':'1'}
select_pic = input("Select PIC (0..1): ")
if select_pic in pic:
    the_pic = int(pic[select_pic])
else:
    print('PIC %s not exist' % select_pic)
    sys.exit()

xcvr = {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8'}
select_xcvr = input("Select Xcvr (0..8): ")
if select_xcvr in xcvr:
    the_xcvr = int(xcvr[select_xcvr])
else:
    print('Xcvr %s not exist' % select_xcvr)
    sys.exit()

fpc_x = 8*(the_lcc+1)-8+the_fpc

print('\n'+'Global FPC: '+str(fpc_x))
print('Interface Name: '+str(fpc_x)+('/')+str(the_pic)+('/')+str(the_xcvr))
