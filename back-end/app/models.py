from . import db
from werkzeug.security import generate_password_hash, check_password_hash


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
    user_edu_info = db.relationship('Education', backref=db.backref('users', lazy='dynamic'))
    user_work_info = db.relationship('Work', backref=db.backref('users', lazy='dynamic'))
    user_family_info = db.relationship('Family', backref=db.backref('users', lazy='dynamic'))

    position = db.relationship('Position',
                               secondary=apply,

                               backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.id)


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


class Family(db.Model):
    __tablename__ = 'families'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    phone_number = db.Column(db.String(16), nullable=False)
    work = db.Column(db.String(32), nullable=False)
    relation = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Work {}>'.format(self.name)
