#!/usr/bin/env python3
import pandas as pd

df = pd.read_csv('devices.csv', sep=';', encoding='utf-8')

header = ["Description", "Hostname"]
df.to_csv('as8997.csv', columns=header, index=False, sep='\t', encoding='utf-8')

print(df.loc[:,['Description','Hostname']])
