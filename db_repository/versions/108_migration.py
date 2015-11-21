from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
recipe = Table('recipe', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=128)),
    Column('cooking_style', VARCHAR(length=7)),
    Column('meal_type', VARCHAR(length=9)),
)

recipe = Table('recipe', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('cooking_style', Enum('fried', 'baked', 'roasted', 'mixed', name='cooking_style')),
    Column('recipe_type', Enum('breakfast', 'lunch', 'dinner', 'snack', 'sauce', 'bread')),
)

ingredient = Table('ingredient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('nutrition', String(length=128)),
    Column('description', String(length=256)),
    Column('is_allergen', Boolean, default=ColumnDefault(True)),
    Column('timestamp', DateTime),
    Column('type', Enum('seafood', 'dairy', 'tree_nuts', name='allergen_groups')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['recipe'].columns['meal_type'].drop()
    post_meta.tables['recipe'].columns['recipe_type'].create()
    post_meta.tables['ingredient'].columns['description'].create()
    post_meta.tables['ingredient'].columns['nutrition'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['recipe'].columns['meal_type'].create()
    post_meta.tables['recipe'].columns['recipe_type'].drop()
    post_meta.tables['ingredient'].columns['description'].drop()
    post_meta.tables['ingredient'].columns['nutrition'].drop()
