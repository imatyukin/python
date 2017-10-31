#!/usr/bin/env python3

'''
xe-0/0/0 {
    unit 0 {
        family ethernet-switching {
            port-mode trunk;
            vlan {
                members [ 1204 1238 351 352 353 1205 1102-1105 ];
            }
        }
    }
}
'''

members_orig = '[ 1204 1238 351 352 353 1205 1102-1105 ]'
members_orig = members_orig[2:][:-2]
members = members_orig.split(' ')
members.sort(key=lambda x: int(x[:4]))
print(members)
