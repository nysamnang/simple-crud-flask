from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.Unicode())
    password = db.Column('password', db.Unicode())
    creation_date = db.Column('creation_date', db.Date, default=datetime.utcnow)
    active = db.Column('active', db.Boolean(), default=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated():
        return True

    def is_active():
        return True
        
    def is_anonymous():
        return False

    def get_id(self):
        return self.id

class Student(db.Model):
    __tablename__ = "student"
    id = db.Column('id', db.Integer, primary_key=True)
    student_id = db.Column('student_id', db.Unicode(10))
    first_name_en = db.Column('first_name_en', db.Unicode(15))
    last_name_en = db.Column('last_name_en', db.Unicode(15))
    first_name_kh = db.Column('first_name_kh', db.Unicode(15))
    last_name_kh = db.Column('last_name_kh', db.Unicode(15))
    gender = db.Column('gender', db.Unicode(3), default=u'F')
    date_of_birth = db.Column('date_of_birth', db.Unicode(10))
    phone = db.Column('phone', db.Unicode(10))
    email = db.Column('email', db.Unicode(50))
    address = db.Column('address', db.Unicode(50))
    active = db.Column('active', db.Boolean(), default=True)
