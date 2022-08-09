import sys
import os
sys.path.append(os.getcwd())
from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth, verify_admin
from app.api.errors import bad_request, error_response
from app.models import User, Family
from app import db


@bp.route('fam_info/<int:id>', methods=['GET'])
@token_auth.login_required
def get_fam_info(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id and not verify_admin():
        return error_response(403)
    fam_info = user.user_fam_info
    return jsonify([info.to_dict() for info in fam_info])


@bp.route('fam_info/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_fam_info(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}

    for field in ['id', 'name', 'phone_number', 'relation']:
        if field not in data or not data[field]:
            message[field] = '请提供{}信息'.format(field)

    if message:
        return bad_request(message)

    fam_info = user.user_fam_info
    for info in fam_info:
        if info.id == int(data['id']):
            # 对指定id的家属信息进行修改
            info.from_dict(data)
            db.session.commit()
            return jsonify([info.to_dict() for info in fam_info])

    # 找不到该id对应的家属信息
    message['id'] = '请提供正确的id信息'
    return bad_request(message)


@bp.route('fam_info/<int:id>', methods=['POST'])
@token_auth.login_required
def create_fam_info(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}

    for field in ['name', 'phone_number', 'relation']:
        if field not in data or not data[field]:
            message[field] = '请提供{}信息'.format(field)

    # 新建一个家属信息
    info = Family()
    setattr(info, 'user_id', id)
    info.from_dict(data)
    db.session.add(info)
    db.session.commit()

    fam_info = user.user_fam_info
    return jsonify([info.to_dict() for info in fam_info])


@bp.route('/fam_info/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_fam_info(id):
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

    fam_info = user.user_fam_info
    for info in fam_info:
        if info.id == int(data['id']):
            db.session.delete(info)
            db.session.commit()
            return jsonify([info.to_dict() for info in user.user_fam_info])

    message['id'] = '请提供正确的id信息'
    bad_request(message)
