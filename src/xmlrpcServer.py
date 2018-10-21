# coding=utf-8
# from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
#
# server = SimpleJSONRPCServer(('localhost', 8080))
# server.register_function(pow)
# server.register_function(lambda x,y: x+y, 'add')
# server.register_function(lambda x: x, 'ping')
# server.serve_forever()
import datetime
import pyjsonrpc
import GrainDataLoad as loader

import numpy as np
from modelManage import find_model, change_model, save_model, load_model, find_model1, saveFile, savePrimaryFile,findAllModel,readExcelFile
import json
import os
import time
from dateutil import parser
import pandas as pd
from sklearn import preprocessing

import commonVariables

modelFileName = commonVariables.modelFileName
trainFileName = commonVariables.trainFileName

x_train, y_train, x_test, y_test, trainList = loader.load_data("../res/savedata2.xls")


class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        """Test method"""
        return a + b

    # TODO 根据粮仓编号和虫的种类返回模型
    @pyjsonrpc.rpcmethod
    def createModel(self, lcbmlist, kindlist):
        name = '00100100101_小露尾甲_b_0.95_0.85_50'

        # print(lcbmlist)
        for lcbm in lcbmlist:
            for kind in kindlist:
                modelName = str(lcbm + "_" + kind + "_a_0.95_0.85_50").strip()
                saveModelName = lcbm + "\\" + modelName.decode('utf-8')
                saveFile(trainList, saveModelName)

    @pyjsonrpc.rpcmethod
    def createFolder(self, lcbmlist):
        for lcbm in lcbmlist:
            path = str("trains\\" + lcbm).strip()
            os.makedirs(path)

    # TODO 增加查询和预测方法
    @pyjsonrpc.rpcmethod
    def predictAll(self, hello):
        results = {"success": True, "msg": "", "obj": []}

        dataList = json.loads(hello)
        if dataList != None:
            for data in dataList:
                results['obj'].append(
                    RequestHandler.predict(data['lcbm'], data['temperature'], data['timeGap'], data['kind']))
        else:
            results['success'] = False
            results['msg'] = "没有找到模型"

        return results

    # TODO 根据粮仓编号恢复缺省模型
    # param：粮仓编号lcbm
    # return：无返回值
    @pyjsonrpc.rpcmethod
    def recoveryByLcbm(self, lcbm):
        result = {
            "success": False,
            "msg": "",
            "obj": ""
        }
        modelList = findAllModel(lcbm)
        for model in modelList:
            if model.split("_")[2] != 'a':
                os.remove(modelFileName + '\\' + lcbm + '\\' + model)
                os.remove(trainFileName + '\\' + lcbm + '\\' + model + '.xls')
        result['success'] = True
        return result

    @pyjsonrpc.rpcmethod
    def recoveryByLcbmAndKind(self, name):
        lcbm = name.split("_")[0]
        kind = name.split("_")[1]
        result = {
            "success": False,
            "msg": "",
            "obj": ""
        }
        modelList = find_model1(lcbm, kind)['obj']
        if modelList.__len__() > 0:
            for model in modelList:
                if model['modelName'].split("_")[2] != 'a':
                    os.remove(modelFileName + '\\' + lcbm + '\\' + model['modelName'])
                    os.remove(trainFileName + '\\' + lcbm + '\\' + model['modelName'] + '.xls')
        result['success'] = True
        return result

    @pyjsonrpc.rpcmethod
    def getTrainData(self, name):
        result = {"success": False, "msg": "没有该模型数据", "obj": []}

        lcbm = name.split("_")[0]
        datalist = []
        datalist = readExcelFile(lcbm, name)
        if datalist.__len__() > 0:
            result['success'] = True
            result["msg"] = "成功返回数据"
            for data in datalist:
                result['obj'].append({"collectTime": data[0], "temperature": data[1], "num": data[2]})
        return result


    @pyjsonrpc.rpcmethod
    def readModelListByKind(self, lcbm, kind):
        return find_model1(lcbm, kind)

    # TODO 根据粮仓编号返回模型
    # param：粮仓编号lcbm
    # return：返回模型列表List<model>
    @pyjsonrpc.rpcmethod
    def readModelListByLcbm(self, lcbm):
        return find_model(lcbm)

    # TODO 是否确认修改模型
    # param：模型名字name
    # param：布尔变量sure，为true时确认修改模型
    # return：无返回值
    @pyjsonrpc.rpcmethod
    def sureChangeModel(self, name, sure):
        result={
            "success":False,
            "msg":"",
            "obj":""
        }
        names = name.split("_")
        lcbm = names[0]
        kind = names[1]
        if sure == True:
            for (path, dirs, files) in os.walk(modelFileName+"\\"+lcbm):
                for filename in files:
                    filenames = filename.split("_")

                    if filename == name:
                        os.rename(modelFileName+"\\"+lcbm + "\\" + filename, modelFileName+"\\"+lcbm + "\\" + name.replace('c','b'))

                    if filenames[1] == kind and filenames[2] =='b':
                        os.remove(modelFileName+"\\"+lcbm + "\\" + filename)

            for (path, dirs, files) in os.walk(trainFileName+"\\"+lcbm):

                for filename in files:
                    filenames = filename.split("_")
                    if filenames[1] ==kind and filenames[2]=='b':
                        os.remove(trainFileName+"\\"+lcbm + "\\" + filename)
                    if filename == name+".xls":
                        os.rename(trainFileName+"\\"+lcbm + "\\" + filename, trainFileName+"\\"+lcbm + "\\" + name.replace('c','b')+".xls")

        else:
            os.remove(modelFileName + '\\' + lcbm + '\\' + name)
            os.remove(trainFileName + '\\' + lcbm + '\\' + name+".xls")

        result['success'] = True
        return result




    # TODO 根据粮仓编号、温度、时间间隔还有害虫种类预测未来一段时间内害虫数量
    # param：粮仓编号lcbm
    # param：当前温度temperature
    # param：预测的时间间隔timeGap
    # param：害虫种类kind
    # return：返回字典result
    @pyjsonrpc.rpcmethod
    def predict(self, lcbm, temperature, timeGap, kind):
        result = {"success": False, "msg": "",
            "obj": [{"kind": kind, "temperature": temperature, "lcbm": lcbm, "danger": 0, "results": []}]}
        modelList = find_model1(lcbm, kind)
        preModel = None
        if modelList['obj'].__len__() == 0:
            return result
        elif modelList['obj'].__len__() == 1:
            preModel = modelList['obj'][0]
        else:
            for model in modelList['obj']:
                if model['type'] == 'b':
                    preModel = model

        path = lcbm + "\\" + preModel['modelName']
        model = load_model(path)

        if model == None:
            result['success'] = False;
            result['msg'] = "没有该虫种的粮仓模型，无法预测"
            return result
        else:
            x_test = []
            for t in range(1, timeGap + 1):
                x_test.append([temperature, t])

            num = model.predict(preprocessing.scale(x_test))
            print(num)
            result['success'] = True
            result['msg'] = "成功预测"
            result['obj'][0]['danger'] = preModel['danger']

            for i in range(1, timeGap + 1):
                result['obj'][0]['results'].append({"timeGap": i, "num": int(num[i - 1])})

        return result

    @pyjsonrpc.rpcmethod
    def addTrainData(self, data):
        req = json.loads(data)
        modelName = req['name']
        danger = req['danger']
        datalist = req['data']
        dataExcelList = []
        trainData = []
        outTime = []
        number = []
        Temperature = []
        timeGap = []
        outPut = []
        count = 0
        for data in datalist:
            date = datetime.datetime.strptime((data['collectTime']), '%Y-%m-%d')
            outTime.append(date)
            temperature = data['temperature']
            Temperature.append(temperature)
            num = data['num']
            number.append(num)
            dataExcelList.append([data['collectTime'], temperature, num])
        lcbm = modelName.split("_")[0]
        kind = modelName.split("_")[1]


        if number.__len__() ==1:
            timeGap.append(0)
            outPut.append(number[0])
            trainData.append([timeGap[0], Temperature[0], 0])
        else:
            for i in range(number.__len__()-1):
                for j in range(i + 1, number.__len__()):
                    timeGap.append((outTime[j] - outTime[i]).days)
                    outPut.append(int(number[j] - number[i]))

            for i in range(number.__len__()-1):
                for j in range(i + 1, number.__len__()):
                    trainData.append([timeGap[count], Temperature[i], outPut[count]])
                    count = count + 1

        changeModelResult = change_model(danger, trainData, lcbm, kind)
        modelName = changeModelResult['obj']['modelName']
        savePrimaryFile(dataExcelList, lcbm, modelName)
        return changeModelResult


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address=('localhost', 12809),
    RequestHandlerClass=RequestHandler)
print "Starting HTTP server ..."
print "URL: http://localhost:12809"
http_server.serve_forever()

