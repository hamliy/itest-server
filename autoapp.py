# encoding: utf-8
"""
@author: han.li
@file  : autoapp.py
@time  : 2018/8/15 10:14
@dec   : 启动入口
"""

from flask.helpers import get_debug_flag
from flask import request,jsonify
import flask
from itest.app import create_app
from itest.config import DevConfig, ProdConfig
from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required)

CONFIG = DevConfig  # if get_debug_flag() else ProdConfig
app = create_app(CONFIG)

_PORT = 8083
_HOST = '0.0.0.0'

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     if
@app.before_request
def before_request():
    if CONFIG.BEFORE_REQUEST:
        if '/login' not in flask.request.url:
            auth()


@jwt_required
def auth():
    pass


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'admin' or password != 'admin':
        return jsonify({"msg": "用户名或密码错误"})

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


if __name__ == '__main__':
   # init_db()
    app.run(port=_PORT, host=_HOST, debug=True, threaded=True, use_reloader=True)
