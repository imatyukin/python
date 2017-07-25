#!/usr/bin/env python3

row_data = {}

with open('PaceData.csv') as paces:

    column_headings = paces.readline().strip().split(',')
    column_headings.pop(0)

    for each_line in paces:
        row = each_line.strip().split(',')
        row_label = row.pop(0)
        inner_dict = {}
        for i in range(len(column_headings)):
            inner_dict[row[i]] = column_headings[i]
        row_data[row_label] = inner_dict

num_cols = len(column_headings)
print(num_cols, end=' -> ')
print(column_headings)

num_2mi = len(row_data['2mi'])
print(num_2mi, end=' -> ')
print(row_data['2mi'])

num_Marathon = len(row_data['Marathon'])
print(num_Marathon, end=' -> ')
print(row_data['Marathon'])

print('\n================================ RESTART ================================\n')

column_heading = row_data['15k']['43:24']
print(column_heading)

prediction = [k for k in row_data['20k'].keys() if row_data['20k'][k] == column_heading]
print(prediction)

print('\n================================ RESTART ================================\n')

times = [t for t in row_data['Marathon'].keys()]
print(times)

times = []
for each_t in row_data['Marathon'].keys():
    times.append(each_t)
print(times)

print('\n================================ RESTART ================================\n')

headings = [h for h in sorted(row_data['10mi'].values(), reverse=True)]
print(headings)

headings = []
for each_h in sorted(row_data['10mi'].values(), reverse=True):
    headings.append(each_h)
print(headings)

print('\n================================ RESTART ================================\n')

time = [t for t in row_data['20k'].keys() if row_data['20k'][t] == '79.3']
print(time)

time = []
for each_t in row_data['20k'].keys():
    if row_data['20k'][each_t] == '79.3':
        time.append(each_t)
print(time)