import re
from flask import request, jsonify, url_for, g, current_app
from . import bp
from .auth import token_auth
from .errors import bad_request, error_response
from ..models import User, Position, apply
from .. import db


@bp.route('/recruit/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user_recruit(id):
    pass


@bp.route('/recruit/<int:id>', methods=['POST'])
@token_auth.login_required
def create_recruit(id):
    pass


@bp.route('/recruit/<int:id>', methods=['DELETE'])
@token_auth.login_required
def cancel_recruit(id):
    pass
