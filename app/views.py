from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, db
from models import User, Releases, Posts, Votes, ReleasePictures, Likes, ROLE_USER, Comments, Selling, Buying
from forms import AddReleaseForm
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug import secure_filename
import os, errno, random
from datetime import datetime

@app.route('/')
@app.route('/index')

def index():
	return render_template("index.html",
		title = "Kiccz")

@app.route('/releases')
def get_releases():
	#get all releases
	releases = Releases.query.all()
	return render_template("releases.html",
		releases = releases)


def returnJsonReleaseInfo():
	jsondic = {}
	releases = Releases.query.all()
	jsondic["releases"] = []
	for r in releases:
		rel = {}
		rel['brand'] = r.brand
		rel['model'] = r.model
		rel['release_date'] = str(r.release_date)
		rel['price'] = r.price
		rel['resell_value'] = r.resell_value
		rel['color1'] = r.color1
		rel['color2'] = r.color2
		rel['text'] = r.text
		rel['date_added'] = str(r.date_added)
		pics = []
		for p in r.pictures.all():
			pics.append(p.url)
		rel['pictures'] = pics
		coms = []
		for c in r.comments.all():
			coms.append(c.body)
		rel['comments'] = coms
		cop, drop = 0, 0
		for v in r.votes.all():
			if v.vote:
				cop +=1
			else:
				drop +=1
		votes = {'cop': cop, 'drop': drop}
		rel['votes'] = votes		
		print 'cop = ' + str(cop)
		print 'drop = ' + str(drop)
		jsondic["releases"].append(rel)
	resp = jsonify(jsondic)
	resp.status_code = 200
	return resp

def returnJsonSellingInfo():
	jsondic = {}
	sales = Selling.query.all()
	jsondic["sales"] = []
	for s in sales:
		sell = {}
		sell['brand'] = s.description
		sell['email'] = s.email
		sell['sale_date'] = s.sale_date
		sell['price'] = s.price
		sell['new'] = s.new
		sell['size'] = s.size
		sell['handle'] = s.handle
		sell['sold'] = s.sold
		cop, drop = 0, 0
		for v in s.votes.all():
			if v.vote:
				cop +=1
			else:
				drop +=1
		votes = {'cop': cop, 'drop': drop}
		sell['votes'] = votes		
		print 'cop = ' + str(cop)
		print 'drop = ' + str(drop)
		jsondic["sales"].append(sell)
	resp = jsonify(jsondic)
	resp.status_code = 200
	return resp

def populate_test_posts():
	for i in range(0,6):
		print "post" + str(i)
		newPost = Posts( 
			post_date=datetime.now(), 
			description='test description',
			user_id = '13',
			pic_path = "posts/shoe" + str(i) + ".jpg",
			)
		# newLike = Likes(like = True, post_id = i, user_id = '1234')
		# db.session.add(newLike)
		db.session.add(newPost)
	db.session.commit()

@app.route('/upload_post', methods= ['POST'])
def get_image():
	handle = request.form['handle']
	user_id = User.query.filter_by(handle = handle).first()
	description = request.form['description']
	post_date = datetime.now()
	files = request.files.getlist("image_name")
	filename = ''
	for file in files:
		name = "%s" % str(handle) + "_" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		filename = secure_filename(name)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'posts', filename))
	path = os.path.join(UPLOAD_FOLDER, '/posts', filename)
	# mkdir_p(path)
	newPost = Posts(post_date = post_date,
					description = description,
					handle = handle,
					user_id = user_id,
					pic_path = path)
	db.session.add(newPost)
	db.session.commit()
	resp = jsonify({})
	resp.status_code = 200
	return resp

def returnJsonPostInfo(index):
	jsondic = {}
	posts = Posts.query.order_by(Posts.post_date.desc())
	jsondic["posts"] = []
	for (i,p) in enumerate(posts[((index-1)*20):(index * 20)]):
		likes = 0
		pos = {}
		pos['handle'] = p.handle
		pos['description'] = p.description
		pos['post_date'] = str(p.post_date)
		pos['pic_path'] = p.pic_path
		for l in p.likes.all():
			likes += 1
		pos['likes'] = likes
		jsondic["posts"].append(pos)
	resp = jsonify(jsondic)
	resp.status_code = 200
	return resp	

def returnJsonProfileInfo(user_id):
	user = User.query.filter_by(id = user_id)
	resp = jsonify(user)
	resp.status_code = 200
	return resp

@app.route('/like_post', methods = ["POST"])
def like():
	user_id = request.form['user_id']
	release_id = request.form['release_id']
	exists = Likes.query.filter_by(user_id = user_id, release_id = release_id).first()
	if not exists:	
		newLike = Likes(like = True,
					post_id = request.form['post_id'],
					handle = request.form['handle'])
		db.session.add(newVote) 
		db.session.commit()	
	resp = jsonify({"No like error": "Like added successfully"})
	resp.status_code = 200
	return resp	

@app.route('/m_releases')
def get_m_releases():
	data = returnJsonReleaseInfo()
	return data

@app.route('/sell', methods = ['GET'])
def get_s_releases():
	sale = returnJsonSellingInfo()
	return sale

@app.route('/profile/<int:user_id>')
def get_profile_info(user_id = 0):
	prof = returnJsonProfileInfo(user_id)
	return prof		

@app.route('/home')
@app.route('/home/')
@app.route('/home/<int:index>', methods = ['GET'])
def get_posts(index = 1):
	#posts = Posts.query.all()
	posts = returnJsonPostInfo(index)
	return posts

@app.route('/home2', methods = ['GET'])
def get_posts2():
	for i in range(0,6):
		newUser= User(handle = 'test' + str(i), name='test' + str(i), 
				facebook_id = 'test' + str(i), 
				role=ROLE_USER)
		db.session.add(newUser)

		newPost = Posts( post_date=datetime.now(), 
					description='test description',
					user_id = '1234',
					pic_path = "posts/shoe" + str(i) + ".jpg",)
		db.session.add(newPost)

		newLike = Likes(like = True, post_id = i, user_id = '1234')
		db.session.add(newLike)
		
	db.session.commit()


#helper to check if uploaded file should be accepted
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#helper to create directory of images for each release
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


@app.route('/m_release_vote', methods = ["GET", "POST"])
def vote():
	vote = True
	user_id = request.form['user_id']
	release_id = request.form['release_id']
	if request.form['vote'] != 'cop':
		vote = False
	exists = Votes.query.filter_by(user_id = user_id, release_id = release_id).first()
	if not exists:	
		newVote = Votes(vote = vote,
					release_id = request.form['release_id'],
					user_id = request.form['user_id'])
		db.session.add(newVote)
	else: #vote already exists, so we update it
		exists.vote = vote 
	#commits the change	
	db.session.commit()	
	resp = jsonify({"hello": "hello"})
	resp.status_code = 200
	return resp	

@app.route('/m_add_release', methods = ["GET", "POST"])
def m_add_release():
	brand = request.form['brand']
	model = request.form['model']
	date = request.form['release_date']
	release_folder = 'releases/' + brand.replace(" ", "_") + "_" + model.replace(" ", "_") + "_" + datetime.now().strftime("%Y-%m-%d")
	path = os.path.join(UPLOAD_FOLDER, release_folder)
	mkdir_p(path)
	print UPLOAD_FOLDER
	newRelease = Releases(brand = brand,
					model = model,
					#release_date = date,
					price = request.form['price'],
					resell_value = request.form['resell_value'],
					color1 = request.form['color1'],
					color2 = request.form['color2'],
					release_folder = release_folder,
					text = request.form['text'],
					date_added = datetime.now())
	db.session.add(newRelease)
	# db.session.commit()
	#release_id = Releases.query.order_by(Releases.id.desc()).first()
	#print request.files[]
	#print request.form


	resp = jsonify({"error": "maybe"})
	resp.status_code = 200
	return resp

@app.route('/add_release', methods = ['GET', 'POST'])
def add_release():
	addReleaseForm = AddReleaseForm()
	#if form was submitted
	if addReleaseForm.validate_on_submit():
		brand = addReleaseForm.brand.data
		model = addReleaseForm.model.data
		date = addReleaseForm.release_date.data
		#create a subfolder to uplaod pictures of the specifc release
		release_folder = 'releases/' + brand.replace(" ", "_") + "_" + model.replace(" ", "_") + "_" + datetime.now().strftime("%Y-%m-%d")
		path = os.path.join(UPLOAD_FOLDER, release_folder)
		mkdir_p(path)
		print UPLOAD_FOLDER
		newRelease = Releases(brand = brand,
							model = model,
							release_date = date,
							price = addReleaseForm.price.data,
							resell_value = addReleaseForm.resell_value.data,
							color1 = addReleaseForm.color1.data,
							color2 = addReleaseForm.color2.data,
							release_folder = release_folder,
							text = addReleaseForm.text.data,
							date_added = datetime.now())
		db.session.add(newRelease)
		db.session.commit()
		release_id = Releases.query.order_by(Releases.id.desc()).first()

		uploaded_files = request.files.getlist("picture")
		for pic in uploaded_files:
			if pic and allowed_file(pic.filename):
				filename = secure_filename(pic.filename)
				url = os.path.join(path, filename)
				pic.save(url)
				url = os.path.join(release_folder, filename)
				picture = ReleasePictures(url = url,
										release_id = release_id.id)
				db.session.add(picture)

		db.session.commit()		

		#redirects to list of releases
	#	return get_releases()
	else:
		print addReleaseForm.errors	
	return render_template('add_release.html',
		form = addReleaseForm)	

@app.route('/m_create_account', methods = ['GET', 'POST'])
def m_create_account():
	user_id = request.form['user_id']
	name = request.form['name']
	handle = request.form['handle']
	user = User.query.filter_by(facebook_id = user_id).first()
	handle_already_used = User.query.filter_by(handle = handle).first()
	#handle already used, return error
	if handle_already_used != None:
		resp = jsonify({"error": "The handle you chose already exists. Please choose a different one."})
		resp.status_code = 200
		return resp
	#create new user
	if user == None:
		user = User(facebook_id = user_id,
					name = name,
					handle = handle,
					role = ROLE_USER)
		db.session.add(user)
		db.session.commit()
	else:
		m_login()	#should never be called

	return_user = User.query.filter_by(facebook_id = user_id).first()
	new_user = {}
	new_user['user_id'] = return_user.id
	new_user['handle'] = return_user.handle
	new_user['name'] = return_user.name
	new_user['role'] = return_user.role

	resp = jsonify(new_user)
	resp.status_code = 200
	return resp

@app.route('/m_login', methods = ['GET', 'POST'])
def m_login():
	user_id = request.form['user_id']
	user = User.query.filter_by(facebook_id = user_id).first()
	if user == None:
		resp = jsonify({"account_exists": "no"})
		resp.status_code = 200
		return resp
	else:
	   #login the user and return his info
	   new_user = {}
	   new_user['user_id'] = user.id
	   new_user['handle'] = user.handle
	   new_user['name'] = user.name
	   new_user['role'] = user.role
	   resp = jsonify(new_user)
	   resp.status_code = 200
	   return resp	
