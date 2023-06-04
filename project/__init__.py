import base64
import hashlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_authorize import Authorize
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

#initalising LoginManager a
limiter = Limiter(get_remote_address)

authorize = Authorize()

def create_app():
    app = Flask(__name__)


    encoded_secret_key = 'c2VjcmV0LWtleS1kby1ub3QtcmV2ZWFsCg=='  # secret key that is encoded in base64
    decoded_secret_key = base64.b64decode(encoded_secret_key).decode() #the decoded base-64 code
    hashed_secret_key = hashlib.md5(decoded_secret_key.encode()).hexdigest()#the base-64 encoded secret key will undergo md5 encryption

    app.config['SECRET_KEY'] = hashed_secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    db.init_app(app)

    authorize.init_app(app)

    
    limiter.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    # blueprint for auth routes in our app
    from .json import json as json_blueprint
    app.register_blueprint(json_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
