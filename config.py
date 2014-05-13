import os
import urlparse

CSRF_ENABLED = True
SECRET_KEY = 'kiccz_iphone_app_backend'
POSTS_PER_PAGE = 20

basedir = os.path.abspath(os.path.dirname(__file__))


if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#shoe brands
BRANDS = [('Air Jordan', 'Air Jordan'), ('Ascics', 'Ascics'), ('New Balance', 'New Balance'), ('Nike', 'Nike'), ('Reebok', 'Reebok'),
		  ('Patrick Ewings', 'Patrick Ewings'), ('Ronnie Releases', 'Ronnie Releases'), ('Sacony', 'Sacony')]

#image upload
UPLOAD_FOLDER = 'app/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])