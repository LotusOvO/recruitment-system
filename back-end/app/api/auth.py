import sys
import os
sys.path.append(os.getcwd())
from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.api.errors import error_response
from app import db
from app.models import User

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    g.current_user = User.verify_jwt(token) if token else None
    # if g.current_user:
    #     db.session.commit()
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    return error_response(401)


def verify_admin():
    if g.current_user:
        return g.current_user.role == 1
    else:
        return False
