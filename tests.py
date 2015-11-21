#!flask/bin/python
import os
import unittest, datetime
from datetime import timedelta, date
from config import basedir
from app import app, db
from app.models import *  # Client, Recipe, Step, Ingredient, Menu
from coverage import coverage

cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()


class TestCaseClient(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Client(self):
        client = Client(name='Randall Spencer',
                        nickname='Randi -- dotted with a heart, of course!',
                        email='randallspencer@gmail.com',
                        home_phone='555-555-5555',
                        mobile_phone='+1-333-333-3333',
                        work_phone='1-777-777-7777'
                        )
        db.session.add(client)
        db.session.commit()

        client = Client.query.filter(Client.name == 'Randall Spencer').first()

        self.assertEqual(client.name, 'Randall Spencer', "Name is wrong!")
        self.assertEqual(client.nickname, 'Randi -- dotted with a heart, of course!')
        self.assertEqual(client.email, 'randallspencer@gmail.com')
        self.assertEqual(client.home_phone, '555-555-5555')
        self.assertEqual(client.mobile_phone, '+1-333-333-3333')
        self.assertEqual(client.work_phone, '1-777-777-7777')

        client.nickname = None
        db.session.add(client)
        db.session.commit()

        client = Client.query.filter(Client.name == 'Randall Spencer').first()

        self.assertEqual(client.nickname, None, 'Client nickname should be None')


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        self.myClient = Client()
        self.myClient = Client(name='Randall Spencer',
                               nickname='Randi -- dotted with a heart, of course!',
                               email='randallspencer@gmail.com',
                               home_phone='555-555-5555',
                               mobile_phone='+1-333-333-3333',
                               work_phone='1-777-777-7777'
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
        db.session.add(i1)
        i2 = Ingredient(name='Peaches (fresh)')
        db.session.add(i2)
        db.session.commit()

        i1 = Ingredient.query.filter(Ingredient.name == 'Blueberries (frozen)').first()
        i2 = Ingredient.query.filter(Ingredient.name == 'Peaches (fresh)').first()

        s.add_ingredient(i1)
        ss1 = s.add_ingredient(i2)
        db.session.add(ss1)
        db.session.commit()

        ss1 = Step.query.first()

        ing1 = ss1.ingredients.filter(Ingredient.name == 'Blueberries (frozen)').first()
        ing1 = ss1.ingredients.filter(Ingredient.name == 'Blueberries (frozen)').first()

        self.assertEquals(i1, ing, "Expected {0}, but got {1}".format(i1, ing))
        # self.assertEquals(i2, ss1.ingredients..filter(name == 'Peaches (fresh)'))

        r2 = Recipe(name='Pie Crust', cooking_style='baked', recipe_type='bread')

        ss2 = ss1.add_sub_recipe(r2)
        db.session.add(ss2)
        db.session.commit()

        result = ss2.sub_recipesV2.filter(Recipe.id == r2.id).first()

        self.assertIsNotNone(result, 'This result is None')
        self.assertEqual(result.name, r2.name, 'These names are not the same')

    def test_Menu(self):
        start_date = date.today()
        menu = Menu(start_date=start_date, end_date=start_date + timedelta(days=7))

        db.session.add(menu)
        db.session.commit()

        menu = Menu.query.first()

        self.assertEqual(menu.start_date.date(), start_date, 'Start date is wrong!  Is {0} but  should be {1}'. \
                         format(start_date, menu.start_date))
        self.assertEqual(menu.end_date.date(), start_date + timedelta(days=7), 'End date is wrong!')

        # def test_Recipe(self):
        #     r1 = Recipe(name='Mango Habanero Hot Sauce', recipe_type='sauce')
        #     r1.cooking_style = "sauce"
        #     r1.description = "Firey-hot diesel like flavor with fruit background"
        #     assert False


# suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
# unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()
