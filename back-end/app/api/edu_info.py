import re
from flask import request, jsonify, url_for, g, current_app
from . import bp
from .auth import token_auth
from .errors import bad_request, error_response
from ..models import User, Education
from .. import db


@bp.route('/edu_info/<int:id>', methods=['GET'])
@token_auth.login_required
def get_edu_info(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    edu_info = user.user_edu_info
    return jsonify([info.to_dict() for info in edu_info])


@bp.route('/edu_info/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_edu_info(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}

    for field in ['id', 'degree', 'school', 'major', 'begin_date', 'end_date']:
        if field not in data or not data[field]:
            message[field] = '请提供{}信息'.format(field)

    if message:
        return bad_request(message)

    edu_info = user.user_edu_info
    for info in edu_info:
        if info.id == int(data['id']):
            # 对指定id的教育信息进行修改
            info.from_dict(data)
            db.session.commit()
            return jsonify([info.to_dict() for info in edu_info])

    # 找不到该id对应的教育信息
    message['id'] = '请提供正确的id信息'
    return bad_request(message)


@bp.route('/edu_info/<int:id>', methods=['POST'])
@token_auth.login_required
def create_edu_info(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}

    for field in ['degree', 'school', 'major', 'begin_date', 'end_date']:
        if field not in data or not data[field]:
            message[field] = '请提供{}信息'.format(field)

    # 新建一个教育信息
    info = Education()
    setattr(info, 'user_id', id)
    info.from_dict(data)
    db.session.add(info)
    db.session.commit()

    edu_info = user.user_edu_info
    return jsonify([info.to_dict() for info in edu_info])


@bp.route('/edu_info/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_edu_info(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}
    if 'id' not in data:
        message['id'] = '请提供id数据'

    if message:
        bad_request(message)

    edu_info = user.user_edu_info
    for info in edu_info:
        if info.id == int(data['id']):
            db.session.delete(info)
            db.session.commit()
            return jsonify([info.to_dict() for info in user.user_edu_info])

    message['id'] = '请提供正确的id信息'
    bad_request(message)
