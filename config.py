import os

CSRF_ENABLED = True
SECRET_KEY = 'kiccz_iphone_app_backend'

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ['HEROKU_POSTGRESQL_TEAL_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#shoe brands
BRANDS = [('Air Jordan', 'Air Jordan'), ('Ascics', 'Ascics'), ('New Balance', 'New Balance'), ('Nike', 'Nike'), ('Reebok', 'Reebok'),
		  ('Patrick Ewings', 'Patrick Ewings'), ('Ronnie Releases', 'Ronnie Releases'), ('Sacony', 'Sacony')]

#image upload
UPLOAD_FOLDER = 'app/static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])