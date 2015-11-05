from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client_allergens = Table('client_allergens', pre_meta,
    Column('client_id', INTEGER),
    Column('allergen_id', INTEGER),
)

client__allergen = Table('client__allergen', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('client_id', Integer),
    Column('allergen_id', Integer),
)

receipt__ingredient = Table('receipt__ingredient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer),
    Column('ingredient_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_allergens'].drop()
    post_meta.tables['client__allergen'].create()
    post_meta.tables['receipt__ingredient'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_allergens'].create()
    post_meta.tables['client__allergen'].drop()
    post_meta.tables['receipt__ingredient'].drop()
