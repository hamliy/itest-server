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
from itest import environment, invoice, user, base, test_data
from itest.apis import a_user, a_project, a_image, a_image_group, a_mark_field, a_environment,\
    a_interface, a_interface_history, a_interface_group, a_interface_use_case_group,\
    a_interface_use_case_history, a_interface_use_case
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
    register_api_blueprints(app)
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
    app.register_blueprint(test_data.test_data_apis.blueprint, url_prefix='/api/data')
    return None


def register_api_blueprints(app):
    app.register_blueprint(a_user.blueprint, url_prefix='/api/users')
    app.register_blueprint(a_project.blueprint, url_prefix='/api/projects')
    app.register_blueprint(a_image.blueprint, url_prefix='/api/images')
    app.register_blueprint(a_image_group.blueprint, url_prefix='/api/images-group')
    app.register_blueprint(a_mark_field.blueprint, url_prefix='/api/mark-field')
    app.register_blueprint(a_environment.blueprint, url_prefix='/api/envs')
    app.register_blueprint(a_interface.blueprint, url_prefix='/api/interfaces')
    app.register_blueprint(a_interface_group.blueprint, url_prefix='/api/interface-group')
    app.register_blueprint(a_interface_history.blueprint, url_prefix='/api/interface-history')
    app.register_blueprint(a_interface_use_case.blueprint, url_prefix='/api/interface-use-case')
    app.register_blueprint(a_interface_use_case_group.blueprint, url_prefix='/api/interface-use-case-group')
    app.register_blueprint(a_interface_use_case_history.blueprint, url_prefix='/api/interface-use-case-history')
    return None


# def register_api():
#     from environment.apis.api import ns as env_api
#     environment.apis.api.add_namespace(env_api)

def register_extensions(app):
    """Register Flask extensions."""
    cors.init_app(app)
    jwt.init_app(app)
    init_mongo(app)




