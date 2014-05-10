from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
comments = Table('comments', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('comment_date', DateTime),
    Column('body', String(length=140)),
    Column('release_id', String(length=64)),
)

posts = Table('posts', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('post_date', DATETIME),
    Column('description', VARCHAR),
    Column('pic_path', VARCHAR),
    Column('handle', INTEGER),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_date', DateTime),
    Column('description', String(length=512)),
    Column('name', String(length=64)),
    Column('pic_path', String(length=512)),
)

likes = Table('likes', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('like', BOOLEAN),
    Column('post_id', INTEGER),
    Column('handle', INTEGER),
)

likes = Table('likes', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('like', Boolean),
    Column('post_id', Integer),
    Column('name', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comments'].create()
    pre_meta.tables['posts'].columns['handle'].drop()
    post_meta.tables['posts'].columns['name'].create()
    pre_meta.tables['likes'].columns['handle'].drop()
    post_meta.tables['likes'].columns['name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['comments'].drop()
    pre_meta.tables['posts'].columns['handle'].create()
    post_meta.tables['posts'].columns['name'].drop()
    pre_meta.tables['likes'].columns['handle'].create()
    post_meta.tables['likes'].columns['name'].drop()