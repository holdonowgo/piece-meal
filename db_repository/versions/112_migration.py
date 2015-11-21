from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu = Table('menu', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

menu_recipe = Table('menu_recipe', post_meta,
    Column('menu_id', Integer, primary_key=True, nullable=False),
    Column('recipe_id', Integer, primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].create()
    post_meta.tables['menu_recipe'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].drop()
    post_meta.tables['menu_recipe'].drop()
