from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_date', DateTime),
    Column('description', String),
    Column('pic_path', String),
    Column('handle', String),
)

buying = Table('buying', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('brand', String),
    Column('model', String),
    Column('price', Float),
    Column('size', Float),
    Column('email', String),
    Column('handle', String),
)

comments = Table('comments', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('handle', String(length=64)),
    Column('comment_date', DateTime),
    Column('body', String(length=140)),
    Column('release_id', Integer),
)

selling = Table('selling', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String(length=140)),
    Column('sale_date', DateTime),
    Column('price', Float),
    Column('new', Boolean),
    Column('email', String(length=128)),
    Column('size', Float),
    Column('handle', String),
    Column('sold', Boolean),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('post_date', DateTime),
    Column('description', String(length=512)),
    Column('user_id', Integer),
    Column('handle', String(length=64)),
    Column('pic_path', String(length=512)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['buying'].create()
    post_meta.tables['comments'].create()
    post_meta.tables['selling'].create()
    post_meta.tables['posts'].columns['handle'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['buying'].drop()
    post_meta.tables['comments'].drop()
    post_meta.tables['selling'].drop()
    post_meta.tables['posts'].columns['handle'].drop()
