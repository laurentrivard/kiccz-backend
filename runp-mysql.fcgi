#!flask/bin/python
import os
# use mysql
os.environ['DATABASE_URL'] = 'mysql://apps:9ge.10lau@localhost/apps'

from flup.server.fcgi import WSGIServer
from app import app

if __name__ == '__main__':
    WSGIServer(app).run()
