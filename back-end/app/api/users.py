import sys
import os
sys.path.append(os.getcwd())
import re
from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, error_response
from app.models import User
from app import db
from utils import mail


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

    if user.role == 1:
        user.confirmed = True
        db.session.commit()
    else:
        token = user.generate_confirm_jwt()
        if not data.get('confirm_email_base_url'):
            confirm_url = 'http://127.0.0.1:5000/api/confirm/' + token
        else:
            confirm_url = data.get('confirm_email_base_url') + token

        text_body = '''
            欢迎注册中国电信中山分公司人员招聘系统！
            点击链接完成账户激活：{}
            注意: 不要回复该邮件。
            '''.format(confirm_url)

        html_body = '''
            <p>欢迎注册<b>中国电信中山分公司人员招聘系统</b>！</p>
            <p>请点击该链接完成账户验证 <a href="{0}">点击这里</a>。</p>
            <p>如果打不开可以复制链接到浏览器窗口打开。</p>
            <p><b>{0}</b></p>
            <p><small>注意: 不要回复该邮件。</small></p>
            '''.format(confirm_url)

        mail.send_email('[中国电信中山分公司] 邮箱验证',
                        sender=current_app.config['MAIL_SENDER'],
                        recipients=[user.email],
                        text_body=text_body,
                        html_body=html_body)

    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user_base_info', id=user.id)
    return response


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': '该用户已注销'})


@bp.route('/confirm/<token>', methods=['GET'])
@token_auth.login_required
def verity_confirm(token):
    if g.current_user.confirmed:
        return bad_request('你已经完成邮箱验证')
    if g.current_user.verity_confirm_jwt(token):
        db.session.commit()
        token = g.current_user.get_jwt()
        return jsonify({
            'status': 'success',
            'message': '已成功验证邮箱。',
            'token': token
        })
    else:
        return bad_request('该链接无效或已超时。')


@bp.route('/confirm/<id>', methods=['POST'])
@token_auth.login_required
def send_confirm(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    if g.current_user.confirmed:
        return bad_request('你已经完成邮箱验证')

    data = request.get_json()
    if not data:
        return bad_request('需要提供JSON数据')
    token = user.generate_confirm_jwt()
    if not data.get('confirm_email_base_url'):
        confirm_url = 'http://127.0.0.1:5000/api/confirm/' + token
    else:
        confirm_url = data.get('confirm_email_base_url') + token

    text_body = '''
                欢迎注册中国电信中山分公司人员招聘系统！
                点击链接完成账户激活：{}
                注意: 不要回复该邮件。
                '''.format(confirm_url)

    html_body = '''
                <p>欢迎注册<b>中国电信中山分公司人员招聘系统</b>！</p>
                <p>请点击该链接完成账户验证 <a href="{0}">点击这里</a>。</p>
                <p>如果打不开可以复制链接到浏览器窗口打开。</p>
                <p><b>{0}</b></p>
                <p><small>注意: 不要回复该邮件。</small></p>
                '''.format(confirm_url)

    mail.send_email('[中国电信中山分公司] 邮箱验证',
                    sender=current_app.config['MAIL_SENDER'],
                    recipients=[user.email],
                    text_body=text_body,
                    html_body=html_body)

    return jsonify({'message': "已发送邮件"})
