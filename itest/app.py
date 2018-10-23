# encoding: utf-8
"""
@author: han.li
@file  : server.py.py
@time  : 2018/8/15 14:39
@dec   : 服务配置及初始化
"""
from flask import Flask, jsonify, Response
from itest.config import DevConfig
from itest.extensions import cors, init_mongo, jwt
from itest import environment, invoice, user, base

#
#
class MyResponse(Response):
    """
    自定义响应结果
    结果对象json化
    """
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, dict):
            response = jsonify(response)
        return super(MyResponse, cls).force_type(response, environ)


def create_app(config_object=DevConfig):
    """An application factory,
    :param config_object: The configuration object to use.
    """

    app = Flask(__name__.split('.')[0])
    app.response_class = MyResponse
    app.config.from_object(config_object)
    # 注册扩展组件
    register_extensions(app)
    # 注册蓝图
    register_blueprints(app)
    # 注册api 别名- api接口文档
    # register_api()
    return app


def register_blueprints(app):
    app.register_blueprint(environment.apis.blueprint, url_prefix='/api/env')
    app.register_blueprint(invoice.apis.blueprint, url_prefix='/api/invoice')
    app.register_blueprint(user.apis.blueprint, url_prefix='/api/user')
    app.register_blueprint(base.project_apis.blueprint, url_prefix='/api/project')
    app.register_blueprint(base.environment_apis.blueprint, url_prefix='/api/environment')
    app.register_blueprint(base.task_apis.blueprint, url_prefix='/api/task')
    app.register_blueprint(base.interface_apis.blueprint, url_prefix='/api/interface')
    app.register_blueprint(base.use_case_apis.blueprint, url_prefix='/api/usecase')
    return None


# def register_api():
#     from environment.apis.api import ns as env_api
#     environment.apis.api.add_namespace(env_api)

def register_extensions(app):
    """Register Flask extensions."""
    cors.init_app(app)
    jwt.init_app(app)
    init_mongo(app)




