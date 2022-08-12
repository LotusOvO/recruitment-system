import sys
import os
sys.path.append(os.getcwd())
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import TimedRotatingFileHandler
from config import Config
from app.extensions import mail

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # 日志
    formatter = logging.Formatter(
        "[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler(
        "flask.log", when="D", interval=1, backupCount=15,
        encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    # 注册blueprint
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from . import models

    return app
