from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
posts = Table('posts', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_date', DateTime),
    Column('description', String),
    Column('user_id', Integer),
    Column('pic_path', String),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_date', DateTime),
    Column('description', String(length=512)),
    Column('handle', Integer),
    Column('pic_path', String(length=512)),
)

likes = Table('likes', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('like', Boolean),
    Column('post_id', Integer),
    Column('user_id', Integer),
)

likes = Table('likes', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('like', Boolean),
    Column('post_id', Integer),
    Column('user_name', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].columns['user_id'].drop()
    post_meta.tables['posts'].columns['handle'].create()
    pre_meta.tables['likes'].columns['user_id'].drop()
    post_meta.tables['likes'].columns['user_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['posts'].columns['user_id'].create()
    post_meta.tables['posts'].columns['handle'].drop()
    pre_meta.tables['likes'].columns['user_id'].create()
    post_meta.tables['likes'].columns['user_name'].drop()
