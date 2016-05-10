from app import db
from app import ma
from app import app
from flask import jsonify
from flask_login import UserMixin
from datetime import datetime

from marshmallow import fields, post_load
from werkzeug.security import check_password_hash, generate_password_hash
from passlib.apps import custom_app_context as pwd_context
import sys

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema, field_for
from flask_marshmallow.sqla import HyperlinkRelated

from config import WHOOSH_ENABLED

if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = WHOOSH_ENABLED
    if enable_search:
        import flask.ext.whooshalchemy as whooshalchemy


# User (Resource Owner)
# A user, or resource owner, is usually the registered user on your site.
# You design your own user model, there is not much to say.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def password(self):
        raise AttributeError('password: write_only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    # @property
    # def is_authenticated(self):
    #     return True
    #
    # @property
    # def is_active(self):
    #     return True
    #
    # @property
    # def is_anonymous(self):
    #     return False
    #
    # def get_id(self):
    #     try:
    #         return unicode(self.id)  # python 2
    #     except NameError:
    #         return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        # fields = ("id", "email", "username", '_links')
        exclude = ("password",)

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        # 'self': ma.URLFor('api._get_user', user_name='<username>'),
        'collection': ma.URLFor('api._get_users')
    })


client_recipes = db.Table('client_recipes',
                          db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
                          db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
                          )

client_menu = db.Table('client_menu',
                       db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
                       db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'))
                       )

client_allergens = db.Table('client_allergens',
                            db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
                            db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
                            )

# I think this table should be killed
# Recipes will not be directly associated with Ingredients
recipe_ingredients = db.Table('recipe_ingredients',
                              db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                              db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
                              )


# recipe_steps = db.Table('recipe_steps',
#                         db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
#                         db.Column('step_id', db.Integer, db.ForeignKey('step.id'))
#                         )

# # this made need to become an Association Table
# # we need to know how much of the recipe is needed for this particular step
# # maybe even more notes
# step_sub_recipe = db.Table('step_sub_recipe',
#                            db.Column('step_id', db.Integer, db.ForeignKey('step.id')),
#                            db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))


# allergen_alternative = db.Table('allergen_alternative',
#                                 db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id')),
#                                 db.Column('alt_ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
#                           )


### classIngredient.py


class IngredientAlternative(db.Model):
    __tablename__ = 'ingredient_alternative'
    # __table_args__ = (
    #     db.ForeignKeyConstraint(
    #         ['step_id', 'ingredient_id'],
    #         ['step_ingredient.step_id', 'step_ingredient.ingredient_id']
    #     ),
    # )
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    alt_ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    notes = db.Column(db.String(50))

    orig_ingredient = db.relationship("Ingredient", foreign_keys=[ingredient_id])
    alt_ingredient = db.relationship("Ingredient", foreign_keys=[alt_ingredient_id])

    # def __repr__(self):
    #     return 'Step #{0} substitute {1} for {2} with the following notes: "{3}"'\
    #         .format(self.step_id, self.alt_ingredient_id, self.ingredient_id, self.notes)


class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    nutrition = db.Column(db.String(128))
    description = db.Column(db.String(256))
    is_allergen = db.Column(db.Boolean, unique=False, default=True)
    timestamp = db.Column(db.DateTime)
    type = db.Column(db.Enum('seafood', 'dairy', 'tree_nut', name='allergen_groups'))

    # alternatives = db.relationship('Ingredient',
    #                               secondary='allergen_alternative',
    #                               backref=db.backref('orig_ingredients', lazy='dynamic'),
    #                               lazy='dynamic')

    # alternatives = db.relationship('Ingredient',
    #                                secondary='ingredient_alternative',
    #                                backref=db.backref('orig_ingredients', lazy='dynamic'),
    #                                lazy='dynamic')

    # alternatives = db.relationship("Ingredient",
    #                                secondary=IngredientAlternative,
    #                                primaryjoin=id == IngredientAlternative.ingredient_id,
    #                                secondaryjoin=id == IngredientAlternative.alt_ingredient_id,
    #                                backref="orig_ingredients",
    #                                lazy='dynamic')

    alternatives = db.relationship('Ingredient',
                                   secondary='ingredient_alternative',
                                   primaryjoin=(IngredientAlternative.ingredient_id == id),
                                   secondaryjoin=(IngredientAlternative.alt_ingredient_id == id),
                                   backref=db.backref('ingredient_alternative', lazy='dynamic'),
                                   lazy='dynamic')

    def add_alternative(self, ingredient):
        if not self.has_alternative(ingredient):
            self.alternatives.append(ingredient)

        return self

    def has_alternative(self, ingredient):
        return self.alternatives.filter(Ingredient.id == ingredient.id).count() > 0

    # def __repr__(self):
    #     s = '<Ingredient:\t{0} - Is Allergen:\t{1}>'.format(
    #         self.name, self.is_allergen
    #     )
    #     return s

    @staticmethod
    def all():
        return Ingredient.query.all()
        # Sreturn 'salt, pepper, milk'


class StepSubRecipe(db.Model):
    __tablename__ = 'step_sub_recipe'
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    measurement = db.Column(db.String(50))

    # step = db.relationship("Step", backref="step_recipe_assocs")
    recipe = db.relationship("Recipe", backref="step_sub_recipe")

    def __repr__(self):
        return '{0} of {1}'.format(self.measurement, self.recipe.name)


class StepIngredient(db.Model):
    __tablename__ = 'step_ingredient'
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    measurement = db.Column(db.String(50))

    # step = db.relationship("Step", backref="step_ingredients")
    ingredient = db.relationship("Ingredient", backref="step_ingredient")

    def requires_alternative(self, client):
        return Ingredient.query.join(client_allergens, (client_allergens.c.ingredient_id == self.ingredient_id)) \
                   .filter(client_allergens.c.client_id == client.id).count() > 0

    # alternatives = db.relationship('Ingredient',
    #                                secondary=AllergenAlternative.__table__,
    #                                primaryjoin='and_(StepIngredient.step_id==AllergenAlternative.step_id, '
    #                                            'StepIngredient.ingredient_id==AllergenAlternative.ingredient_id)',
    #                                # secondaryjoin=ingredient_id==AllergenAlternative.ingredient_id,
    #                                secondaryjoin='and_(Ingredient.id==AllergenAlternative.ingredient_id)',
    #                                backref=db.backref('original', lazy='dynamic'),
    #                                # backref='ingredients',
    #                                lazy='dynamic')

    # alternatives = db.relationship("AllergenAlternative", foreign_keys=[step_id, ingredient_id])

    # alternatives = db.relationship("AllergenAlternative",
    #                                primaryjoin="StepIngredient.step_id==StepIngredient.step_id,"
    #                                            "StepIngredient.ingredient_id==StepIngredient.ingredient_id")

    @property
    def alt_ingredients(self):
        return AllergenAlternative.query.filter(
            AllergenAlternative.step_id == self.step_id,
            AllergenAlternative.ingredient_id == self.ingredient_id) \
            .order_by(AllergenAlternative.alt_ingredient_id)

    def __repr__(self):
        return '{0} of {1}'.format(self.measurement, self.ingredient.name)


class AllergenAlternative(db.Model):
    __tablename__ = 'allergen_alternative'
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['step_id', 'ingredient_id'],
            ['step_ingredient.step_id', 'step_ingredient.ingredient_id']
        ),
    )

    # id = db.Column(db.Integer, primary_key=True)
    # step_id = db.Column(db.Integer, db.ForeignKey('step_ingredient.step_id'), primary_key=True)
    # ingredient_id = db.Column(db.Integer, db.ForeignKey('step_ingredient.ingredient_id'), primary_key=True)
    step_id = db.Column(db.Integer, db.ForeignKey('step_ingredient.step_id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('step_ingredient.ingredient_id'), primary_key=True)
    alt_ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    notes = db.Column(db.String(50))

    # ingredient_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    # alt_ingredient_id = db.Column(db.Integer, db.ForeignKey("address.id"))

    orig_ingredient = db.relationship("StepIngredient", foreign_keys=[step_id, ingredient_id])
    alt_ingredient = db.relationship("Ingredient", foreign_keys=[alt_ingredient_id])

    # step_ingredient = db.relationship('StepIngredient', backref='alternatives', foreign_keys=[step_id, ingredient_id])

    def __repr__(self):
        return 'Step #{0} substitute {1} for {2} with the following notes: "{3}"' \
            .format(self.step_id, self.alt_ingredient_id, self.ingredient_id, self.notes)


### classRecipe.py
class Recipe(db.Model):
    __tablename__ = 'recipe'
    __searchable__ = ['description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)
    description = db.Column(db.String(128))
    style = db.Column(db.Enum('fried', 'baked', 'roasted', 'mixed', name='cooking_style'))
    type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack', 'sauce', 'bread', 'dessert', name='recipe_type'))

    # ingredients = db.relationship('Ingredient',
    #                               secondary=recipe_ingredients,
    #                               backref='recipes',
    #                               # backref=db.backref('recipes', lazy='dynamic'))
    #                               lazy='dynamic')

    # ingredients = db.relationship("Ingredient",
    #                 primaryjoin="and_(User.id==Address.user_id, Address.city=='Boston')",
    #                               primaryjoin=)

    # ingredients = db.relationship("Step.ingredients", backref='recipe', lazy='dynamic')

    # def followed_posts(self):
    #     return Post.query.join(followers, (followers.c.followed_id == Post.user_id))\
    #                      .filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
    #
    #     Customer.query.\
    #      join(Branch).\
    #      join(Branch.salesmanagers).\
    #      filter(SalesManager.id == 1).all()

    # ingredients = db.relationship('Ingredient', backref='recipe', lazy='dynamic')

    @property
    def ingredientsV2(self):
        return Ingredient.query. \
            join(StepIngredient). \
            join(Step). \
            filter(Step.recipe_id == self.id)

    #   TODO need to define 'ingredients' for Recipe

    # steps = db.relationship('Step',
    #                         secondary=recipe_steps,
    #                         backref='steps',
    #                         # backref=db.backref('recipes', lazy='dynamic'))
    #                         lazy='dynamic')

    steps = db.relationship('Step', backref='recipe', lazy='dynamic')

    def has_ingredient(self, ingredient):
        b = self.ingredients.filter(Ingredient.id == ingredient.id).count() > 0
        return b

    def client_allergen_conflict(self, ingredient):
        query = db.session.query(Client). \
            join(client_recipes). \
            join(client_allergens). \
            filter(client_recipes.c.recipe_id == self.id). \
            filter(client_allergens.c.ingredient_id == ingredient.id). \
            filter(Client.id == client_recipes.c.recipe_id).count()
        if query > 0:
            return True
        else:
            return False

    def add_ingredient(self, ingredient):
        if not self.has_ingredient(ingredient):
            if not self.client_allergen_conflict(ingredient):
                self.ingredients.append(ingredient)

        return self

    def add_step(self, step):
        # if not self.has_step(step):
        # if not self.client_allergen_conflict(step):
        self.steps.append(step)

        return self

    def __repr__(self):
        s = self.name
        # if self.ingredients:  # s.count() > 0
        #     s += '\n\n----------------------------------'
        #     for i in self.ingredients:
        #         s += '\n{0}'.format(i)
        # s += '\n----------------------------------'
        # s += '\n'
        return s

    @staticmethod
    def get_catalogue():
        return Recipe.query.order_by(Recipe.name)


# # this made need to become an Association Table
# # we need to know how much of the ingredient is needed for this particular step
# # maybe even more notes
# step_ingredient = db.Table('step_ingredient',
#                            db.Column('step_id', db.Integer, db.ForeignKey('step.id')),
#                            db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
#                            )


# # from classClient import Client
# # from classIngredient import Ingredient
# class Client_Allergen(db.Model):
#     __tablename__ = 'client_allergen'S
#     id = db.Column(db.Integer, primary_key=True)
#     client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
#     allergen_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
#
#     client = db.relationship('Client', backref='client')
#     allergen = db.relationship('Ingredient', backref='client_allergen')
#
#     def __repr__(self):
#         i = Ingredient.query.filter(Ingredient.id == self.allergen_id).first()
#         s = 'Ingredient: {0}\nIs Allergen: {1}'.format(
#         i.name, i.is_allergen
#         )

# classClient.py
class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    home_phone = db.Column(db.String(10), index=True, unique=False)
    mobile_phone = db.Column(db.String(10), index=True, unique=False)
    work_phone = db.Column(db.String(10), index=True, unique=False)
    # warnings = db.relationship('Client_Warning', backref='client', lazy='dynamic')

    recipes = db.relationship('Recipe',
                              secondary=client_recipes,
                              backref='clients',
                              # backref=db.backref('clients', lazy='dynamic'))
                              lazy='dynamic')

    allergens = db.relationship('Ingredient',
                                secondary=client_allergens,
                                # backref='clients',
                                backref=db.backref('client', lazy='dynamic'),
                                # foreign_keys=[id],
                                lazy='dynamic')

    menus = db.relationship('Menu',
                            secondary=client_menu,
                            backref='clients',
                            lazy='dynamic')

    # @property
    # def _allergens(self):
    #     return db.session.query(client_allergens).filter(client_allergens.c.client_id == self.id)

    @property
    def _allergens(self):
        return Ingredient.query \
            .join(client_allergens) \
            .filter(Ingredient.id == client_allergens.c.ingredient_id,
                    client_allergens.c.client_id == self.id)

    # allergens = db.relationship('Client_Allergen',
    #             # secondary=client_allergen,
    #             backref='clients', lazy='dynamic')

    def add_recipe(self, recipe):
        if not self.has_recipe(recipe):
            # # if Recipe_Ingredient.query.join(Client_Allergen,
            # #     (Client_Allergen.ingredient_id == Recipe_Ingredient.ingredient_id).
            # #     filter(Client_Allergen.client_id == self.id)).count == 0:
            # ri = recipe.ingredients
            # fa = db.session.query(self.allergens).filter(self.allergens.ingredient_id.in_(ri)).all()
            # print 'db.session.query(self.allergens).filter(self.allergens.ingredient_id.in_(ri)).all()'
            # print fa.count()
            # fa = self.allergens.filter(allergens.ingredient_id.in_(ri)).all()
            # print 'self.allergens.filter(allergens.ingredient_id.in_(ri)).all()'
            # print fa.count()
            # if fa.count() == 0
            if not self.is_allergic(recipe):
                self.recipes.append(recipe)

        return self

    def add_menu(self, menu):
        if not self.has_menu(menu):
            if not self.is_allergic(menu):
                self.menus.append(menu)

        return self

    def is_allergic(self, recipe):
        b = False
        alrgns = db.session.query(client_allergens).filter(client_allergens.c.client_id == self.id)
        # print 'db.session.query(client_allergens).filter(client_allergens.c.client_id == self.id)'
        ingrdnts = Ingredient.query \
            .join(StepIngredient) \
            .join(Step) \
            .filter(Ingredient.id == StepIngredient.ingredient_id,
                    StepIngredient.step_id == Step.id,
                    Step.recipe_id == recipe.id)
        # print 'Recipe.query.filter(Recipe.id == recipe.id).first().ingredients'
        # from pprint import pprint
        # pprint(Ingredient.query.all())
        # pprint(StepIngredient.query.all())
        # pprint(Step.query.all())
        for a in alrgns:
            for i in ingrdnts:
                if a.ingredient_id == i.id:
                    b = True
        return b

    # return Post.query.join(followers, (followers.c.followed_id == Post.user_id))\
    # .filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def remove_recipe(self, recipe):
        if self.has_recipe(recipe):
            self.recipes.remove(recipe)
            return self

    def has_recipe(self, recipe):
        return self.recipes.filter(Recipe.id == recipe.id).count() > 0

    def has_menu(self, menu):
        return self.menus.filter(Menu.id == menu.id).count() > 0

    def add_allergen(self, ingredient):
        if not self.has_allergen(ingredient):
            self.allergens.append(ingredient)
            return self

    def remove_allergen(self, ingredient):
        if self.has_allergen(ingredient):
            self.allergens.remove(ingredient)
            return self

    def has_allergen(self, ingredient):
        b = self.allergens.filter(Ingredient.id == ingredient.id).count() > 0
        return b

    def __repr__(self):
        s = '\n{0}\n{1}\nH#:  {2}\nM#:  {3}\nW: {4}'.format(self.name, self.email, self.home_phone, self.mobile_phone,
                                                            self.work_phone)
        # if self.warnings:#s.count() > 0
        #     for w in self.warnings:
        #         s += '\n{0}'.format(w)
        # s += '\n'
        return s


class MenuRecipe(db.Model):
    __tablename__ = 'menu_recipe'
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)


class Menu(db.Model):
    __tablename__ = 'menu'
    # __searchable__ = ['description']

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    recipes = db.relationship('Recipe',
                              secondary="menu_recipe",
                              backref='menus',
                              # backref=db.backref('recipes', lazy='dynamic'))
                              lazy='dynamic')

    # @property
    # def recipes(self):
    #     return Recipe.query.\
    #     join(MenuRecipe)
    #     filter(MenuRecipe.menu_id == self.id)

    @property
    def ingredients(self):
        return Ingredient.query. \
            join(MenuRecipe). \
            join(Recipe). \
            join(Recipe.ingredients). \
            filter(MenuRecipe.menu_id == self.id, MenuRecipe.recipe_id == Recipe.recipe_id)

    def add_recipe(self, recipe):
        if not self.has_recipe(recipe):
            # if not self.client_allergen_conflict(ingredient):
            self.recipes.append(recipe)

        return self

    def has_recipe(self, recipe):
        return self.recipes.filter(Recipe.id == recipe.id).count() > 0

    def __repr__(self):
        result = "{0:%d/%m/%y} - {1:%d/%m/%y}}".format(self.start_date, self.end_date)

        for r in self.recipes:
            result += "\n\n{0}".format(r)

        return result


class Step(db.Model):
    """docstring for """
    __tablename__ = 'step'
    id = db.Column(db.Integer, primary_key=True)  # step_no?
    order_no = db.Column(db.Integer)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    instructions = db.Column(db.String(256))

    sub_recipes = db.relationship('Recipe',
                                  secondary='step_sub_recipe',
                                  backref=db.backref("step", lazy='dynamic')
                                  )

    ingredients = db.relationship('Ingredient',
                                  secondary='step_ingredient',
                                  # backref='steps',
                                  lazy='dynamic'
                                  )

    step_ingredients = db.relationship('StepIngredient', backref='step', lazy='dynamic')

    @property
    def ingredientsV2(self):
        return Ingredient.query. \
            join(StepIngredient). \
            filter(StepIngredient.step_id == self.id)

    @property
    def sub_recipesV2(self):
        return Recipe.query. \
            join(StepSubRecipe). \
            filter(StepSubRecipe.step_id == self.id)

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

        return self

    def add_sub_recipe(self, recipe):
        self.sub_recipes.append(recipe)

        return self

    def has_ingredient(self, ingredient):
        b = self.ingredients.filter(Ingredient.id == ingredient.id).count() > 0
        return b

    def __repr__(self):
        return 'Step #:\t{0}\nInstructions:\t{1}'.format( \
            self.order_no, self.instructions
        )


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)

    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic')

    def add_item(self, item):
        self.order_items.append(item)

        return self

    @property
    def items(self):
        return OrderItem.query.filter(OrderItem.order_id == self.id)


class OrderItem(db.Model):
    tablename = 'order_item'
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    each_serving = db.Column(db.Integer, nullable=False)
    each_cost = db.Column(db.DECIMAL)

    # order = db.relationship("Order", backref="order_items", lazy='dynamic')

    @property
    def recipe(self):
        return Recipe.query.filter(Recipe.id == self.recipe_id).first()

    @property
    def total_cost(self):
        return self.quantity * self.each_cost


class IngredientAlternativeSchema(ma.ModelSchema):
    class Meta:
        model = IngredientAlternative


class AllergenAlternativeSchema(ma.ModelSchema):
    class Meta:
        model = AllergenAlternative
        # fields = ("step_id", "ingredient_id", "alt_ingredient_id", "notes", "step_ingredient", "_links")
        exclude = ("password",)

        # # Smart hyperlinking
        # _links = ma.Hyperlinks({
        #     'self': ma.URLFor('api._get_allergen_alternative', step_id='<step_id>', ingredient_id='<ingredient_id>'),
        #     'collection': ma.URLFor('api._get_allergen_alternatives')
        # })


class IngredientSchema(ma.ModelSchema):
    class Meta:
        model = Ingredient
        # fields = ("id", "name", "description", "style", "type", "_links")
        exclude = ('step_ingredient', 'client',)

    alternatives = ma.Nested('self', many=True,
                             only=('_links', 'description', 'id', 'is_allergen', 'name', 'nutrition', 'timestamp'),
                             include=('uri'))

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api._get_ingredient', id='<id>'),
        'collection': ma.URLFor('api._get_ingredients')
    })

    uri = ma.URLFor('api._get_ingredient', id='<id>')


class StepSubRecipeSchema(ma.ModelSchema):
    class Meta:
        model = StepSubRecipe
        # fields = ("step_id", "recipe_id", "measurement", "_links")

    # recipe = ma.Nested(RecipeSchema, many=True)

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api._get_step_sub_recipe', step_id='<step_id>', recipe_id='<recipe_id>'),
        'collection': ma.URLFor('api._get_step_sub_recipes')
    })


class StepIngredientSchema(ma.ModelSchema):
    class Meta:
        model = StepIngredient
        # fields = ("step_id", "ingredient_id", "measurement", "_links")

    # recipe = ma.Nested(RecipeSchema, many=True)

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api._get_step_ingredient', step_id='<step_id>', recipe_id='<recipe_id>'),
        # 'collection': ma.URLFor('api._get_step_ingredients')
    })


class StepSchema(ma.ModelSchema):
    class Meta:
        model = Step
        # fields = ("id", "recipe_id", "instructions")

    ingredients = ma.Nested(IngredientSchema, many=True)

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.recipe_step', recipe_id='<recipe_id>', step_id='<id>'),
        'collection': ma.URLFor('api.recipe_step', recipe_id='<recipe_id>')
    })


class RecipeSchema(ma.ModelSchema):
    class Meta:
        model = Recipe
        # fields = ("id", "name", "description", "style", "type", "_links")
        exclude = ('step', 'clients', 'step_sub_recipe')

    steps = ma.Nested(StepSchema, many=True)

    # sub_recipes = ma.Nested(StepSubRecipeSchema, many=True)
    # ingredients = ma.Nested(StepIngredientSchema, many=True)
    # ingredients = ma.Method("get_days_since_created", dump_only=True)
    #
    # def get_days_since_created(self, obj):
    #     # return dt.datetime.now().day - obj.created_at.day
    #     ingredients_schmea = IngredientSchema(many=True)
    #     ingredients = db.session.query(Ingredient).all()
    #     # return jsonify(ingredients_schmea.dump(ingredients))
    #     return ingredients_schmea.jsonify(ingredients)
    #     # print(db.session.query(User).all())
    #     # print(db.session.query(Ingredient).all())
    #     # return db.session.query(Ingredient).all()

    # balance = fields.Method('get_balance', deserialize='load_balance', dump_only=True)
    #
    # def get_balance(self, obj):
    #     return obj.name
    #
    # def load_balance(self, value):
    #     return float(value)

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api._get_recipe', recipe_id='<id>'),
        'collection': ma.URLFor('api._get_recipes')
    })


class ClientSchema(ma.ModelSchema):
    class Meta:
        model = Client
        # fields = ("id", "recipe_id", "instructions")

    recipes = ma.Nested(RecipeSchema, many=True)

    # pass Schema as string to avoid infinite circular relation between Clients & Recipes
    menus = ma.Nested('MenuSchema', many=True, exclude=('client,'), dump_only=True, )

    allergens = ma.Nested(IngredientSchema, many=True, only=("_links",
                                                             "alternatives",
                                                             "description",
                                                             "id",
                                                             "is_allergen",
                                                             "name",
                                                             "nutrition",
                                                             "timestamp",
                                                             "type"))

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api._get_client', client_id='<id>'),
        'collection': ma.URLFor('api._get_clients')
    })

    @post_load
    def make_client(self, data):
        return Client(**data)


class MenuSchema(ma.ModelSchema):
    class Meta:
        model = Menu
        # fields = ("end_date",)

    # end_date = fields.Method("formate_date", dump_only=True)

    def formate_date(self, menu):
        return menu.end_time

    clients = ma.Nested(ClientSchema, many=True, exclude=('menu',), dump_only=True, )

    recipes = ma.Nested(RecipeSchema, many=True)

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api._get_menu', menu_id='<id>'),
        'collection': ma.URLFor('api._get_menus')
    })


if enable_search:
    whooshalchemy.whoosh_index(app, Recipe)
