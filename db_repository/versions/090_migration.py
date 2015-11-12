from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
step_ingredient = Table('step_ingredient', pre_meta,
    Column('step_id', INTEGER),
    Column('ingredient_id', INTEGER),
    Column('extra_data', VARCHAR(length=50)),
)

step_sub_recipe = Table('step_sub_recipe', pre_meta,
    Column('step_id', INTEGER),
    Column('recipe_id', INTEGER),
    Column('measurement', VARCHAR(length=50)),
)

step_ingredients = Table('step_ingredients', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('ingredient_id', Integer, primary_key=True, nullable=False),
    Column('extra_data', String(length=50)),
)

step_sub_recipes = Table('step_sub_recipes', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer, primary_key=True, nullable=False),
    Column('measurement', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['step_ingredient'].drop()
    pre_meta.tables['step_sub_recipe'].drop()
    post_meta.tables['step_ingredients'].create()
    post_meta.tables['step_sub_recipes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['step_ingredient'].create()
    pre_meta.tables['step_sub_recipe'].create()
    post_meta.tables['step_ingredients'].drop()
    post_meta.tables['step_sub_recipes'].drop()
