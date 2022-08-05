from flask import Blueprint

bp = Blueprint('api', __name__)

from ..api import \
    test, auth, base_info, \
    errors, tokens, users, \
    edu_info, work_info, fam_info, \
    recruitment, recruit
