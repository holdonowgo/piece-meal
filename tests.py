#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import Client, Recipe, Step, Ingredient

class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        self.myClient = Client()
        self.myClient = Client(name = 'Randall Spencer',\
                        nickname = 'Randi -- dotted with a heart, of course!',\
                        email = 'randallspencer@gmail.com',\
                        home_phone = '555-555-5555',\
                        mobile_phone = '+1-333-333-3333',\
                        work_phone = '1-777-777-7777'
                        )
        db.session.add(self.myClient)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_ingredients(self):
        # c = Client(name = 'Randall Spencer',\
        #            nickname = 'Randi -- dotted with a heart, of course!',\
        #            email = 'randallspencer@gmail.com',\
        #            home_phone = '555-555-5555',\
        #            mobile_phone = '+1-333-333-3333',\
        #            work_phone = '1-777-777-7777'
        #            )
        # db.session.add(c)
        # db.session.commit()

        r1 = Recipe(name='Mango Habanero Hot Sauce', recipe_type='sauce')

        # cc1 = c.add_recipe(r1)
        cc1 = self.myClient.add_recipe(r1)
        db.session.add(cc1)
        db.session.commit()

        s = Step(order_no=1, recipe=r1, instructions='Mix the stuff')

        rr = r1.add_step(s)
        db.session.add(rr)
        db.session.commit()

        i1 = Ingredient(name='Blueberries (frozen)')
        i2 = Ingredient(name='Peaches (fresh)')

        ss1 = s.add_ingredient(i1)
        ss1 = s.add_ingredient(i2)
        db.session.add(ss1)
        db.session.commit()

        r2 = Recipe(name='Pie Crust', cooking_style='baked', recipe_type='bread')

        ss2 = ss1.add_sub_recipe(r2)
        db.session.add(ss2)
        db.session.commit()

        result = ss2.sub_recipesV2.filter(Recipe.id == r2.id).first()

        self.assertIsNotNone(result, 'This result is None')
        self.assertEqual(result.name, r2.name, 'These names are not the same')

suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
