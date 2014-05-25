from app import db
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	handle = db.Column(db.String(64), index = True, unique = True)
	name = db.Column(db.String(64))
	facebook_id = db.Column(db.String(120), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ROLE_USER)
	email = db.Column(db.String(120))
	posts = db.relationship('Posts', backref = 'author', lazy = 'dynamic')

	@staticmethod
	def make_unique_handle(handle):
		if User.query.filter_by(handle = handle).first() == None:
			return handle
		version = 2
		while True:
			new_handle = handle + str(version)
			if User.query.filter_by(handle = new_handle).first() == None:
				break
			version += 1
		return new_handle

	@staticmethod
	def make_unique_fbid(facebook_id):
		if User.query.filter_by(facebook_id = facebook_id).first() == None:
			return facebook_id
		version = 2
		while True:
			new_facebood_id = facebook_id + str(version)
			if User.query.filter_by(facebook_id = new_facebood_id).first() == None:
				break
			version += 1
		return new_facebood_id

	@staticmethod
	def populate_user_table(count):
		for i in range(0,count):
			newUser = User(handle = "chrissplinter" + str(i),
				name = "chrissplinter",
				facebook_id = "chrisfacebook" + str(i)
			)
			newHandle = newUser.make_unique_handle(newUser.handle)
			newFbid = newUser.make_unique_fbid(newUser.facebook_id)
			newUser = User(handle = newHandle,
				name = "chrissplinter",
				facebook_id = newFbid)
			db.session.add(newUser)
		db.session.commit()

	def __repr__(self):
		return '<User %r>' % (self.handle)

class Releases(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	brand = db.Column(db.String(64))
	model = db.Column(db.String(64))
	release_date = db.Column(db.DateTime)
	price = db.Column(db.Float)
	resell_value = db.Column(db.Float)
	color1 = db.Column(db.String(64))
	color2 = db.Column(db.String(64))
	#gr = db.Column(db.Boolean())
	#difficulty = db.Column(db.Integer)
	text = db.Column(db.String(512))
	date_added = db.Column(db.DateTime)
	release_folder = db.Column(db.String(512))
	pictures = db.relationship('ReleasePictures', backref= 'release', lazy = 'dynamic')
	votes = db.relationship('Votes', backref='votes', lazy='dynamic')
	comments = db.relationship('Comments', backref='comments', lazy='dynamic')

	@staticmethod
	def populate_releases_table(count):
		for i in range(0,count):
			newRelease = Releases(id = i, 
				brand="Nike", 
				model='test',
				release_date=datetime.now(),
				price=i,
				resell_value=100,
				color1="crim",
				color2="morecrim",
				text= "test",
				date_added = datetime.now()
				)
			# newLike = Likes(like = True, post_id = i, user_id = '1234')
			# db.session.add(newLike)
			db.session.add(newRelease)
		db.session.commit()

class Posts(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	post_date = db.Column(db.DateTime)
	description = db.Column(db.String(512))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	handle = db.Column(db.String(64))
	pic_path = db.Column(db.String(512))
	likes = db.relationship('Likes', backref = 'likes', lazy='dynamic')
	dislikes = db.relationship('disLikes', backref = 'disLikes', lazy='dynamic')

	@staticmethod
	def populate_posts_table(count):
		for i in range(0,count):
			newPost = Posts( 
				post_date=datetime.now(), 
				description='test description',
				user_id = i,
				pic_path = "posts/shoe" + str(i) + ".jpg",
				)
			# newLike = Likes(like = True, post_id = i, user_id = '1234')
			# db.session.add(newLike)
			db.session.add(newPost)
		db.session.commit()

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

class disLikes(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	dislike = db.Column(db.Boolean)
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

	@staticmethod
	def populate_comments_table(count):
		for i in range(0,count):
			newComment = Comments(handle = "chrissplinter" + str(i),
				comment_date = datetime.now(),
				body = "example comment " + str(i),
				release_id = i
			)
			db.session.add(newComment)
		db.session.commit()

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

	@staticmethod
	def populate_sell_table(count):
		for i in range(0,count):
			newSale = Selling(description = "test",
				sale_date=datetime.now(), 
				price =7.5,
				new = False,
				email = "test email",
				size = 10.5,
				handle = "chrissplinter" + str(i),
				sold = False
			)
			db.session.add(newSale)
		db.session.commit()

class Buying(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	brand = db.Column(db.String)
	model = db.Column(db.String)
	price = db.Column(db.Float)
	size = db.Column(db.Float)
	email = db.Column(db.String)
	handle = db.Column(db.String, db.ForeignKey('user.handle'))

	@staticmethod
	def populate_buy_table(count):
		for i in range(0,count):
			newBuy = Buying(brand = "Nike",
				model = "Air", 
				price =75,
				size = 10.5,
				email = "test email",
				handle = "chrissplinter" + str(i),
			)
			db.session.add(newBuy)
		db.session.commit()



