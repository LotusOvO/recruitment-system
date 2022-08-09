import sys
import os
sys.path.append(os.getcwd())
from app import create_app, db
from app.models import User
from flask import make_response

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


# @app.after_request
# def atq(resp):
#     resp = make_response(resp)
#     resp.headers['Access-Control-Allow_Origin'] = '*'
#     resp.headers['Access-Control-Allow_Methods'] = 'GET,POST,PUT,DELETE'
#     resp.headers['Access-Control-Allow_Headers'] = 'x-requested-with,content-type'
#     return resp
