from flask import jsonify
from . import bp
from .auth import token_auth


@bp.route('/test', methods=['GET'])
@token_auth.login_required
def test():
    return jsonify('It\'s a test message!')

