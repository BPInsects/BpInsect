import os
import time
import pandas as pd
import numpy as np
import random
import xlwt
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.externals import joblib
import commonVariables

modelFileName = commonVariables.modelFileName
trainFileName = commonVariables.trainFileName


def save_model(model,name):
    joblib.dump(model,modelFileName+'/'+name)

def load_model(name):
    model = joblib.load(modelFileName+'/'+name)
    return model

def find_model(lcbm,kind):
    name = lcbm + '_' + kind
    namelist = []
    modelName = None

    for parent, dirnames, filenames in os.walk(modelFileName):
        if filenames != None:
            for filename in filenames:
                if filename[0,9] == name:
                    namelist.append(filename)

    if namelist != None:
        for name1 in namelist:
            if name1[10] == 'a':
                modelName =name1

        for name2 in namelist:
            if name2[10] == 'b':
                modelName =name2

    return modelName


def find_model(lcbm):
    name = lcbm
    namelist = []
    modelName = None

    for parent, dirnames, filenames in os.walk(modelFileName):
        if filenames != None:
            for filename in filenames:
                if filename[0, 4] == name:
                    namelist.append(filename)

    if namelist != None:
        for name1 in namelist:
            if name1[10] == 'a':
                modelName = name1

        for name2 in namelist:
            if name2[10] == 'b':
                modelName = name2

    return modelName

def change_model(f,dataList,lcbm,kind):
    existDataList = []
    name = lcbm + '_' + kind
    for parent, dirnames, filenames in os.walk(trainFileName):
        if filenames != None:
            for filename in filenames:
                if filenames[0,9] == name:
                    existDataList.append(filename)

    if existDataList != None:
        df = pd.read_excel(trainFileName+'/'+existDataList[-1])
        train = df[:].values.tolist()
        train = np.array(train)
        train = train + dataList

        row = train.__len__()
        for i in range(200):
            m1 = random.randint(0, row)
            m2 = random.randint(0, row)
            train[[m1, m2], :] = train[[m2, m1], :]

        trainLength = row//10*8
        for i in range(200):
            m1 = random.randint(0, trainLength)
            m2 = random.randint(0, trainLength)
            train[[m1, m2], :] = train[[m2, m1], :]
        y = train[:, -1]

        train_data = train[:, 0:-1]
        x_train = train_data[0:trainLength].copy()
        x_test = train_data[trainLength:].copy()
        y_train = y[0:trainLength].copy()
        y_test = y[trainLength:].copy()


        x_train = preprocessing.scale(x_train)
        x_test = preprocessing.scale(x_test)
        d = {}

        for Y in range(3, 20):
            model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(Y,), random_state=1, max_iter=100000,
                                  momentum=0.9,
                                  activation='logistic', learning_rate_init=0.001, tol=1e-5)

            model.fit(x_train, y_train)

            d[Y] = model.score(x_test, y_test)

        maxY = 3
        maxscore = 0
        for key in d:
            if maxscore < d[key]:
                maxY = key

        print(maxY)
        model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(maxY,), random_state=1, max_iter=100000,
                              momentum=0.9,
                              verbose=10,
                              activation='logistic', learning_rate_init=0.001, tol=1e-5)

        time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        modelName =  lcbm+'_'+kind+'_'+'c_'+time1+'_'+str(f)+'.model'

        save_model(model,modelFileName+'/'+modelName)
        # 此处将新的数据存储
        saveFile(train,modelName)
        return modelName


def saveFile(datalist,name):

    dataList = list(datalist)
    row = dataList.__len__()

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)
    fields = ['timeGap', 'barnTemp', 'y']
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field])

    for i in range(1, row + 1):
        for j in range(list(dataList[0]).__len__()):
            trans = int(dataList[i - 1][j])
            sheet.write(i, j, trans)
    # workbook.save(r'../res/readout.xls')
    workbook.save(trainFileName+'/'+name+'.xls')




