from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	handle = db.Column(db.String(64), index = True, unique = True)
	name = db.Column(db.String(64))
	facebook_id = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	posts = db.relationship('Posts', backref = 'author', lazy = 'dynamic')

	def __repr__(self):
		return '<User %r>' % (self.handle)


class Releases(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	brand = db.Column(db.String(64))
	model = db.Column(db.String(64))
	release_date = db.Column(db.DateTime)
	price = db.Column(db.Integer)
	resell_value = db.Column(db.Integer)
	color1 = db.Column(db.String(64))
	color2 = db.Column(db.String(64))
	text = db.Column(db.String(512))
	date_added = db.Column(db.DateTime)
	release_folder = db.Column(db.String(512))
	pictures = db.relationship('ReleasePictures', backref= 'release', lazy = 'dynamic')
	votes = db.relationship('Votes', backref='votes', lazy='dynamic')

class Posts(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	post_date = db.Column(db.DateTime)
	description = db.Column(db.String(512))
	handle = db.Column(db.Integer, db.ForeignKey('user.handle'))
	pic_path = db.Column(db.String(512))
	likes = db.relationship('Likes', backref = 'likes', lazy='dynamic')

class Votes(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	vote = db.Column(db.Boolean)
	release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Likes(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	like = db.Column(db.Boolean)
	post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
	handle = db.Column(db.Integer, db.ForeignKey('user.handle'))

class ReleasePictures(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	url = db.Column(db.String(512))
	release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))



