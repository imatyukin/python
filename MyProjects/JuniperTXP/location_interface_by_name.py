#!/usr/bin/env python3
import sys

fpc = {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','10':'10','11':'11','12':'12','13':'13','14':'14','15':'15','16':'16','17':'17','18':'18','19':'19','20':'20','21':'21','22':'22','23':'23','24':'24','25':'25','26':'26','27':'27','28':'28','29':'29','30':'30','31':'31'}
select_fpc = input("Select FPC (0..31): ")
if select_fpc in fpc:
    the_fpc = int(fpc[select_fpc])
else:
    print("error: fpc value outside range 0..31 for '%s'" % select_fpc)
    sys.exit()

pic = {'0':'0','1':'1'}
select_pic = input("Select PIC (0..1): ")
if select_pic in pic:
    the_pic = int(pic[select_pic])
else:
    print("error: pic value outside range 0..1 for '%s'" % select_pic)
    sys.exit()

xcvr = {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8'}
select_xcvr = input("Select Xcvr (0..8): ")
if select_xcvr in xcvr:
    the_xcvr = int(xcvr[select_xcvr])
else:
    print("error: xcvr value outside range 0..8 for '%s'" % select_xcvr)
    sys.exit()

lcc_x = str(the_fpc//8)
fpc_x = str(the_fpc%8)

msg_lcc='''LCC: '''
msg_fpc='''FPC: '''
msg_pic='''PIC: '''
msg_xcvr='''Xcvr: '''

print('\n'+'Interface Name: '+str(select_fpc)+'/'+str(select_pic)+'/'+str(select_xcvr))
print(msg_lcc+str(lcc_x)+',', msg_fpc+str(fpc_x)+',', msg_pic+str(the_pic)+',', msg_xcvr+str(the_xcvr))