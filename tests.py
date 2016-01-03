#!flask/bin/python
import os
import unittest
import datetime
from datetime import date, timedelta
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

        self.myMenu = Menu(start_date=date.today(), end_date=date.today())
        self.myRecipe = Recipe(name='Flourless Chocolate Cake',
                               description='A rich chocolate cake encrusted with nuts.',
                               style='baked',
                               type='dessert')
        self.myStep = Step(order_no=1, recipe=self.myRecipe, instructions='Crush Hazelnuts')
        self.myIngredient = Ingredient(name='Hazelnut',
                                       description='Also known as filbert',
                                       timestamp=datetime.utcnow(),
                                       type='tree_nut')

        db.session.add(self.myMenu)
        db.session.add(self.myIngredient)
        db.session.add(self.myRecipe)
        db.session.add(self.myStep)
        self.myStep.add_ingredient(self.myIngredient)
        self.myRecipe.add_step(self.myStep)
        db.session.add(self.myRecipe)

        db.session.commit()

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

        ingredient = Ingredient.query.first()

        client.add_allergen(ingredient)
        db.session.add(client)
        db.session.commit()

        client = Client.query.filter(Client.name == 'Randall Spencer').first()

        self.assertEqual(client.allergens.count(), 1, 'Client should have one allergen!')
        self.assertEqual(client._allergens.first().name,
                         'Hazelnut',
                         'Allergen name should be ''Hazelnut'' and not {0}'.format(client._allergens.first().name))

        r = Recipe.query.first()

        client.add_recipe(r)

        self.assertNotIn(r, client.recipes,
                         'Client should not contain the recipe {0} because they suffer from an allergy to {1} and '
                         'the recipe contains {2}'.format(
                             r.name, client.allergens.first(), r.ingredients.first()))


class TestCaseAllergenAlternatives(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        create_ingredient(self)

        self.myRecipe = Recipe(name='BLT',
                               description='Bacon, Lettuce & Tomato Sandwich',
                               style='mixed',
                               type='lunch'
                               )
        db.session.add(self.myRecipe)
        db.session.commit()

        self.myStep = Step(order_no=1,
                           recipe=self.myRecipe,
                           instructions='Mix flour with water until smooth.  '
                                        'Slowly add mixture to soup base while stirring.')
        db.session.add(self.myStep)

        self.myStepIngredient = StepIngredient(step=self.myStep, ingredient=self.myIngredient1)
        db.session.add(self.myStepIngredient)
        db.session.commit()

        self.myAllergenAlt1 = AllergenAlternative(
            # step=self.myStep,
            # ingredient_id=self.myIngredient1.id,
            step_ingredient=self.myStepIngredient,
            alt_ingredient_id=self.myIngredient2.id,
            notes='use half the amount')
        db.session.add(self.myAllergenAlt1)
        self.myAllergenAlt2 = AllergenAlternative(
            # step=self.myStep,
            # ingredient_id=self.myIngredient1.id,
            step_ingredient=self.myStepIngredient,
            alt_ingredient_id=self.myIngredient3.id,
            notes='use 1/4 the amount')
        db.session.add(self.myAllergenAlt2)
        db.session.commit()

        # print self.myRecipe.steps.count()
        #
        # print self.myStep.ingredients.count()
        #
        # print self.myStep.step_ingredients.count()

        # print self.myAllergenAlt1
        # print self.myAllergenAlt2
        # print self.myStepIngredient.alternatives
        # print 'Count: {0}.'.format(self.myStepIngredient.alternatives.count)
        #
        # for idx,alt in enumerate(self.myStepIngredient.alternatives):
        #     print alt
        #     print idx

        # for alt in AllergenAlternative.query.all():
        #     print alt

        self.myClient = Client(name='Randall Spencer',
                               nickname='Randi -- dotted with a heart, of course!',
                               email='randallspencer@gmail.com',
                               home_phone='555-555-5555',
                               mobile_phone='+1-333-333-3333',
                               work_phone='1-777-777-7777'
                               )
        db.session.add(self.myClient)
        db.session.commit()
        self.myClient.add_allergen(self.myIngredient1)
        db.session.add(self.myClient)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_AllergenAlternative(self):
        self.assertTrue(self.myStepIngredient.requires_alternative(self.myClient),
                        'This step should require alternatives.')

        self.assertEquals(self.myStepIngredient.alt_ingredients.count(), 2, 'There should be 2 alternative ingredients')

        # print 'TEST START'
        # print AllergenAlternative.query.all()
        # print AllergenAlternative.query.count()
        # print 'TEST END'


def create_ingredient(self):
    self.myIngredient1 = Ingredient(name='Wheat Flour')
    self.myIngredient2 = Ingredient(name='Cornstarch')
    self.myIngredient3 = Ingredient(name='Arrowroot Powder')
    db.session.add(self.myIngredient1)
    db.session.add(self.myIngredient2)
    db.session.add(self.myIngredient3)
    db.session.commit()


class TestCaseIngredient(unittest.TestCase):
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

    def test_Ingredient(self):
        r1 = Recipe(name='Mango Habanero Hot Sauce', type='sauce')

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
        ing2 = ss1.ingredients.filter(Ingredient.name == 'Peaches (fresh)').first()

        self.assertEquals(i1, ing1, "Expected {0}, but got {1}".format(i1, ing1))
        # self.assertEquals(i2, ss1.ingredients..filter(name == 'Peaches (fresh)'))

        r2 = Recipe(name='Pie Crust', style='baked', type='bread')

        ss2 = ss1.add_sub_recipe(r2)
        db.session.add(ss2)
        db.session.commit()

        result = ss2.sub_recipesV2.filter(Recipe.id == r2.id).first()

        self.assertIsNotNone(result, 'This result is None')
        self.assertEqual(result.name, r2.name, 'These names are not the same')


class TestCaseMenu(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        self.myRecipe = Recipe(name='', description='')
        db.session.add(self.myRecipe)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Menu(self):
        start_date = date.today()
        menu = Menu(start_date=start_date, end_date=start_date + timedelta(days=7))

        db.session.add(menu)
        db.session.commit()

        menu = Menu.query.first()

        menu.add_recipe(self.myRecipe)

        self.assertIn(self.myRecipe, menu.recipes, '{0} should be in this collection of recipes'.format(self.myRecipe))

        self.assertEqual(menu.start_date.date(), start_date, 'Start date is wrong!  Is {0} but  should be {1}'.
                         format(start_date, menu.start_date))

        self.assertEqual(menu.end_date.date(), start_date + timedelta(days=7), 'End date is wrong!')


class TestCaseRecipe(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

        self.myRecipe = Recipe(name='BLT',
                               description='Bacon, Lettuce & Tomato Sandwich',
                               style='mixed',
                               type='lunch'
                               )
        db.session.add(self.myRecipe)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Recipe(self):
        recipe = Recipe.query.first()
        self.assertEquals(recipe.name, 'BLT', 'Name should be BLT')


class TestCaseOrder(unittest.TestCase):
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

        self.myRecipe = Recipe(name='', description='')
        db.session.add(self.myRecipe)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_Order(self):
        order = Order()
        db.session.add(order)
        db.session.commit()

        recipe = Recipe.query.first()

        order_item = OrderItem(order=order, recipe_id=recipe.id, quantity=3, each_serving=4, each_cost=8.88)
        o = order.add_item(order_item)
        db.session.add(o)
        db.session.commit()

        oo = Order.query.first()

        self.assertEqual(oo.order_items.count(), 1, 'There should be one order item.')


suite = unittest.TestLoader().loadTestsFromTestCase(TestCaseClient)
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCaseIngredient))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCaseOrder))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCaseMenu))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCaseRecipe))
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCaseAllergenAlternatives))
unittest.TextTestRunner(verbosity=2).run(suite)

# if __name__ == '__main__':
#     try:
#         unittest.main()
#     except:
#         pass
#     cov.stop()
#     cov.save()
#     print("\n\nCoverage Report:\n")
#     cov.report()
#     print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
#     cov.html_report(directory='tmp/coverage')
#     cov.erase()
