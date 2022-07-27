import re
from flask import request, jsonify, url_for, g, current_app
from . import bp
from .auth import token_auth
from .errors import bad_request, error_response
from ..models import User, UserBaseInfo
from .. import db


@bp.route('/base_info/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user_base_info(id):
    user = User.query.get_or_404(id)
    if user.user_info:
        return jsonify(user.user_info.to_dict())
    else:
        return jsonify({'id': id})


@bp.route('/base_info/<int:id>', methods=['POST'])
@token_auth.login_required
def update_user_base_info(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    if not data:
        return bad_request("必须提供JSON数据")

    message = {}
    for field in ['name', 'sex', 'race', 'id_number', 'phone_number', 'address']:
        if field not in data or not data[field]:
            message[field] = '请提供{}信息'.format(field)

    if message:
        return bad_request(message)

    if user.user_info:
        user.user_info.from_dict(data)
    else:
        user_info = UserBaseInfo()
        setattr(user_info, 'id', id)
        user_info.from_dict(data)

    db.session.commit()
    return jsonify(user.user_info.to_dict())
