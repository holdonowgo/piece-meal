from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
step_ingredient = Table('step_ingredient', post_meta,
    Column('step_id', Integer),
    Column('ingredient_id', Integer),
)

step_sub_recipe = Table('step_sub_recipe', post_meta,
    Column('step_id', Integer),
    Column('recipe_id', Integer),
)

step = Table('step', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('ingredient_id', INTEGER),
    Column('recipe_id', INTEGER),
    Column('sub_recipe_id', INTEGER),
)

step = Table('step', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('instructions', String(length=256)),
    Column('recipe_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['step_ingredient'].create()
    post_meta.tables['step_sub_recipe'].create()
    pre_meta.tables['step'].columns['ingredient_id'].drop()
    pre_meta.tables['step'].columns['sub_recipe_id'].drop()
    post_meta.tables['step'].columns['instructions'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['step_ingredient'].drop()
    post_meta.tables['step_sub_recipe'].drop()
    pre_meta.tables['step'].columns['ingredient_id'].create()
    pre_meta.tables['step'].columns['sub_recipe_id'].create()
    post_meta.tables['step'].columns['instructions'].drop()
