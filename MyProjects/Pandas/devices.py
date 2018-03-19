#!/usr/bin/env python3
import pandas as pd

df = pd.read_csv('devices.csv', sep=';', encoding='utf-8')

header = ["Hostname", "IP-address"]
df.to_csv('as8997.dat', columns=header, index=False, sep='\t', encoding='utf-8')

# print(df.loc[:,['Hostname','IP-address']])

data = pd.read_table('as8997.dat', index_col='Hostname')
print(data[:])
