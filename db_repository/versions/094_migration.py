from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
step_ingredients = Table('step_ingredients', pre_meta,
    Column('step_id', INTEGER, primary_key=True, nullable=False),
    Column('ingredient_id', INTEGER, primary_key=True, nullable=False),
    Column('extra_data', VARCHAR(length=50)),
)

step_sub_recipes = Table('step_sub_recipes', pre_meta,
    Column('step_id', INTEGER, primary_key=True, nullable=False),
    Column('recipe_id', INTEGER, primary_key=True, nullable=False),
    Column('measurement', VARCHAR(length=50)),
)

step_ingredient = Table('step_ingredient', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('ingredient_id', Integer, primary_key=True, nullable=False),
    Column('extra_data', String(length=50)),
)

step_sub_recipe = Table('step_sub_recipe', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer, primary_key=True, nullable=False),
    Column('measurement', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['step_ingredients'].drop()
    pre_meta.tables['step_sub_recipes'].drop()
    post_meta.tables['step_ingredient'].create()
    post_meta.tables['step_sub_recipe'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['step_ingredients'].create()
    pre_meta.tables['step_sub_recipes'].create()
    post_meta.tables['step_ingredient'].drop()
    post_meta.tables['step_sub_recipe'].drop()
