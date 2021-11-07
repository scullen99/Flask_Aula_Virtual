from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = None

def init_db(app):
    global db
    if db == None:
        db = SQLAlchemy(app) # class db extends app
    return db

def get_db():
    global db
    if db == None:
        from application import get_app
        app = get_app()
        db = init_db(app)
    return db

from application import get_app
app = get_app()
db = init_db(app)

class User(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50),unique=True)
    username = db.Column(db.String(15),unique=True)
    password = db.Column(db.String(80))
    profile = db.Column(db.String(10),default='student') # 'admin', 'staff', 'professor', 'student'
    confirmed = db.Column(db.Boolean(),default=False)
    userhash = db.Column(db.String(50))
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())
    course = db.relationship('Course', backref='user', lazy=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')



class Course(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    institution_name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    code = db.Column(db.String(50),unique=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())
    follow = db.relationship('Follow', backref='course', lazy=True)

class Follow(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_name = db.Column(db.String(50))
    course_code = db.Column(db.String(50))
    institution_name = db.Column(db.String(50))
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())


class ParticipationCode(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    code_description = db.Column(db.String(120))
    code_type = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_name = db.Column(db.String(50))
    institution_name = db.Column(db.String(50))
    date_expire = db.Column(db.DateTime)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

class ParticipationRedeem(UserMixin,db.Model): # User extends db.Model
    id = db.Column(db.Integer, primary_key=True)
    participation_code = db.Column(db.String(50))
    code_description = db.Column(db.String(120))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_name = db.Column(db.String(50))
    institution_name = db.Column(db.String(50))
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(15))
    hidden =  db.Column(db.Boolean, unique=False, default=False)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.Text)
    descripcion = db.Column(db.Text)
    date_expire = db.Column(db.DateTime)

class Entrega(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.LargeBinary)
    name = db.Column(db.String(100))
    nota = db.Column(db.Float, nullable=True)
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                       onupdate=db.func.current_timestamp())
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)












