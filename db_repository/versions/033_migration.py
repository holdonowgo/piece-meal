from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client__warning = Table('client__warning', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('text', TEXT),
    Column('client_id', INTEGER),
)

ingredient__warning = Table('ingredient__warning', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('text', TEXT),
    Column('ingredient_id', INTEGER),
)

recipe = Table('recipe', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=128)),
    Column('cooking_style', VARCHAR(length=7)),
    Column('meal_type', VARCHAR(length=9)),
)

recipe__ingredient = Table('recipe__ingredient', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('recipe_id', INTEGER),
    Column('ingredient_id', INTEGER),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client__warning'].drop()
    pre_meta.tables['ingredient__warning'].drop()
    pre_meta.tables['recipe'].drop()
    pre_meta.tables['recipe__ingredient'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client__warning'].create()
    pre_meta.tables['ingredient__warning'].create()
    pre_meta.tables['recipe'].create()
    pre_meta.tables['recipe__ingredient'].create()
