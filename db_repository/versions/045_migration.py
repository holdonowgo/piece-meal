from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client_allergen = Table('client_allergen', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('client_id', INTEGER),
    Column('allergen_id', INTEGER),
)

recipe_ingredient = Table('recipe_ingredient', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('recipe_id', INTEGER),
    Column('ingredient_id', INTEGER),
)

client_allergens = Table('client_allergens', post_meta,
    Column('client_id', Integer),
    Column('ingredient_id', Integer),
)

recipe_ingredients = Table('recipe_ingredients', post_meta,
    Column('recipe_id', Integer),
    Column('ingredient_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_allergen'].drop()
    pre_meta.tables['recipe_ingredient'].drop()
    post_meta.tables['client_allergens'].create()
    post_meta.tables['recipe_ingredients'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_allergen'].create()
    pre_meta.tables['recipe_ingredient'].create()
    post_meta.tables['client_allergens'].drop()
    post_meta.tables['recipe_ingredients'].drop()
