import re
from flask import request, jsonify, url_for, g, current_app
from sqlalchemy import and_
from . import bp
from .auth import token_auth, verify_admin
from .errors import bad_request, error_response
from ..models import User, Position
from .. import db


@bp.route('recruitment', methods=['GET'])
def get_recruitments():
    return jsonify([position.to_dict() for position in Position.query])


@bp.route('recruitment/<int:id>', methods=['GET'])
@token_auth.login_required
def get_recruitment(id):
    position = Position.query.get_or_404(id)
    return jsonify(position.to_dict(detail=True))


@bp.route('recruitment', methods=['POST'])
@token_auth.login_required
def create_recruitment():
    # 验证是否为管理员
    # if not verify_admin():
    #     return bad_request('没有该权限')

    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}

    for field in ['name', 'department', 'location']:
        if field not in data or not data[field]:
            message[field] = '请提供{}信息'.format(field)

    if message:
        bad_request(message)

    # 新增招聘信息
    position = Position()
    position.from_dict(data)
    db.session.add(position)
    db.session.commit()

    # 返回招聘信息集合
    return jsonify([position.to_dict() for position in Position.query])


@bp.route('recruitment/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_recruitment(id):
    # 验证是否为管理员
    # if not verify_admin():
    #     return bad_request('没有该权限')
    position = Position.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}

    for field in ['name', 'department', 'location']:
        if field not in data or not data[field]:
            message[field] = '请提供{}信息'.format(field)

    if message:
        bad_request(message)

    position.from_dict(data)
    db.session.commit()

    return jsonify(position.to_dict(detail=True))


@bp.route('recruitment/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_recruitment(id):
    # 验证是否为管理员
    # if not verify_admin():
    #     return bad_request('没有该权限')
    position = Position.query.get_or_404(id)

    db.session.delete(position)
    db.session.commit()

    return jsonify([position.to_dict() for position in Position.query])


@bp.route('recruitment/search', methods=['GET'])
def search_recruitment():
    name = request.args.get('name', None)
    location = request.args.get('location', None)
    positions = Position.query.filter(
        and_(Position.name.like('%{}%'.format(name)), Position.location.like('%{}%'.format(location)))).all()

    return jsonify([position.to_dict() for position in positions])
