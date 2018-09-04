import os
import random
import pandas as pd
import xlwt
import time

df = pd.read_excel("../res/primary5.xlsx")
columns = df.columns.size
row = df.iloc[:,0].size-1
source = []
zero = []
target = []
for i in range(0,row):
    column = []
    for j in df:
        column.append(df[j][i])
    source.append(column)
for i in source:
    y = i[3]
    if y == 0:
        zero.append(i)

for i in zero:
    before = i[0]

    for j in source:
        targetColumn = []
        now = j[0]
        yj = j[3]
        if yj == 0:
            continue
        diffDays = (now-before).days
        targetColumn.append(diffDays)
        targetColumn.append(float(i[1]))
        targetColumn.append(float(i[2]))
        targetColumn.append(float(yj-i[3]))
        target.append(targetColumn)

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('table_message',cell_overwrite_ok=True)
fields = ['timeGap','barnTemp','grainTemp','y']
for field in range(0,len(fields)):
    sheet.write(0,field,fields[field])

for i in range(0,len(target)):
    row = target[i]
    for j in range(0,len(row)):
        print(row[j])
        sheet.write(i+1,j,row[j])
workbook.save('../res/readout7.xls')
