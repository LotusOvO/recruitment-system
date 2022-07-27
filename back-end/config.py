import os
from dotenv import load_dotenv
import pymysql
pymysql.install_as_MySQLdb()

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'), encoding='utf-8')


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:12345689@127.0.0.1:3306/rec_sys'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
