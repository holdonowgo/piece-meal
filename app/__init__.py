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
from .views.api import api
from .views.ui import ui
app.register_blueprint(api, url_prefix='/piece-meal/api/v1.0')
app.register_blueprint(ui)
# sandboy = Sandboy(app, db, [models.User, models.Client, models.Menu, models.Recipe, models.Step, models.Ingredient])

from .momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)
oid = OpenID(app, os.path.join(basedir, 'tmp'))

if not app.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/piecemeal.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('piecemeal startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('piecemeal startup')

app.jinja_env.globals['momentjs'] = momentjs

from app import views, models
