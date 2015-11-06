from app import db
from datetime import datetime


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
        return '<User %r>' % (self.nickname)


client_recipes = db.Table('client_recipes',
                          db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
                          db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
                          )

client_allergens = db.Table('client_allergens',
                            db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
                            db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
                            )

recipe_ingredients = db.Table('recipe_ingredients',
                              db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                              db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
                              )

# recipe_steps = db.Table('recipe_steps',
#                         db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
#                         db.Column('step_id', db.Integer, db.ForeignKey('step.id'))
#                         )

step_sub_recipe = db.Table('step_sub_recipe',
                           db.Column('step_id', db.Integer, db.ForeignKey('step.id')),
                           db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
                           )

step_ingredient = db.Table('step_ingredient',
                           db.Column('step_id', db.Integer, db.ForeignKey('step.id')),
                           db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
                           )


# # from classClient import Client
# # from classIngredient import Ingredient
# class Client_Allergen(db.Model):
#     __tablename__ = 'client_allergen'
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
                print recipe.name + ' added!'

        return self

    def is_allergic(self, recipe):
        b = False
        alrgns = db.session.query(client_allergens).filter(client_allergens.c.client_id == self.id)
        print 'db.session.query(client_allergens).filter(client_allergens.c.client_id == self.id)'
        ingrdnts = Recipe.query.filter(Recipe.id == recipe.id).first().ingredients
        print 'Recipe.query.filter(Recipe.id == recipe.id).first().ingredients'
        for a in alrgns:
            for i in ingrdnts:
                if a.ingredient_id == i.id:
                    print 'Recipe contains allergen {0}'.format(i.name)
                    b = True
        print 'Recipe does not contain allergen'
        return b

    # return Post.query.join(followers, (followers.c.followed_id == Post.user_id))\
    # .filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def remove_recipe(self, recipe):
        if self.has_recipe(recipe):
            self.recipes.remove(recipe)
            return self

    def has_recipe(self, recipe):
        cnt = self.recipes.filter(Recipe.id == recipe.id).count()
        if cnt > 0:
            print 'client already has recipe'
            return True
        else:
            print 'client does not have recipe'
            return False

    def add_allergen(self, ingredient):
        if not self.has_allergen(ingredient):
            print 'add_allergen start'
            self.allergens.append(ingredient)
            print 'add_allergen end'
            return self

    def remove_allergen(self, ingredient):
        if self.has_allergen(ingredient):
            self.allergens.remove(ingredient)
            return self

    def has_allergen(self, ingredient):
        print 'has_allergen start'
        b = self.allergens.filter(Ingredient.id == ingredient.id).count() > 0
        print 'has_allergen end'
        return b

    def __repr__(self):
        s = '\n{0}\n{1}\nH#:  {2}\nM#:  {3}\nW: {4}'.format(self.name, self.email, self.home_phone, self.mobile_phone,
                                                            self.work_phone)
        # if self.warnings:#s.count() > 0
        #     for w in self.warnings:
        #         s += '\n{0}'.format(w)
        # s += '\n'
        return s


### classRecipe.py
class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    cooking_style = db.Column(db.Enum('fried', 'baked', 'roasted', 'mixed', name='cooking_style'))
    meal_type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack'))

    ingredients = db.relationship('Ingredient',
                                  secondary=recipe_ingredients,
                                  backref='recipes',
                                  # backref=db.backref('recipes', lazy='dynamic'))
                                  lazy='dynamic')

    # steps = db.relationship('Step',
    #                         secondary=recipe_steps,
    #                         backref='steps',
    #                         # backref=db.backref('recipes', lazy='dynamic'))
    #                         lazy='dynamic')

    steps = db.relationship('Step', backref='recipe', lazy='dynamic')

    def has_ingredient(self, ingredient):
        print 'has_ingredient start'
        b = self.ingredients.filter(Ingredient.id == ingredient.id).count() > 0
        print 'has_ingredient end'
        return b

    def client_allergen_conflict(self, ingredient):
        # alrgns = db.session.query.join(client_allergens).filter(client_allergens.c.client_id == self.id)
        # query = session.query(User, Document, DocumentsPermissions).join(Document).join(DocumentsPermissions)
        query = db.session.query(Client). \
            join(client_recipes). \
            join(client_allergens). \
            filter(client_recipes.c.recipe_id == self.id). \
            filter(client_allergens.c.ingredient_id == ingredient.id). \
            filter(Client.id == client_recipes.c.recipe_id).count()
        if query > 0:
            print 'Client Allergen Conflict!'
            return True
        else:
            return False

    def add_ingredient(self, ingredient):
        if not self.has_ingredient(ingredient):
            if not self.client_allergen_conflict(ingredient):
                self.ingredients.append(ingredient)
                print 'Ingredient Added!'
            else:
                print 'Ingredient Not Added!'

        return self

    def __repr__(self):
        s = self.name
        if self.ingredients:  # s.count() > 0
            s += '----------------------------------'
            for i in self.ingredients:
                s += '\n{0}'.format(i)
        s += '----------------------------------'
        s += '\n'
        return s


### classIngredient.py
class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    # nickname = db.Column(db.String(64), index=True, unique=True)
    # email = db.Column(db.String(120), index=True, unique=True)
    is_allergen = db.Column(db.Boolean, unique=False, default=True)
    timestamp = db.Column(db.DateTime)
    # warnings = db.relationship('Ingredient_Warning', backref='ingredient', lazy='dynamic')
    type = db.Column(db.Enum('seafood', 'dairy', 'tree_nuts', name='allergen_groups'))

    def __repr__(self):
        # return '<Ingredient %r>' % (self.name)
        s = 'Ingredient: {0}\nIs Allergen: {1}'.format(
            self.name, self.is_allergen
        )
        # for w in self.warnings:
        #     s += '\nWarning: {0}'.format(w.text)
        return s

class Step(db.Model):
    """docstring for """
    id = db.Column(db.Integer, primary_key=True)#step_no?
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    # ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
    # sub_recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    # ForeignKeyConstraint(['invoice_id', 'ref_num'], ['invoice.invoice_id', 'invoice.ref_num']),
    # recipe_id = Column(Integer, ForeignKey('recipe.id'), primary_key=True)
    # employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    # extra_data = Column(String(256))
    instructions = db.Column(db.String(256))

    # recipe = db.relationship(Recipe, backref="recipe_assoc")
    # sub_recipe = db.relationship(Recipe, backref="sub_recipe_assoc")
    # ingredient = db.relationship(Ingredient, backref="ingredient_assoc")

    ingredient = db.relationship('Ingredient',
                                  secondary=step_ingredient,
                                  backref='step',
                                  # backref=db.backref('recipes', lazy='dynamic'))
                                  lazy='dynamic')

    sub_recipe = db.relationship('Recipe',
                                 secondary=step_sub_recipe,
                                 backref='step',
                                 # backref=db.backref('recipes', lazy='dynamic'))
                                 lazy='dynamic')

    def set_ingredient(self, ingredient):
        if not self.has_ingredient(ingredient):
        # if not self.client_allergen_conflict(ingredient):
            self.ingredient.append(ingredient)
            print 'Ingredient Set!'
        else:
            print 'Ingredient Not Set!'

        return self

    def has_ingredient(self, ingredient):
        print 'step_has_ingredient start'
        b = self.ingredient.filter(Ingredient.id == ingredient.id).count() > 0
        print 'has_ingredient end'
        return b

# class Ingredient_Warning(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text)
#     ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
#
#     def __repr__(self):
#         #return '<Ingredient %r>' % (self.name)
#         return 'Ingredient: {0}\nWarning: {1}'.format(
#         self.ingredient.name, self.text
#         )
#
# class Client_Warning(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.Text)
#     client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
#
#     def __repr__(self):
#         s = 'Warning: {0}'.format(self.text)
#         # if self.client:#s.count() > 0
#         #     s += '\nClients:'
#         #     for w in self.clients:
#         #         s += '\nWarning: {0}'.format(w.text)
#         return s

# from classRecipe import Recipe
# from classIngredient import Ingredient
# class Recipe_Ingredient(db.Model):
#     __tablename__ = 'recipe_ingredient'
#     id = db.Column(db.Integer, primary_key=True)
#     recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
#     ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))
#
#     recipe = db.relationship('Recipe', backref='ingredient_recipe')
#     ingredient = db.relationship('Ingredient', backref='recipe_ingredient')
