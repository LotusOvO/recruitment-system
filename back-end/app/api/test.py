from flask import jsonify
from . import bp


@bp.route('/test', methods=['GET'])
def test():
    return jsonify('It\'s a test message!')
