# coding=utf-8
# from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
#
# server = SimpleJSONRPCServer(('localhost', 8080))
# server.register_function(pow)
# server.register_function(lambda x,y: x+y, 'add')
# server.register_function(lambda x: x, 'ping')
# server.serve_forever()



import pyjsonrpc
import numpy as np
from modelManage import find_model,change_model,save_model,load_model,find_model1
import json
import commonVariables
import os
from sklearn import preprocessing

modelFileName = commonVariables.modelFileName
trainFileName = commonVariables.trainFileName


class RequestHandler(pyjsonrpc.HttpRequestHandler):

    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        """Test method"""
        return a + b
    # TODO 增加查询和预测方法
    @pyjsonrpc.rpcmethod
    def allpredict(self,hello):
        results = {
            "success": True,
            "msg": "",
            "obj": []
        }

        dataList = json.loads(hello)
        if dataList!= None:
            for data in dataList:
               results['obj'].append(RequestHandler.predict(data['lcbm'],data['temperature'],data['timeGap'],data['kind']))
        else:
            results['success'] = False
            results['msg'] = "没有找到模型"

        return results

    @pyjsonrpc.rpcmethod
    def readModelListByKind(self,lcbm,kind):
        return find_model1(lcbm,kind)

    @pyjsonrpc.rpcmethod
    def readModelListByLcbm(self,lcbm):
        value = find_model(lcbm)
        return value

    @pyjsonrpc.rpcmethod
    def changeModel(self,f,dataList,lcbm,kind):
        return change_model(f,dataList,lcbm,kind)

    @pyjsonrpc.rpcmethod
    def sureChangeModel(self,name,sure):
        if sure == True:
            Name = name
            Name.split("_")[2] = 'b'
            save_model(load_model(name),Name)
            os.remove(modelFileName+'/'+name)
        else:
            os.remove(modelFileName + '/' + name )


    @pyjsonrpc.rpcmethod
    def predict(self, lcbm,temperature,timeGap,kind):

        modelList = find_model1(lcbm, kind)
        if modelList['obj'].__len__() == 1:
            preModel = modelList['obj'][0]
        else:
            for model in modelList['obj']:
                if model['type'] == 'b':
                    preModel = model

        f = preModel['danger']
        model = load_model(preModel['modelName'])
        result = {
            "success": False,
            "msg": "",
            "obj": [{
                "kind": kind,
                "temperature": temperature,
                "lcbm": lcbm,
                "danger": f,
                "results": []
            }]

        }
        if model == None:
            result['success'] = False;
            result['msg'] = "没有该虫种的粮仓模型，无法预测"
            return result
        else:

            num = []
            x_test = []

            for t in range(1,timeGap+1):
                x_test.append([temperature,t])

            num = model.predict(preprocessing.scale(x_test))
            print(num)
            result['success'] = True
            result['msg'] = "成功预测"

            for i in range(1,timeGap+1):
                result['obj'][0]['results'].append( {
                    "timeGap": i,
                    "num": int(num[i-1])
                })

        return result;




# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 12809),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:12809"
http_server.serve_forever()
