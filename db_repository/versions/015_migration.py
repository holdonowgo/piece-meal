from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client_recipes = Table('client_recipes', post_meta,
    Column('client_id', Integer),
    Column('recipe_id', Integer),
)

recipe = Table('recipe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('cooking_style', Enum('fried', 'baked', 'raosted', 'mixed', name='cooking_style')),
    Column('meal_type', Enum('breakfast', 'lunch', 'dinner', 'snack')),
)

client = Table('client', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('home_phone', String(length=10)),
    Column('mobile_phone', String(length=10)),
    Column('work_phone', String(length=10)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client_recipes'].create()
    post_meta.tables['recipe'].create()
    post_meta.tables['client'].columns['work_phone'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client_recipes'].drop()
    post_meta.tables['recipe'].drop()
    post_meta.tables['client'].columns['work_phone'].drop()
