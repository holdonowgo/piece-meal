from app import models
from flask import request, Response, jsonify, abort, render_template
from flask_swagger import swagger
from os import abort
from app.api import services
from sqlalchemy.orm.exc import NoResultFound
# from . import api
from flask import Blueprint
import app

ui = Blueprint(
    name='ui',
    import_name=__name__
    # template_folder='../templates',
    # static_folder='../static'
)

@ui.route('/main')
def search():
    return render_template('main.html')