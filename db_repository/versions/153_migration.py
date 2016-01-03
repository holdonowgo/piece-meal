from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('step_id', INTEGER, primary_key=True, nullable=False),
    Column('ingredient_id', INTEGER, primary_key=True, nullable=False),
    Column('notes', VARCHAR(length=50)),
    Column('alt_ingredient_id', INTEGER),
)

allergen_alternative = Table('allergen_alternative', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('step_id', Integer, primary_key=True, nullable=False),
    Column('ingredient_id', Integer, primary_key=True, nullable=False),
    Column('notes', String(length=50)),
    Column('alt_ingredient_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['allergen_alternative'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['allergen_alternative'].drop()
