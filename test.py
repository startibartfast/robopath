'''
Created on Dec 7, 2018

@author: carlo
'''

import csv

with open('/home/carlo/Downloads/Out_csv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        s = row[0]
        #rs = map(lambda r: r.name, self.robots)
        ps = map(lambda p: int(p[1:]), s.split(","))
        print(list(ps))
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
        #print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
        #line_count += 1
        #print(row[0])
    #print(f'Processed {line_count} lines.')