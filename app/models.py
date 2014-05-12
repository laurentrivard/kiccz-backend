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
	comments = db.relationship('Comments', backref='comments', lazy='dynamic')

class Posts(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	post_date = db.Column(db.DateTime)
	description = db.Column(db.String(512))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	handle = db.Column(db.String(64))
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
	handle = db.Column(db.String(64), db.ForeignKey('user.handle'))

class ReleasePictures(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	url = db.Column(db.String(512))
	release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	handle = db.Column(db.String(64), db.ForeignKey('user.handle'))
	comment_date = db.Column(db.DateTime)
	body = db.Column(db.String(140))
	release_id = db.Column(db.Integer, db.ForeignKey('releases.id'))

class Selling(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	description = db.Column(db.String(140))
	sale_date = db.Column(db.DateTime)
	price = db.Column(db.Float)
	new = db.Column(db.Boolean)
	email = db.Column(db.String(128))
	size = db.Column(db.Float)
	handle = db.Column(db.String, db.ForeignKey('user.handle'))
	sold = db.Column(db.Boolean)

class Buying(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	brand = db.Column(db.String)
	model = db.Column(db.String)
	price = db.Column(db.Float)
	size = db.Column(db.Float)
	email = db.Column(db.String)
	handle = db.Column(db.String, db.ForeignKey('user.handle'))



