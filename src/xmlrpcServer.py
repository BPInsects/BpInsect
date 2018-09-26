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
from modelManage import find_model,change_model,save_model,load_model
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
        results = {
            "success": True,
            "msg": "",
            "obj": []
        }

        dataList = json.loads(hello)
        if dataList != None:
            i = 0
            for data in dataList:
               results.obj[i] = RequestHandler.predict(data.lcbm,data.kind)
        else:
            results.success = False
            results.msg = "没有找到模型"

        return results

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
    def sureChangeModel(self,name,sure):
        if sure == True:
            Name = name
            Name.split("_")[2] = 'b'
            save_model(load_model(name),modelFileName+'/'+Name)
            os.remove(modelFileName+'/'+name)
        else:
            os.remove(modelFileName + '/' + name )


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
                "results": []
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
