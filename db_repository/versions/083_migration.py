from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
step_sub_recipe = Table('step_sub_recipe', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer, primary_key=True, nullable=False),
    Column('extra_data', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['step_sub_recipe'].columns['extra_data'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['step_sub_recipe'].columns['extra_data'].drop()
