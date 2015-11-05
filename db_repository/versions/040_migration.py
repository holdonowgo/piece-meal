from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client_allergens = Table('client_allergens', pre_meta,
    Column('client_id', INTEGER),
    Column('ingredient_id', INTEGER),
)

client_allergen = Table('client_allergen', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('client_id', Integer),
    Column('allergen_id', Integer),
)

client_recipes = Table('client_recipes', post_meta,
    Column('client_id', Integer),
    Column('recipe_id', Integer),
)

recipe = Table('recipe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('cooking_style', Enum('fried', 'baked', 'roasted', 'mixed', name='cooking_style')),
    Column('meal_type', Enum('breakfast', 'lunch', 'dinner', 'snack')),
)

recipe_ingredient = Table('recipe_ingredient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer),
    Column('ingredient_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_allergens'].drop()
    post_meta.tables['client_allergen'].create()
    post_meta.tables['client_recipes'].create()
    post_meta.tables['recipe'].create()
    post_meta.tables['recipe_ingredient'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_allergens'].create()
    post_meta.tables['client_allergen'].drop()
    post_meta.tables['client_recipes'].drop()
    post_meta.tables['recipe'].drop()
    post_meta.tables['recipe_ingredient'].drop()
