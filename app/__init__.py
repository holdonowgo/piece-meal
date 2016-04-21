from flask import Flask
# from flask.ext.sandboy import Sandboy
from flask.ext.sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
Bootstrap(app)
# sandboy = Sandboy(app, db, [models.User, models.Client, models.Menu, models.Recipe, models.Step, models.Ingredient])

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))
from app import views, models

# app.jinja_env.globals['momentjs'] = momentjs
