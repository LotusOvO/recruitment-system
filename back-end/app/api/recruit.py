import sys
import os
sys.path.append(os.getcwd())
from flask import request, jsonify, url_for, g, current_app
from app.api import bp
from app.api.auth import token_auth, verify_admin
from app.api.errors import bad_request, error_response
from app.models import User, Position, apply, UserBaseInfo
from app import db


@bp.route('/recruit/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user_recruit(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id and not verify_admin():
        return error_response(403)
    positions = user.position
    return jsonify([position.to_dict(user=user) for position in positions])


@bp.route('/recruit/<int:id>', methods=['POST'])
@token_auth.login_required
def create_recruit(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}
    if 'position_id' not in data:
        message['position_id'] = '请提供id数据'
    if message:
        bad_request(message)
    position = Position.query.get_or_404(data['position_id'])

    if user.is_apply(position):
        return bad_request('已经应聘该岗位')
    user.position.append(position)
    db.session.commit()
    return jsonify([position.to_dict(user=user) for position in user.position])


@bp.route('/recruit/<int:id>', methods=['DELETE'])
@token_auth.login_required
def cancel_recruit(id):
    user = User.query.get_or_404(id)
    if g.current_user.id != id:
        return error_response(403)
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}
    if 'position_id' not in data:
        message['position_id'] = '请提供id数据'
    if message:
        bad_request(message)
    position = Position.query.get_or_404(data['position_id'])

    if not user.is_apply(position):
        return bad_request('没有应聘该岗位')

    user.position.remove(position)
    db.session.commit()
    return jsonify([position.to_dict(user=user) for position in user.position])


@bp.route('/recruit/advance', methods=['PUT'])
@token_auth.login_required
def apply_advance():
    # 验证是否为管理员
    if not verify_admin():
        return bad_request('没有该权限')
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}
    if 'user_id' not in data:
        message['user_id'] = '请提供user_id数据'
    if 'position_id' not in data:
        message['position_id'] = '请提供position_id数据'
    if message:
        bad_request(message)

    user = User.query.get_or_404(data['user_id'])
    user_info = UserBaseInfo.query.get_or_404(data['user_id'])
    position = Position.query.get_or_404(data['position_id'])
    result = position.to_dict(user=user)
    if result['status'] == -1:
        return bad_request('该招聘流程已终止')
    elif result['status'] == 4:
        return bad_request('该招聘流程已完成')

    position.change_status(user=user, status=result['status'] + 1)
    current_app.logger.info("管理员{}将用户{}与职位{}的招聘流程操作到下一阶段".format(g.current_user.id, data['user_id'],
                                                                 data['position_id']))
    response = {
        'user': user_info.to_dict(detail=False),
        'position': position.to_dict(user=user)
    }
    return jsonify(response)


@bp.route('/recruit/refuse', methods=['PUT'])
@token_auth.login_required
def apply_refuse():
    # 验证是否为管理员
    if not verify_admin():
        return bad_request('没有该权限')
    data = request.get_json()
    if not data:
        return bad_request('必须提供JSON数据')

    message = {}
    if 'user_id' not in data:
        message['user_id'] = '请提供user_id数据'
    if 'position_id' not in data:
        message['position_id'] = '请提供position_id数据'
    if message:
        bad_request(message)

    user = User.query.get_or_404(data['user_id'])
    user_info = UserBaseInfo.query.get_or_404(data['user_id'])
    position = Position.query.get_or_404(data['position_id'])
    result = position.to_dict(user=user)
    if result['status'] == -1:
        return bad_request('该招聘流程已终止')
    elif result['status'] == 4:
        return bad_request('该招聘流程已完成')

    position.change_status(user=user, status=-1)
    current_app.logger.info("管理员{}将用户{}与职位{}的招聘流程操作结束".format(g.current_user.id, data['user_id'],
                                                              data['position_id']))
    response = {
        'user': user_info.to_dict(detail=False),
        'position': position.to_dict(user=user)
    }
    return jsonify(response)


@bp.route('/recruit/search', methods=['GET'])
@token_auth.login_required
def search_recruit():
    # 验证是否为管理员
    if not verify_admin():
        return bad_request('没有该权限')
    user_name = request.args.get('user_name', '')
    position_name = request.args.get('position_name', '')
    users = [user for user in UserBaseInfo.query.filter(UserBaseInfo.name.like('%{}%'.format(user_name)))]
    users = [user.users for user in users]
    result = []
    for user in users:  # type:User
        positions = [position for position in user.position if position_name in position.name]
        for position in positions:
            position_data = position.to_dict(user=user)  # type: dict
            user_data = user.user_info.to_dict(detail=False)
            data = {
                'position': position_data,
                'user': user_data
            }
            result.append(data)

    return jsonify(result)


@bp.route('/recruit/status', methods=['GET'])
@token_auth.login_required
def search_recruit_by_id_and_status():
    # 验证是否为管理员
    if not verify_admin():
        return bad_request('没有该权限')
    position_id = request.args.get('position_id', '')
    status = request.args.get('status', '')
    if position_id == '' and status == '':
        result = db.session.execute(
            "select * from apply"
        )
    elif position_id != '' and status == '':
        result = db.session.execute(
            "select * from apply where position_id={}".format(position_id)
        )
    elif status != '' and position_id == '':
        result = db.session.execute(
            "select * from apply where status={}".format(status)
        )
    else:
        result = db.session.execute(
            "select * from apply where position_id={} and status={}".format(position_id, status)
        )
    data = []
    for item in result.all():
        user = User.query.get_or_404(item[0])
        position = Position.query.get_or_404(item[1])
        position_data = position.to_dict(user=user)  # type: dict
        user_data = user.user_info.to_dict(detail=False)
        data.append({
            'position': position_data,
            'user': user_data
        })
    return jsonify(data)
