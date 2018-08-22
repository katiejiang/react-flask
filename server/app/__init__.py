import os

from flask import Flask, jsonify
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

compress = Compress()
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

# Set up Flask-Login
login_manager.session_protection = 'strong'
login_manager.unauthorized_handler(lambda : jsonify({}, 400)) # user not logged in

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    set_up_extensions(app)
    configure_ssl(app)
    register_blueprints(app)

    return app

def set_up_extensions(app):
    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    compress.init_app(app)
    RQ(app)

def configure_ssl(app):
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        SSLify(app)

def register_blueprints(app):
    from .account import account
    app.register_blueprint(account, url_prefix='/api/account')
