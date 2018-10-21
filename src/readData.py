import os
import random
import pandas as pd
import xlwt
import time

df = pd.read_excel("../res/primary6.xlsx")
columns = df.columns.size-1
row = df.iloc[:,0].size

read = [([0] * 1) for i in range(row)]
outTime = []
timeGap = []

outPut = []
count = 0

for i in range(row):
    read[i]=df.loc[i]


# print(row)
# print(read[0])
# print(read[0][0])
# print(read[0][1])
# print(read[0][2])
# print(read[0][3])
# print(read[1][1]-read[0][0])

for date in range(row):
    outTime.append(time.mktime(time.strptime(read[date][0].ctime(),"%a %b %d %H:%M:%S %Y")))
    print(type(read[date][0]))


for i in range(row):
    for j in range(i+1,row):
        timeGap.append((read[j][1]-read[i][1]).days)
        outPut.append(int(read[j][3]-read[i][3]))


workbook = xlwt.Workbook()
sheet = workbook.add_sheet('table_message',cell_overwrite_ok=True)
fields = ['timeGap','barnTemp','y']
for field in range(0,len(fields)):
    sheet.write(0,field,fields[field])

for i in range(1,row):
    for j in range(i+1,row):
        count = count+1
        for column in range(0,fields.__len__()):
            if column == 0:
                sheet.write(count,column,timeGap[count-1])
            elif column == 1:
                sheet.write(count,column,int(read[i-1][column+1]))
            else:
                sheet.write(count, column, outPut[count - 1])

print(count)


# workbook.save(r'../res/readout.xls')
workbook.save(r'../res/readout8.xls')

