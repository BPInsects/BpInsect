import os
import random
import pandas as pd
import numpy as np
import xlwt
import time

df = pd.read_excel("../res/readout8.xls")
read = df[:].values.tolist()
read = np.array(read)
row = df.iloc[:,0].size
columns = df.columns.size

# print(row)


for i in range(200):
   m1 =  random.randint(0,135)
   m2 = random.randint(0,135)
   read[[m1, m2], :] = read[[m2, m1], :]

print(read)

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('table_message',cell_overwrite_ok=True)
fields = ['timeGap','barnTemp','y']
for field in range(0,len(fields)):
    sheet.write(0,field,fields[field])


for i in range(1,row+1):
    for j in range(columns):
        trans = int(read[i-1][j])
        sheet.write(i,j, trans)
# workbook.save(r'../res/readout.xls')
workbook.save(r'../res/savedata2.xls')