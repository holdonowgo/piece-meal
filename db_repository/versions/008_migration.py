from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client = Table('client', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
)

client__warning = Table('client__warning', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', Text),
    Column('client_id', Integer),
)

ingredient = Table('ingredient', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=128)),
    Column('is_allergen', Boolean, default=ColumnDefault(True)),
    Column('timestamp', DateTime),
    Column('type', Enum('seafood', 'dairy', 'tree_nuts', name='allergen_groups')),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client'].create()
    post_meta.tables['client__warning'].create()
    post_meta.tables['ingredient'].columns['type'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client'].drop()
    post_meta.tables['client__warning'].drop()
    post_meta.tables['ingredient'].columns['type'].drop()
