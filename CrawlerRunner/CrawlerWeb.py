#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/5/6 21:06
# @Author : yingchao.wang
# @describe : 



from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/eleven", methods=['GET','POST'])
def snap():
    elevenData=request.headers.get("eleven")
    return "111"


@app.route("/myweb/getEleven", methods=['GET'])
def view():
    hotelId = request.args.to_dict().get('hotelId', "")
    return "{\"error\":\"\"}"



@app.errorhandler(404)
def page_not_found(e):
    return "{'error': 'URL有误，请检查后重新输入！'}"


@app.errorhandler(500)
def service_error(e):
    # log.error("服务器异常，当前请求url为【{url}】".format(url=request.url))
    return "{'error': '服务器异常！'}"

# if __name__ == '__main__':
#     app.run(port="8000")


