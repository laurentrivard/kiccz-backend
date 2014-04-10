from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post_pictures = Table('post_pictures', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String),
    Column('post_id', Integer),
    Column('user_id', Integer),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_date', DateTime),
    Column('description', String(length=512)),
    Column('user_id', Integer),
    Column('pic_path', String(length=512)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post_pictures'].drop()
    post_meta.tables['posts'].columns['pic_path'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post_pictures'].create()
    post_meta.tables['posts'].columns['pic_path'].drop()
