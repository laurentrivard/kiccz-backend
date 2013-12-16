from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
releases = Table('releases', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('brand', String(length=64)),
    Column('model', String(length=64)),
    Column('release_date', DateTime),
    Column('price', Integer),
    Column('resell_value', Integer),
    Column('color1', String(length=64)),
    Column('color2', String(length=64)),
    Column('text', String),
    Column('date_added', DateTime),
    Column('release_folder', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['releases'].columns['release_folder'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['releases'].columns['release_folder'].drop()
