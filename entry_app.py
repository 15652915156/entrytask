#!/usr/local/bin/python3
from flask import Flask,abort,request,jsonify
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
import flask_restful

app=Flask(__name__)
api=Api(app)

class Code:
    SUCCESS_CODE = 0
    SYSTEM_ERRCODE = 11
    PARAMS_ERRCODE = 21

    msg = {
        SUCCESS_CODE: "success",
        SYSTEM_ERRCODE: "system error",
        PARAMS_ERRCODE: "empty or wrong params"
    }
    
def make_result(data="entrytest", code=Code.SUCCESS_CODE):
    return jsonify({"error_code": code,  "error_message": Code.msg[code],"reference":data})

#获取请求参数以及对参数合法性做校验
parser = RequestParser()
parser.add_argument("a", type=int, location="args", required=True)
parser.add_argument("b", type=str, location="args", required=True)

#使用get方法
class Test(Resource):
    def get(self):
        req = parser.parse_args(strict=True)
        a = req.get("a")
        b = req.get("b")
        return make_result(data="NO."+str(a)+" is "+b)
    
#获取参数   
api.add_resource(Test, "/shopee/test")

#参数错误码
def my_abort(http_status_code, *args, **kwargs):
    if http_status_code == 400:
       abort(make_result(code=Code.PARAMS_ERRCODE))

flask_restful.abort = my_abort

#系统错误码
@app.errorhandler(404)
def page_not_found(e):
    return (make_result(code=Code.SYSTEM_ERRCODE))

if __name__=="__main__":
    app.run(host='127.0.0.1',debug=True)
