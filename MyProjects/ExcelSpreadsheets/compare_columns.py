import pandas as pd

f1 = 'c:/Users/imatu/Documents/Projects/RTK-Service/Lab/Nokia spares for sell/IP лаборатория Nokia v4 GL.xlsx'
f2 = 'c:/Users/imatu/Documents/Projects/RTK-Service/Lab/Nokia spares for sell/Оборудование РТК-СТ лаборатория.xlsx'

df1 = pd.read_excel(f1, "Спека лабы IP", usecols=['part #'])
df2 = pd.read_excel(f2, "№8", usecols=['Артикул'])
df3 = pd.read_excel(f2, "№9", usecols=['Артикул'])
df4 = pd.read_excel(f2, "№10", usecols=['Артикул'])
df5 = pd.read_excel(f2, "№11", usecols=['Артикул'])
df6 = pd.read_excel(f2, "№12", usecols=['Артикул'])
df7 = pd.read_excel(f2, "№13", usecols=['Артикул'])
df8 = pd.read_excel(f2, "№14", usecols=['Артикул'])
df9 = pd.read_excel(f2, "№15", usecols=['Артикул'])
df10 = pd.read_excel(f2, "№16", usecols=['Артикул'])
df11 = pd.read_excel(f2, "№17", usecols=['Артикул'])
df12 = pd.read_excel(f2, "PO 20", usecols=['Артикул'])

vals1 = set(df1['part #']).intersection(df2['Артикул'])
vals2 = set(df1['part #']).intersection(df3['Артикул'])
vals3 = set(df1['part #']).intersection(df4['Артикул'])
vals4 = set(df1['part #']).intersection(df5['Артикул'])
vals5 = set(df1['part #']).intersection(df6['Артикул'])
vals6 = set(df1['part #']).intersection(df7['Артикул'])
vals7 = set(df1['part #']).intersection(df8['Артикул'])
vals8 = set(df1['part #']).intersection(df9['Артикул'])
vals9 = set(df1['part #']).intersection(df10['Артикул'])
vals10 = set(df1['part #']).intersection(df11['Артикул'])
vals11 = set(df1['part #']).intersection(df12['Артикул'])

print("№8", vals1)
print("№9", vals2)
print("№10", vals3)
print("№11", vals4)
print("№12", vals5)
print("№13", vals6)
print("№14", vals7)
print("№15", vals8)
print("№16", vals9)
print("№17", vals10)
print("№20", vals11)


