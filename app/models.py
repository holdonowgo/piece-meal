from app import db
from app import app
from datetime import datetime
import sys

if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import flask.ext.whooshalchemy as whooshalchemy


# User (Resource Owner)
# A user, or resource owner, is usually the registered user on your site.
# You design your own user model, there is not much to say.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)

    # posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.nickname


client_recipes = db.Table('client_recipes',
                          db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
                          db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
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
# # we need to know how much of the recipe is needed for this partiucular step
# # maybe even more notes
# step_sub_recipe = db.Table('step_sub_recipe',
#                            db.Column('step_id', db.Integer, db.ForeignKey('step.id')),
#                            db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))

class StepSubRecipe(db.Model):
    __tablename__ = 'step_sub_recipe'
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
    measurement = db.Column(db.String(50))

    # step = db.relationship("Step", backref="step_recipe_assocs")
    recipe = db.relationship("Recipe", backref="step_sub_recipe")

    def __repr__(self):
        return '{0} of {1}'.format(self.measurement, self.recipe.name)


# # this made need to become an Association Table
# # we need to know how much of the ingredient is needed for this partiucular step
# # maybe even more notes
# step_ingredient = db.Table('step_ingredient',
#                            db.Column('step_id', db.Integer, db.ForeignKey('step.id')),
#                            db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
#                            )

class StepIngredient(db.Model):
    __tablename__ = 'step_ingredient'
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
    measurement = db.Column(db.String(50))

    # step = db.relationship("Step", backref="step_ingredient_assocs")
    ingredient = db.relationship("Ingredient", backref="step_ingredient")

    def __repr__(self):
        return '{0} of {1}'.format(self.measurement, self.ingredient.name)


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
                                backref='clients',
                                # backref=db.backref('clients', lazy='dynamic'))
                                lazy='dynamic')

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

    def is_allergic(self, recipe):
        b = False
        alrgns = db.session.query(client_allergens).filter(client_allergens.c.client_id == self.id)
        # print 'db.session.query(client_allergens).filter(client_allergens.c.client_id == self.id)'
        ingrdnts = Ingredient.query \
            .join(StepIngredient) \
            .join(Step) \
            .filter(Ingredient.id == StepIngredient.ingredient_id,
                    StepIngredient.step_id == Step.id,
                    Step.recipe_id == recipe.id).all()
        # print 'Recipe.query.filter(Recipe.id == recipe.id).first().ingredients'
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


### classRecipe.py
class Recipe(db.Model):
    __tablename__ = 'recipe'
    __searchable__ = ['description']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.String(128))
    cooking_style = db.Column(db.Enum('fried', 'baked', 'roasted', 'mixed', name='cooking_style'))
    recipe_type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack', 'sauce', 'bread'))

    ingredients = db.relationship('Ingredient',
                                  secondary=recipe_ingredients,
                                  backref='recipes',
                                  # backref=db.backref('recipes', lazy='dynamic'))
                                  lazy='dynamic')

    # def followed_posts(self):
    #     return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())
    #
    #     Customer.query.\
    #      join(Branch).\
    #      join(Branch.salesmanagers).\
    #      filter(SalesManager.id == 1).all()

    def ingredientsV2(self):
        return Ingredient.query. \
            join(Step). \
            join(Step.ingredients). \
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
        if self.ingredients:  # s.count() > 0
            s += '\n\n----------------------------------'
            for i in self.ingredients:
                s += '\n{0}'.format(i)
        s += '\n----------------------------------'
        s += '\n'
        return s


### classIngredient.py
class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    nutrition = db.Column(db.String(128))
    description = db.Column(db.String(256))
    is_allergen = db.Column(db.Boolean, unique=False, default=True)
    timestamp = db.Column(db.DateTime)
    type = db.Column(db.Enum('seafood', 'dairy', 'tree_nuts', name='allergen_groups'))

    def __repr__(self):
        s = 'Ingredient:\t{0} - Is Allergen:\t{1}'.format(
            self.name, self.is_allergen
        )
        return s


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
                                  backref='steps',
                                  lazy='dynamic'
                                  )

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


if enable_search:
    whooshalchemy.whoosh_index(app, Recipe)
