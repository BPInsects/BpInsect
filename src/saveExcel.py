import os
import random

import pandas as pd
import xlwt

dirs = os.listdir('2009年')
newList = []
prefix = '2009年/'
temps = []
gtemps = []
atemps = []
ghums = []
ahums = []
humidity = []
moisture = []
for file in dirs:
    if not file.__contains__('$'):
        newList.append(prefix+file)
for file in newList:
    df = pd.read_excel(file)
    temp = df.loc[26][9]
    gtemp = df.loc[25][1]
    atemp = df.loc[25][3]
    ghum = df.loc[25][5]
    ahum = df.loc[25][7]
    temps.append(temp)
    gtemps.append(gtemp)
    atemps.append(atemp)
    ghums.append(ghum)
    ahums.append(ahum)

dir2 = os.listdir('wwww')
prefix2 = 'wwww/'
fl = []
for file in dir2:
    if not file.__contains__('$'):
            fl.append(prefix2+file)

for file in fl:
    df = pd.read_excel(file)
    h = df.loc[6][3]
    m = df.loc[6][4]
    humidity.append(h)
    moisture.append(m)

for i in range(0,6):
    df = pd.read_excel(fl[i])
    h = df.loc[6+i][3]
    m = df.loc[6+i][4]
    humidity.append(h)
    moisture.append(m)

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('table_message',cell_overwrite_ok=True)
fields = ['temperature','humidity','moisture','gtemp','ghum','atemp','ahum','y']
for field in range(0,len(fields)):
    sheet.write(0,field,fields[field])

row = 1
col = 0
TABLE = {"normal":0,"critical":1,"danger":2}
print(temps)
y = []
for i in range(0,52):
    a =int(random.uniform(0, 3))
    y.append(a)
for i in range(0, 52):
    temperature = temps[i]
    if temperature > 20:
        y[i] = 2
        continue

    if humidity[i] > 70:
        y[i] = 2
        continue
    if moisture[i] > 14:
        y[i] = 2

    gtemperature = gtemps[i]
    atemperature = atemps[i]
    if temperature-gtemperature > 5:
        y[i] = 2
        continue
    if temperature - atemperature > 5:
        y[i] = 1
        continue
    if ghums[i]  > 50:
        y[i] = 1
        continue
    if ahums[i] > 50:
        y[i] = 1
        continue
    y[i] = 0
for row in range(1,len(humidity)+1):
    sheet.write(row, 0,'%.2f' % temps[row-1])
    sheet.write(row, 1, '%.2f' % humidity[row - 1])
    sheet.write(row, 2, '%.2f' % moisture[row - 1])
    sheet.write(row, 3, '%.2f' % gtemps[row - 1])
    sheet.write(row, 4, '%.2f' % ghums[row - 1])
    sheet.write(row, 5, '%.2f' % atemps[row - 1])
    sheet.write(row, 6, '%.2f' % ahums[row - 1])
    sheet.write(row, 7, y[row - 1])
workbook.save(r'./readout.xls')



