# coding=utf-8
import os
import pandas as pd
import numpy as np
import random

import time
import xlwt
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from sklearn.externals import joblib
import commonVariables
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

modelFileName = commonVariables.modelFileName
trainFileName = commonVariables.trainFileName


def save_model(model, name):
    joblib.dump(model, modelFileName + '\\' + name)


def load_model(name):
    # model = joblib.load(modelFileName +"\\"+ unicode(name,'utf-8'))
    model = joblib.load(modelFileName + "\\" + name)
    return model


def find_model1(lcbm, kind):
    namelist = []
    result = {
        "success": False,
        "msg": "没有模型",
        "obj": [
            {
                "kind": kind,
                "lcbm": lcbm,
                "type": "",
                "fittingAccuracy": "",
                "predictionAccuracy": "",
                "danger": "",
                "modelName": ""
            }
        ]
    }

    for parent, dirnames, filenames in os.walk(modelFileName + "/" + lcbm):
        if filenames != None:
            for filename in filenames:
                if filename.split("_")[1].encode('utf-8') == kind.strip().decode('utf-8'):
                    namelist.append(filename)

    if namelist.__len__() > 0:
        result['success'] = True
        result['msg'] = "成功找到模型"

        for name in namelist:
            Name = name.split("_")
            result['obj'].append({
                "lcbm": lcbm,
                "kind": Name[1],
                "type": Name[2],
                "fittingAccuracy": float(Name[3]),
                "predictionAccuracy": float(Name[4]),
                "danger": int(Name[5]),
                "modelName": name,
            })

    del result['obj'][0]

    return result


def find_model(lcbm):
    namelist = []
    result = {
        "success": False,
        "msg": "没有模型",
        "obj": [
            {
                "lcbm": lcbm,
                "kind": "",
                "type": "",
                "fittingAccuracy": "",
                "predictionAccuracy": "",
                "danger": "",
                "modelName": ""
            }
        ]
    }

    filemap = {
    }
    for parent, dirnames, filenames in os.walk(modelFileName + "\\" + lcbm):
        for filename in filenames:
            kind = filename.split("_")[1]
            if filename.split("_")[2]!='c':
                if filemap.has_key(kind):
                    if filemap[kind].split("_")[2]=='a':
                        filemap.update({kind:filename})
                else:
                    filemap.update({kind:filename})
    namelist = list(filemap.values())
    if namelist.__len__() > 0:
        result['success'] = True
        result['msg'] = "成功找到模型"
        for name in namelist:
            Name = name.split("_")
            result['obj'].append({
                "lcbm": lcbm,
                "kind": Name[1],
                "type": Name[2],
                "fittingAccuracy": float(Name[3]),
                "predictionAccuracy": float(Name[4]),
                "danger": int(Name[5]),
                "modelName": name,
            })

    del result['obj'][0]

    return result

def findAllModel(lcbm):
    lcbm = lcbm.strip()
    namelist = []
    print(modelFileName +"\\"+ lcbm)
    for parent, dirnames, filenames in os.walk(modelFileName +"\\"+ lcbm):
        namelist = list(filenames)
    return namelist


def change_model(f, dataList, lcbm, kind):
    existDataList = []
    for parent, dirnames, filenames in os.walk(trainFileName+"\\"+lcbm):
        if filenames.__len__() > 0:
            for filename in filenames:
                if filename.split("_")[1].decode('utf-8') == kind.strip().decode('utf-8') and filename.split("_")[2] == 'a':
                    existDataList.append(filename)
        else:
            existDataList = []
    # TUDO 补充非空情况
    if existDataList.__len__() > 0:
        df = pd.read_excel(trainFileName + '\\' + lcbm + "\\"+existDataList[0].decode('utf-8'))
        train = df[:].values.tolist()

    else:
        train = []

    train = train + dataList
    train = np.array(train)
    row = train.__len__()
    for i in range(200):
        m1 = random.randint(0, row-1)
        m2 = random.randint(0, row-1)
        train[[m1, m2], :] = train[[m2, m1], :]

    trainLength = row // 10 * 8
    for i in range(200):
        m1 = random.randint(0, trainLength-1)
        m2 = random.randint(0, trainLength-1)
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

    # for Y in range(3, 20):
    #     model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(Y,), random_state=1, max_iter=100000,
    #                           momentum=0.9,
    #                           activation='logistic', learning_rate_init=0.001, tol=1e-5,verbose=10)
    #
    #     model.fit(x_train, y_train)
    #
    #     d[Y] = model.score(x_test, y_test)
    #
    # maxY = 3
    # maxscore = 0
    # for key in d:
    #     if maxscore < d[key]:
    #         maxY = key

    model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1, max_iter=100000,
                          momentum=0.9,
                          verbose=10,
                          activation='logistic', learning_rate_init=0.001, tol=1e-5)
    model.fit(x_train, y_train)
    print(model.loss_)
    fittingAccuracy = round(1 - model.loss_, 6)
    predictionAccuracy = round(model.score(x_test, y_test), 4)
    modelList = find_model1(lcbm, kind)
    if modelList['obj'].__len__() == 1:
        preModel = modelList['obj'][0]
    else:
        for model in modelList['obj']:
            if model['type'] == 'b':
                preModel = model
                break
            if model['type'] == 'a':
                preModel = model

    beforeFittingAccuracy = preModel['fittingAccuracy']
    beforePredictionAccuracy = preModel['predictionAccuracy']

    modelName = lcbm + '_' + kind + '_' + 'c_' + str(fittingAccuracy) + '_' + str(predictionAccuracy) + '_' + str(f)

    save_model(model, lcbm+"\\"+modelName.decode('utf-8'))
    # 此处将新的数据存储
    # saveFile(train, modelName)

    result = {
        "success": False,
        "msg": "改变模型失败",
        "obj": {
            "modelName": "",
            "fittingAccuracy": "",
            "predictionAccuracy": "",
            "beforeFittingAccuracy": "",
            "beforePredictionAccuracy": ""
        }
    }

    result['success'] = True
    result['msg'] = "更换模型成功"
    result['obj'] = {
        "modelName": modelName,
        "fittingAccuracy": fittingAccuracy,
        "predictionAccuracy": predictionAccuracy,
        "beforeFittingAccuracy": beforeFittingAccuracy,
        "beforePredictionAccuracy": beforePredictionAccuracy
    }
    print(result)

    return result


def saveFile(datalist, name):
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
    workbook.save(trainFileName + '\\' + name + '.xls')


def savePrimaryFile(datalist,lcbm, name):

    dataList = list(datalist)
    row = dataList.__len__()

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)
    fields = ['date', 'barnTemp', 'number']
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field])

    for i in range(1, row + 1):
        for j in range(list(dataList[0]).__len__()):
            if j == 0:
                trans = dataList[i - 1][j]
            else:
                trans = int(dataList[i - 1][j])
            sheet.write(i, j, trans)
    # workbook.save(r'../res/readout.xls')
    name = str(name).replace("a","c")
    name = str(name).replace("b","c")
    workbook.save(trainFileName + '\\'+lcbm+"\\" + name.decode('utf-8') + '.xls')

def readExcelFile(lcbm,name,origin):
    train = []
    names = name.split("_")
    model_type = 'b'
    if origin:
        model_type = 'a'

    for (path, dirs, files) in os.walk("trains" + "\\" + lcbm):
        for filename in files:
            filenames = filename.split("_")
            if model_type== filenames[2] and filenames[1] == names[1]:
                df = pd.read_excel(trainFileName+"\\"+lcbm+"\\"+filename)
                train = df[:].values.tolist()
                return train
    return train
