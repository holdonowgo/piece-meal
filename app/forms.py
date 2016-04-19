from flask.ext.wtf import Form
from wtforms.fields import (StringField, BooleanField, TextAreaField, FieldList, TextField, PasswordField,
                            SubmitField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from models import User, Ingredient


def possible_ingredient():
    return Ingredient.query


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class IngredientEditForm(Form):
    name = StringField('name', validators=[DataRequired()])
    nutrition = StringField('nutrition', validators=[DataRequired()])
    description = TextAreaField('description', validators=[Length(min=0, max=256)])
    is_allergen = BooleanField('is_allergen', default=False)


class EditClientForm(Form):
    name = StringField('name', validators=[DataRequired()])
    nickname = StringField('nickname', validators=[DataRequired()])
    # about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])
    email = StringField('email', validators=[DataRequired()])
    mobile_phone = StringField('mobile_phone')


class EditStepForm(Form):
    order_no = StringField('order_no', validators=[DataRequired()])
    instructions = TextAreaField('instructions', validators=[DataRequired(), Length(min=0, max=256)])
    # ingredients = FieldList(TextField('ingredients', validators=[DataRequired()]))
    autocomp = TextField('autocomp', id='autocomplete')
    ingredient = TextField('ingredient')
    ingredient_list = QuerySelectField('ingredient_list', query_factory=possible_ingredient, get_label='name',
                                       allow_blank=True)


class LoginForm(Form):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignUpForm(Form):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(),
                                                      EqualTo("password2", message="Passwords must match!")])
    password2 = PasswordField('Re-Enter Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(1, 120), Email()])
    submit = SubmitField('Log In')

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There is already another user with this email address.')

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken')
