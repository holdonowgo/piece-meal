from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
step_ingredient = Table('step_ingredient', pre_meta,
    Column('step_id', INTEGER, primary_key=True, nullable=False),
    Column('ingredient_id', INTEGER, primary_key=True, nullable=False),
    Column('extra_data', VARCHAR(length=50)),
)

step_ingredient = Table('step_ingredient', post_meta,
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('ingredient_id', Integer, primary_key=True, nullable=False),
    Column('measurement', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['step_ingredient'].columns['extra_data'].drop()
    post_meta.tables['step_ingredient'].columns['measurement'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['step_ingredient'].columns['extra_data'].create()
    post_meta.tables['step_ingredient'].columns['measurement'].drop()
