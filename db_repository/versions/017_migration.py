from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
likes = Table('likes', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('like', Boolean),
    Column('post_id', Integer),
    Column('user_name', Integer),
)

likes = Table('likes', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('like', Boolean),
    Column('post_id', Integer),
    Column('handle', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['likes'].columns['user_name'].drop()
    post_meta.tables['likes'].columns['handle'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['likes'].columns['user_name'].create()
    post_meta.tables['likes'].columns['handle'].drop()
