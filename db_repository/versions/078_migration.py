from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
step = Table('step', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer),
    Column('ingredient_id', Integer),
    Column('sub_recipe_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['step'].columns['ingredient_id'].create()
    post_meta.tables['step'].columns['recipe_id'].create()
    post_meta.tables['step'].columns['sub_recipe_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['step'].columns['ingredient_id'].drop()
    post_meta.tables['step'].columns['recipe_id'].drop()
    post_meta.tables['step'].columns['sub_recipe_id'].drop()
