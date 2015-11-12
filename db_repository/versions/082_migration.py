from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
step = Table('step', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('order_no', Integer),
    Column('recipe_id', Integer),
    Column('instructions', String(length=256)),
)

step_ingredient = Table('step_ingredient', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('ingredient_id', Integer, primary_key=True, nullable=False),
    Column('extra_data', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['step'].columns['order_no'].create()
    post_meta.tables['step_ingredient'].columns['extra_data'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['step'].columns['order_no'].drop()
    post_meta.tables['step_ingredient'].columns['extra_data'].drop()
