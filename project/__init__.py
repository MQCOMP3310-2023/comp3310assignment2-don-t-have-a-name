import base64
import hashlib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    encoded_secret_key = 'c2VjcmV0LWtleS1kby1ub3QtcmV2ZWFsCg=='  # secret key that is encoded in base64
    decoded_secret_key = base64.b64decode(encoded_secret_key).decode() #the decoded base-64 code
    hashed_secret_key = hashlib.md5(decoded_secret_key.encode()).hexdigest()#the base-64 encoded secret key will undergo md5 encryption

    app.config['SECRET_KEY'] = hashed_secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'

    db.init_app(app)

    # blueprint for auth routes in our app
    from .json import json as json_blueprint
    app.register_blueprint(json_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
