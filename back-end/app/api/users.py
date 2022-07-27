import re
from flask import request, jsonify, url_for, g, current_app
from . import bp
from .auth import token_auth
from .errors import bad_request, error_response
from ..models import User
from .. import db


@bp.route('/users', methods=['POST'])
def create_user():
    # 注册新用户
    data = request.get_json()
    if not data:
        return bad_request('需要提供JSON数据')

    message = {}
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = '请提供一个有效的邮箱'
    if 'password' not in data or not data.get('password', None).strip():
        message['password'] = '请提供一个有效的密码'

    # 判断重复
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = '该邮箱已经注册过'
    if message:
        return bad_request(message)

    # 根据邮箱判断是否为管理员
    #
    # 待完成

    user = User()
    user.new_user(data)
    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user_base_info', id=user.id)
    return response
