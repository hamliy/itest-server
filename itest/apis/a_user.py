# encoding: utf-8
"""
@author: han.li
@file  : a_user.py
@time  : 11/12/18 4:47 PM
@dec   : 用户接口
"""

from flask import Blueprint, request
from itest.service.user.s_user import UserService
from itest.service.user.s_token import TokenService
from itest.utils.utils import init_return, md5
from itest.utils.decorators import init_params
from flask_jwt_extended import (create_access_token, get_raw_jwt, create_refresh_token, jwt_refresh_token_required, get_jwt_identity)


blueprint = Blueprint('users', __name__)


@blueprint.route('/search', methods=['POST'])
@init_params(params=['query'])
def search():
    info = request.get_json()
    data = UserService.find(info['query'])
    for item in data:
        item.pop('password')
    return init_return(data)


@blueprint.route('/create', methods=['POST'])
@init_params(params=['username', 'password', 'email'], empty_check=True)
def create():
    info = request.get_json()
    is_exist = UserService.get_by_email(info['email'])
    if is_exist:
        return init_return({}, sucess=False, error="此邮箱已被注册", errorCode=2001)

    data = UserService.create(info)
    data.pop('password')
    return init_return(data)


@blueprint.route('/login', methods=['POST'])
@init_params(params=['password', 'email'], empty_check=True)
def login():
    info = request.get_json()
    user = UserService.get_by_email(info['email'])
    if not user:
        return init_return({}, sucess=False, error="账号不存在", errorCode=2002)
    if user['password'] != md5(info['password']):
        return init_return({}, sucess=False, error="密码错误", errorCode=2003)
    user.pop('password')
    user['access_token'] = create_access_token(identity=user['id'])
    user['refresh_token'] = create_refresh_token(user['id'])
    user['access_token_exp'] = TokenService.get_token_exp(user['access_token'])
    user['refresh_token_exp'] = TokenService.get_token_exp(user['refresh_token'])

    TokenService.add_token_to_database(user['access_token'], 'identity')
    TokenService.add_token_to_database(user['refresh_token'], 'identity')

    return init_return(user)


@blueprint.route('/logout', methods=['POST'])
def logout():
    jti = get_raw_jwt()['jti']
    current_user = get_jwt_identity()
    TokenService.revoke_token(jti, current_user)
    return init_return({'logout': 'success'})


@blueprint.route('/logout/refreshToken', methods=['POST'])
@jwt_refresh_token_required
def refresh_logout():
    jti = get_raw_jwt()['jti']
    current_user = get_jwt_identity()
    TokenService.revoke_token(jti, current_user)
    return init_return({'logout-refreshToken': 'success'})


@blueprint.route('/refreshToken', methods=['POST'])
@jwt_refresh_token_required
def refresh_token():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    TokenService.add_token_to_database(new_token, 'identity')
    return init_return({'access_token': new_token})


@blueprint.route('/update/info', methods=['POST'])
@init_params(params=['id', 'email', 'username'], empty_check=True)
def update():
    info = request.get_json()
    rs = UserService.update(info)
    if not rs:
        return init_return({}, sucess=False, error="邮箱名重复，修改失败", errorCode=2004)
    rs.pop('password')
    return init_return(rs)


@blueprint.route('/update/password', methods=['POST'])
@init_params(params=['originPassword', 'password', 'verifyPassword'], empty_check=True)
def update_password():
    info = request.get_json()
    if info['password'] != info['verifyPassword']:
        return init_return({}, sucess=False, error="确认密码不一致", errorCode=2005)
    user_id = get_jwt_identity()
    rs = UserService.update_password_by_old_password(user_id, info['originPassword'], info['password'])
    if not rs:
        return init_return({}, sucess=False, error="修改失败", errorCode=2006)
    rs.pop('password')
    return init_return(rs)