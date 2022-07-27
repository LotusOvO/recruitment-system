from flask import g, jsonify
from . import bp
from .auth import basic_auth


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_jwt()
    return jsonify({'token': token})
