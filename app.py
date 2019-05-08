from gevent.pywsgi import WSGIServer
from gevent import monkey
from flask import Flask, request, jsonify
from scrapy.http import Request

monkey.patch_all()
app = Flask(__name__)


# @app.route("/spider", methods=['GET','POST'])
# def snap():
#     elevenData=request.headers.get("eleven")
#     return "111"


@app.route("/spider", methods=['GET'])
def view():
    hotelId = request.args.to_dict().get('hotelId', "")
    return jsonify({"hotelId":hotelId})



@app.errorhandler(404)
def page_not_found(e):
    return "{'error': 'URL有误，请检查后重新输入！'}"


@app.errorhandler(500)
def service_error(e):
    # log.error("服务器异常，当前请求url为【{url}】".format(url=request.url))
    return "{'error': '服务器异常！'}"


if __name__ == '__main__':
    WSGIServer(('0.0.0.0',8000), app).serve_forever()