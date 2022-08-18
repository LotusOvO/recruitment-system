import sys
import os
sys.path.append(os.getcwd())
from flask import request, jsonify, url_for, g, current_app
from sqlalchemy import and_, func
from app.api import bp
from app.api.auth import token_auth, verify_admin
from app.api.errors import bad_request, error_response
from app.models import User, Position
from app import db


@bp.route('recruitment', methods=['GET'])
def get_recruitments():
    return jsonify([position.to_dict() for position in Position.query])


@bp.route('recruitment/department', methods=['GET'])
def get_recruitments_by_department():
    data = {}
    departments = db.session.query(Position.department).group_by(Position.department)
    for dp in departments.all():
        dp = dp[0]
        data[dp] = []
        for item in Position.query.filter(Position.department == dp).all():
            data[dp].append(item.to_dict())
    return jsonify(data)


@bp.route('recruitment/<int:id>', methods=['GET'])
@token_auth.login_required
def get_recruitment(id):
    position = Position.query.get_or_404(id)
    return jsonify(position.to_dict(detail=True))


@bp.route('recruitment', methods=['POST'])
@token_auth.login_required
def create_recruitment():
    # 验证是否为管理员
    if not verify_admin():
        return bad_request('没有该权限')

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
    if not verify_admin():
        return bad_request('没有该权限')
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
    if not verify_admin():
        return bad_request('没有该权限')
    position = Position.query.get_or_404(id)

    db.session.delete(position)
    db.session.commit()

    return jsonify([position.to_dict() for position in Position.query])


@bp.route('recruitment/search', methods=['GET'])
def search_recruitment():
    name = request.args.get('name', "")
    department = request.args.get('department', "")
    location = request.args.get('location', "")
    positions = Position.query.filter(
        and_(Position.name.like('%{}%'.format(name)),
             Position.location.like('%{}%'.format(location)),
             Position.department.like('%{}%'.format(department)))).all()

    return jsonify([position.to_dict() for position in positions])
