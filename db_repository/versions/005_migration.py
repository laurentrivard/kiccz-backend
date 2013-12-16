from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
release_pictures = Table('release_pictures', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('url', String),
    Column('release_id', Integer),
)

releases = Table('releases', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('brand', String),
    Column('model', String),
    Column('release_date', DateTime),
    Column('price', Integer),
    Column('resell_value', Integer),
    Column('color1', String),
    Column('color2', String),
    Column('text', String),
    Column('picture1', String),
    Column('picture2', String),
    Column('picture3', String),
    Column('image_folder_path', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['release_pictures'].create()
    pre_meta.tables['releases'].columns['image_folder_path'].drop()
    pre_meta.tables['releases'].columns['picture1'].drop()
    pre_meta.tables['releases'].columns['picture2'].drop()
    pre_meta.tables['releases'].columns['picture3'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['release_pictures'].drop()
    pre_meta.tables['releases'].columns['image_folder_path'].create()
    pre_meta.tables['releases'].columns['picture1'].create()
    pre_meta.tables['releases'].columns['picture2'].create()
    pre_meta.tables['releases'].columns['picture3'].create()
