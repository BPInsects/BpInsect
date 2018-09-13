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
from saveModel import find_model
import json

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
    def predict(self, lcbm,temperature,timeGap,kind):
        model = find_model(lcbm,kind)
        result = {
            "success":False,
            "msg":"",
            "obj":{}
        }
        if model == None:
            result.success = False;
            result.msg = "没有该虫种的粮仓模型，无法预测"
            return result
        else:
            #时间分割
            time = []
            num = []
            for i in range(timeGap//5):
                time.append(5*(i+1))
            if (timeGap%5) != 0:
                time.append(timeGap)

            for t in time:
                num.append(model.predict(temperature,t))

            obj = []
            for j in range(time.__len__()):
                obj[j][0]=time[j]
                obj[j][1] = num[j]

            result.success = True,
            result.obj = obj;
            return result;
        data ={
            'lcbm':lcbm,
            'temperature':temperature,
            'timeGap':timeGap,
            'num':20
        }
        print(lcbm)

        """Test method"""
        return data

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
