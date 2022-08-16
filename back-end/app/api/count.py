import sys
import os

sys.path.append(os.getcwd())
from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth, verify_admin
from app.api.errors import bad_request, error_response
from app.models import User, Position, apply
from app import db
from sqlalchemy import func


@bp.route('/count/position/<int:id>', methods=['GET'])
@token_auth.login_required
def count_position(id):
    # 验证是否为管理员
    if not verify_admin():
        return bad_request('没有该权限')
    position = Position.query.get_or_404(id)
    count = db.session.execute(
        "select status,count(*) from (select * from apply where position_id = {}) as a group by status".format(id))
    data = {}
    for status in [0, 1, 2, 3, 4, -1]:
        data[status] = 0
    for temp in count.all():
        data[temp[0]] = temp[1]
    return jsonify(data)


@bp.route('/count/positions/<int:sum>', methods=['GET'])
@token_auth.login_required
def count_positions(sum):
    # 验证是否为管理员
    if not verify_admin():
        return bad_request('没有该权限')
    if sum <= 0:
        sum = 1
    if sum > 20:
        sum = 20
    count = db.session.execute(
        "select a.name,a.id,b.number "
        "from positions as a,(select position_id,count(*) as number from apply group by position_id) as b "
        "where b.position_id = a.id order by b.number desc limit {}".format(sum)
    )
    data = {}
    i = 1
    for temp in count.all():
        data[i] = {
            'name': temp[0],
            'id': temp[1],
            'number': temp[2]
        }
        i += 1
    return jsonify(data)


@bp.route('/count/status/<int:status>', methods=['GET'])
@token_auth.login_required
def count_status(status):
    # 验证是否为管理员
    if not verify_admin():
        return bad_request('没有该权限')
    if status not in [-1, 0, 1, 2, 3, 4]:
        return bad_request('没有该状态')
    count = db.session.execute(
        "select status,count(*) from apply where status={} group by status".format(status)
    )
    data = {}
    temp = count.all()
    if len(temp) > 0:
        data[temp[0][0]] = temp[0][1]
    else:
        data[status] = 0
    return jsonify(data)
