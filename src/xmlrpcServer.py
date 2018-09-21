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
import saveModel as mu
from modelManage import find_model,change_model,save_model,load_model
from saveModel import find_model
import json
import commonVariables
import os

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
        dataList = json.loads(hello)
        for data in dataList:
           print(data)
        print(hello)
        return dataList

    @pyjsonrpc.rpcmethod
    def readModelListByKind(self,lcbm,kind):
        return find_model(lcbm,kind)

    @pyjsonrpc.rpcmethod
    def readModelListByLcbm(self,lcbm):
        return find_model(lcbm)

    @pyjsonrpc.rpcmethod
    def changeModel(self,f,dataList,lcbm,kind):
        return change_model(f,dataList,lcbm,kind)

    @pyjsonrpc.rpcmethod
    def sureChangeModel(self,name):
        Name = name
        Name[10] = 'b'
        save_model(load_model(name),modelFileName+'/'+Name)
        os.remove(modelFileName+'/'+name+'.md')

    @pyjsonrpc.rpcmethod
    def cancelChangeModel(self,name):
        os.remove(modelFileName + '/' + name + '.md')


    @pyjsonrpc.rpcmethod
    def predict(self, lcbm,temperature,timeGap,kind):
        modelName = find_model(lcbm,kind)
        f = int(modelName[-7])
        model = load_model(modelName)
        result = {
            "success": True,
            "msg": "",
            "obj": {
                "kind": kind,
                "temperature": temperature,
                "lcbm": lcbm,
                "danger": f,
                "results": [{
                    "timeGap": 1,
                    "num": 20
                }, {
                    "timeGap": 2,
                    "num": 40
                }, {
                    "timeGap": 3,
                    "num": 60
                }, {
                    "timeGap": 4,
                    "num": 70
                }]
            }

        }
        if model == None:
            result.success = False;
            result.msg = "没有该虫种的粮仓模型，无法预测"
            return result
        else:

            num = []

            for t in timeGap:
                num.append(model.predict(temperature,t))

            result.success = True,
            result.msg = "成功预测"

            for i in range(1,timeGap+1):
                result.obj.results[i-1] = {
                    "timeGap": i,
                    "num": num[i-1]
                }

        return result;


    @pyjsonrpc.rpcmethod
    def test(self, t,h,m,gt,gh,at,ah):

        data = [[t,h,m,gt,gh,at,ah]]
        data = np.array(data)
        model = mu.load_model()
        result = model.predict(data).tolist()[0]

        print(result)
        return result


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8081),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8081"
http_server.serve_forever()
