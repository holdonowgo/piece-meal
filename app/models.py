from app import db

client_recipes = db.Table('client_recipes',
    db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'))
    )

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    home_phone = db.Column(db.String(10), index=True, unique=False)
    mobile_phone = db.Column(db.String(10), index=True, unique=False)
    work_phone = db.Column(db.String(10), index=True, unique=False)
    warnings = db.relationship('Client_Warning', backref='client', lazy='dynamic')
    recipes = db.relationship("Recipe",
                secondary=client_recipes,
                backref="client",
                lazy="dynamic")

    def add_recipe(self, recipe):
        r = self.recipes.filter(Recipe.id == recipe.id).first()
        #if not self.recipes.contains(user):
        if r is None:
            self.recipes.append(recipe)
            return self

    def __repr__(self):
        s = '\n{0}\n{1}\nH#:  {2}\nM#:  {3}\nW: {4}'.format(self.name, self.email, self.home_phone, self.mobile_phone, self.work_phone)
        if self.warnings:#s.count() > 0
            for w in self.warnings:
                s += '\n{0}'.format(w)
        s += '\n'
        return s

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    cooking_style = db.Column(db.Enum('fried', 'baked', 'roasted', 'mixed', name='cooking_style'))
    meal_type = db.Column(db.Enum('breakfast', 'lunch', 'dinner', 'snack'))

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    #nickname = db.Column(db.String(64), index=True, unique=True)
    #email = db.Column(db.String(120), index=True, unique=True)
    is_allergen = db.Column(db.Boolean, unique=False, default=True)
    timestamp = db.Column(db.DateTime)
    warnings = db.relationship('Ingredient_Warning', backref='ingredient', lazy='dynamic')
    type = db.Column(db.Enum('seafood', 'dairy', 'tree_nuts', name='allergen_groups'))

    def __repr__(self):
        #return '<Ingredient %r>' % (self.name)
        s = 'Ingredient: {0}\nIs Allergen: {1}'.format(
        self.name, self.is_allergen
        )
        for w in self.warnings:
            s += '\nWarning: {0}'.format(w.text)
        return s

class Ingredient_Warning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'))

    def __repr__(self):
        #return '<Ingredient %r>' % (self.name)
        return 'Ingredient: {0}\nWarning: {1}'.format(
        self.ingredient.name, self.text
        )

class Client_Warning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))

    def __repr__(self):
        s = 'Warning: {0}'.format(self.text)
        # if self.client:#s.count() > 0
        #     s += '\nClients:'
        #     for w in self.clients:
        #         s += '\nWarning: {0}'.format(w.text)
        return s
