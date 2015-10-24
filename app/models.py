from app import db

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    #nickname = db.Column(db.String(64), index=True, unique=True)
    #email = db.Column(db.String(120), index=True, unique=True)
    is_allergen = db.Column(db.Boolean, unique=False, default=True)
    timestamp = db.Column(db.DateTime)
    warnings = db.relationship('Ingredient_Warning', backref='ingredient', lazy='dynamic')

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
