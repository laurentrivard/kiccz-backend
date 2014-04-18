from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
posts = Table('posts', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('handle', String),
    Column('facebook_id', String),
    Column('post_date', DateTime),
    Column('description', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].columns['facebook_id'].drop()
    pre_meta.tables['posts'].columns['handle'].drop()
    pre_meta.tables['posts'].columns['name'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].columns['facebook_id'].create()
    pre_meta.tables['posts'].columns['handle'].create()
    pre_meta.tables['posts'].columns['name'].create()
