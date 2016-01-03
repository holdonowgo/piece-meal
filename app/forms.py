from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length
from models import Ingredient, Step, Recipe


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class IngredientEditForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[Length(min=0, max=256)])


class EditClientForm(Form):
    name = StringField('name', validators=[DataRequired()])
    nickname = StringField('nickname', validators=[DataRequired()])
    # about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    email = StringField('email', validators=[DataRequired()])
    mobile_phone = StringField('mobile_phone')
