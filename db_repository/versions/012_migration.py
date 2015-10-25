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
    Column('home_phone', String(length=10)),
    Column('mobile_phone', String(length=10)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client'].columns['home_phone'].create()
    post_meta.tables['client'].columns['mobile_phone'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client'].columns['home_phone'].drop()
    post_meta.tables['client'].columns['mobile_phone'].drop()
