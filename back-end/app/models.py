from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from flask import url_for, current_app

apply = db.Table(
    'apply',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('position_id', db.Integer, db.ForeignKey('positions.id')),
    db.Column('status', db.Integer, default=0)
    # 0-待审  1-初审    2-一面	3-二面	4-入职	-1-流程终止
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Integer, default=0)

    user_info = db.relationship('UserBaseInfo', uselist=False)
    user_edu_info = db.relationship('Education', backref=db.backref('users'))
    user_work_info = db.relationship('Work', backref=db.backref('users'))
    user_fam_info = db.relationship('Family', backref=db.backref('users'))

    position = db.relationship('Position',
                               secondary=apply,

                               backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def set_password(self, pw):
        # 保存用户密码为HASH值
        self.password = generate_password_hash(pw)

    def check_password(self, pw):
        # 验证用户密码
        return check_password_hash(self.password, pw)

    def to_dict(self):
        data = {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            '_links': {
                'self': url_for('api.get_user_base_info', id=self.id)
            }
        }
        return data

    def from_dict(self, data):
        pass

    def new_user(self, data):
        if 'email' in data:
            setattr(self, 'email', data['email'])
        if 'password' in data:
            self.set_password(data['password'])

    def get_jwt(self, exp_in=3600):
        # 发放jwt
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'user_name': self.user_info.name if self.user_info and self.user_info.name else self.email,
            'exp': now + timedelta(seconds=exp_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256')

    @staticmethod
    def verify_jwt(token):
        try:
            # 解码token验证是否有效，有效则返回对应用户
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
        except (jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.InvalidSignatureError,
                jwt.exceptions.DecodeError) as e:
            return None
        return User.query.get(payload.get('user_id'))


class UserBaseInfo(db.Model):
    __tablename__ = 'base_info'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    sex = db.Column(db.String(8), nullable=False)
    race = db.Column(db.String(16), nullable=False)
    id_number = db.Column(db.String(18), nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    address = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<Base Info {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'sex': self.sex,
            'race': self.race,
            'id_number': self.id_number,
            'phone_number': self.phone_number,
            'address': self.address
        }

        return data

    def from_dict(self, data):
        for field in ['name', 'sex', 'race', 'id_number', 'phone_number', 'address']:
            if field in data:
                setattr(self, field, data[field])


class Position(db.Model):
    __tablename__ = 'positions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    department = db.Column(db.String(64), nullable=False, index=True)
    location = db.Column(db.String(64), nullable=False, index=True)
    describe = db.Column(db.Text)
    requirement = db.Column(db.Text)

    def __repr__(self):
        return '<Position {}>'.format(self.name)

    def to_dict(self, detail=False):
        data = {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'location': self.location
        }
        if detail:
            data['describe'] = self.describe
            data['requirement'] = self.requirement

        return data

    def from_dict(self, data):
        for field in ['name', 'department', 'location', 'describe', 'requirement']:
            if field in data:
                setattr(self, field, data[field])



class Education(db.Model):
    __tablename__ = 'educations'
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(32), nullable=False)
    school = db.Column(db.String(32), nullable=False)
    major = db.Column(db.String(32), nullable=False)
    begin_date = db.Column(db.String(16), nullable=False)
    end_date = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Education {}>'.format(self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'degree': self.degree,
            'school': self.school,
            'major': self.major,
            'begin_date': self.begin_date,
            'end_date': self.end_date
        }
        return data

    def from_dict(self, data):
        for field in ['degree', 'school', 'major', 'begin_date', 'end_date']:
            if field in data:
                setattr(self, field, data[field])


class Work(db.Model):
    __tablename__ = 'works'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(32), nullable=False)
    position = db.Column(db.String(32), nullable=False)
    begin_date = db.Column(db.String(16), nullable=False)
    end_date = db.Column(db.String(16), nullable=False)
    describe = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Work {}>'.format(self.id)

    def to_dict(self):
        data = {
            'id': self.id,
            'company': self.company,
            'position': self.position,
            'describe': self.describe,
            'begin_date': self.begin_date,
            'end_date': self.end_date
        }
        return data

    def from_dict(self, data):
        for field in ['company', 'position', 'describe', 'begin_date', 'end_date']:
            if field in data:
                setattr(self, field, data[field])


class Family(db.Model):
    __tablename__ = 'families'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    work = db.Column(db.String(32))
    relation = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Family {}>'.format(self.name)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'work': self.work,
            'relation': self.relation,
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'phone_number', 'work', 'relation']:
            if field in data:
                setattr(self, field, data[field])
