#!flask/bin/python
import os
import unittest
from datetime import date, timedelta
from config import basedir
from app.models import *
from coverage import coverage
import contextlib

cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

# from sqlalchemy import MetaData
#
# meta = MetaData()
#
# with contextlib.closing(engine.connect()) as con:
#     trans = con.begin()
#     for table in reversed(meta.sorted_tables):
#         con.execute(table.delete())
#     trans.commit()

# add a client
c1 = Client(name='Randall Spencer',
            nickname='Randi -- dotted with a heart, of course!',
            email='randallspencer@gmail.com',
            home_phone='555-555-5555',
            mobile_phone='+1-333-333-3333',
            work_phone='1-777-777-7777'
            )
db.session.add(c1)
db.session.commit()

c2 = Client(name='Michelle Krejci',
            nickname='Dev Meshev',
            email='michellekrejci@gmail.com',
            home_phone='555-555-5555',
            mobile_phone='+1-333-333-3333',
            work_phone='1-777-777-7777'
            )
db.session.add(c2)
db.session.commit()

c3 = Client(name='Brian Spencer',
            nickname='Pootie',
            email='gogubari@gmail.com',
            home_phone='555-555-5555',
            mobile_phone='+1-333-333-3333',
            work_phone='1-777-777-7777'
            )
db.session.add(c3)
db.session.commit()

# add some menus
start_date = date.today()
m1 = Menu(start_date=start_date, end_date=start_date + timedelta(days=7))

db.session.add(m1)
db.session.commit()

start_date = date.today() - timedelta(days=3)
m2 = Menu(start_date=start_date, end_date=start_date + timedelta(days=30))

db.session.add(m2)
db.session.commit()

start_date = date.today() + timedelta(days=10)
m3 = Menu(start_date=start_date, end_date=start_date + timedelta(days=14))

db.session.add(m3)
db.session.commit()

# add a few recipes
r1 = Recipe(name='Mango Habanero Hot Sauce', type='sauce')
r2 = Recipe(name='BLT',
            description='Bacon, Lettuce & Tomato Sandwich',
            style='mixed',
            type='lunch'
            )
db.session.add(r2)
db.session.commit()
r3 = Recipe(name='')

# add some ingredients
i1 = Ingredient(name='Blueberries (frozen)')
db.session.add(i1)
i2 = Ingredient(name='Peaches (fresh)')
db.session.add(i2)
db.session.commit()
