from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
ingredient_alternative = Table('ingredient_alternative', post_meta,
    Column('ingredient_id', Integer, primary_key=True, nullable=False),
    Column('alt_ingredient_id', Integer, primary_key=True, nullable=False),
    Column('notes', String(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ingredient_alternative'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['ingredient_alternative'].drop()
