from . import db
from flask_authorize import RestrictionsMixin, AllowancesMixin, PermissionsMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# mapping tables
UserGroup = db.Table(
    'user_group', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'))
)

UserRole = db.Table(
    'user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    passwordAttempts = db.Column(db.Integer,default=0)
    roles = db.relationship('Role', secondary=UserRole)
    groups = db.relationship('Group', secondary=UserGroup)
    

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password, password_plaintext)
        
        
    def set_password(self, password_plaintext: str):
        self.password = generate_password_hash(password_plaintext)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

class Restaurant(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    ratings = db.Column(db.Float)
    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }
 
class MenuItem(db.Model):
    __tablename__ = 'menuItem'
    
    name = db.Column(db.String(80), nullable = False)
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    course = db.Column(db.String(250))
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'       : self.name,
           'description' : self.description,
           'id'         : self.id,
           'price'      : self.price,
           'course'     : self.course,
       }

class Rating(db.Model):
    __tablename__ = 'Rating'

    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    user = db.relationship(User)
    restaurant_id = db.Column(db.Integer,db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)
