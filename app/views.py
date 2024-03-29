from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, db
from models import User, Releases, Posts, Votes, ReleasePictures, Likes, disLikes, ROLE_USER, Comments, Selling, Buying
from forms import AddReleaseForm
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug import secure_filename
import os, errno, random
from datetime import datetime
import time
from time import mktime
@app.route('/')
@app.route('/index')
def index():
	User.populate_user_table(5)
	return render_template("index.html", title = "Kiccz")

@app.route('/m_create_account', methods = ['GET', 'POST'])
def m_create_account():
	user_id = request.form['user_id']
	name = request.form['name']
	handle = request.form['handle']
	email = request.form['email']
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
					email = email,
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
	new_user['email'] = return_user.email

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
		rel['gr'] = r.gr
		rel['difficulty'] = r.difficulty
		rel['text'] = r.text
		rel['date_added'] = str(r.date_added)
		pics = []
		for p in r.pictures.all():
			pics.append(p.url)
		rel['pictures'] = pics
		coms = []
		for c in r.comments.limit(5).all():
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

@app.route('/releases')
def get_releases():
	#get all releases
	releases = Releases.query.all()
	return render_template("releases.html", releases = releases)

def returnJsonSellingInfo():
	jsondic = {}
	sales = Selling.query.all()
	jsondic["sales"] = []
	for s in sales:
		sell = {}
		sell['description'] = s.description
		sell['email'] = s.email
		sell['sale_date'] = s.sale_date
		sell['price'] = s.price
		sell['new'] = s.new
		sell['size'] = s.size
		sell['handle'] = s.handle
		sell['sold'] = s.sold
		jsondic["sales"].append(sell)
	resp = jsonify(jsondic)
	resp.status_code = 200
	return resp

def returnJsonBuyingInfo():
	jsondic = {}
	buys = Buying.query.all()
	jsondic["buys"] = []
	for b in buys:
		buy = {}
		buy['brand'] = b.brand
		buy['model'] = b.model
		buy['price'] = b.price
		buy['size'] = b.size
		buy['email'] = b.email
		buy['handle'] = b.handle
		jsondic["buys"].append(buy)
	resp = jsonify(jsondic)
	resp.status_code = 200
	return resp

def returnJsonPostInfo(index):
	jsondic = {}
	posts = Posts.query.order_by(Posts.post_date.desc())
	jsondic["posts"] = []
	for (i,p) in enumerate(posts[((index-1)*20):(index * 20)]):
		likes = 0
		dislikes = 0
		pos = {}
		pos['handle'] = p.handle
		pos['description'] = p.description
		pos['id'] = p.id
		pos['post_date'] = str(p.post_date)
		pos['pic_path'] = p.pic_path
		for l in p.likes.all():
			likes += 1
		pos['likes'] = likes
		for d in p.dislikes.all():
			dislikes += 1
		pos['dislikes'] = dislikes
		jsondic["posts"].append(pos)
	resp = jsonify(jsondic)
	resp.status_code = 200
	return resp
		
def returnJsonProfileInfo(user_id,index):
	userdic = {}
	user = User.query.filter_by(id = user_id).first()
	userdic['handle'] = user.handle
	userdic['name'] = user.name
	userdic['facebook_id'] = user.facebook_id
	userdic['role'] = user.role
	userdic['email'] = user.email
	posts = user.posts.limit(index*20).all()
	userdic["posts"] = []
	for p in posts:
		likes = 0
		pos = {}
		pos['handle'] = p.handle
		pos['description'] = p.description
		pos['post_date'] = str(p.post_date)
		pos['pic_path'] = p.pic_path
		for l in p.likes.all():
			likes += 1
		pos['likes'] = likes
		userdic["posts"].append(pos)
	resp = jsonify(userdic)
	resp.status_code = 200
	return resp

def returnJsonCommentsInfo(release_id, index):
	commentdic = {}
	release = Releases.query.filter_by(id = release_id).first()
	commentdic["comments"] = []
	for c in release.comments.limit(index*25).all():
		com = {}
		com["handle"] = c.handle
		com["comment_date"] = c.comment_date
		com["body"] = c.body
		com["release_id"] = c.release_id
		commentdic["comments"].append(com)
	resp = jsonify(commentdic)
	resp.status_code = 200
	return resp

@app.route('/upload_sale', methods= ['POST'])
def get_sale():
	description = request.form['description']
	sale_date = datetime.now()
	price = request.form['price']
	new = request.form['new']
	email = request.form['email']
	size = request.form['size']
	handle = request.form['handle']
	newSale = Selling(description = description,
					sale_date = sale_date,
					price = price,
					new = new,
					email = email,
					size = size,
					handle = handle,
					sold = False)
	db.session.add(newSale)
	db.session.commit()
	resp = jsonify({})
	resp.status_code = 200
	return resp

@app.route('/upload_buy', methods= ['POST'])
def get_buy():
	brand = request.form['brand']
	model = request.form['model']
	price = request.form['price']
	size = request.form['size']
	email = request.form['email']
	handle =request.form['handle']
	newBuy = Buying(brand = brand,
					model = model,
					price = price,
					size = size,
					email = email,
					handle = handle)
	db.session.add(newBuy)
	db.session.commit()
	resp = jsonify({})
	resp.status_code = 200
	return resp

@app.route('/upload_post', methods= ['POST'])
def get_image():
	handle = request.form['handle']
	user_id = User.query.filter_by(handle = handle).first()
	email = request.form['email']
	description = request.form['description']
	post_date = datetime.now()
	files = request.files.getlist("image_name")
	filename = ''
	for file in files:
		name = "%s" % str(handle) + "_" + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		filename = secure_filename(name)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'posts', filename))
	path = os.path.join(UPLOAD_FOLDER, '/posts', filename)
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


@app.route('/like_post', methods= ["POST"])
def like():
	handle = request.form['handle']
	post_id = request.form['post_id']
	exists = Likes.query.filter_by(handle = handle, post_id = post_id).first()
	if not exists:	
		newLike = Likes(like = True,
					post_id = post_id,
					handle = handle)
		db.session.add(newLike) 
		db.session.commit()	
	resp = jsonify({"No like error": "Like added successfully"})
	resp.status_code = 200
	return resp

@app.route('/dislike_post', methods = ["POST"])
def dislike():
	handle = request.form['handle']
	post_id = request.form['post_id']
	exists = disLikes.query.filter_by(handle = handle, post_id = post_id).first()
	if not exists:	
		newDislike = disLikes(dislike = True,
					post_id = post_id,
					handle = handle)
		db.session.add(newDislike) 
		db.session.commit()	
	resp = jsonify({"No dislike error": "disLike added successfully"})
	resp.status_code = 200
	return resp	

@app.route('/home')
@app.route('/home/')
@app.route('/home/<int:index>', methods = ['GET'])
def get_posts(index = 1):
	posts = returnJsonPostInfo(index)
	return posts	

@app.route('/sell', methods = ['GET'])
def get_s_releases():
	sale = returnJsonSellingInfo()
	return sale

@app.route('/buy', methods = ['GET'])
def get_b_releases():
	buy = returnJsonBuyingInfo()
	return buy

@app.route('/profile/<int:user_id>/<int:index>')
def get_profile_info(user_id = 0, index = 1):
	prof = returnJsonProfileInfo(user_id,index)
	return prof

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

@app.route('/m_releases')
def get_m_releases():
	data = returnJsonReleaseInfo()
	return data

@app.route('/m_releases/<int:release_id>/comments/<int:index>')
def get_comments(release_id = 0, index = 1):
	comments = returnJsonCommentsInfo(release_id, index)
	return comments

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
	print '---------------' + str(request.form['release_date'])
	release_date = time.strptime(request.form['release_date'], '%d-%m-%Y')
	dt = datetime.fromtimestamp(mktime(release_date))
	release_folder = 'releases/' + brand.replace(" ", "_") + "_" + model.replace(" ", "_") + "_" + datetime.now().strftime("%Y-%m-%d")
	path = os.path.join(UPLOAD_FOLDER, release_folder)
	mkdir_p(path)
	date_added = datetime.now()
	files = request.files.getlist("image_name")
	filename = ''

	newRelease = Releases(brand = brand,
					model = model,
					release_date = dt,
					price = request.form['price'],
					resell_value = request.form['resell_value'],
					gr = request.form['gr'],
					difficulty = request.form['difficulty'],
					release_folder = release_folder,
					text = request.form['text'],
					date_added = date_added,
					)

	db.session.add(newRelease)
	db.session.commit()

	return_release = Releases.query.filter_by(date_added = date_added).first()

	for file in files:
		print 'first file'
		name = release_folder
		filename = secure_filename(name)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], release_folder, filename))
		path = os.path.join(UPLOAD_FOLDER, '/releases', filename)
		newReleasePicture = ReleasePictures(url = path,
			release_id = return_release.id
			)

	db.session.add(newReleasePicture)
	db.session.commit()
	#release_id = Releases.query.order_by(Releases.id.desc()).first()
	#print request.files[]
	#print request.form


	resp = jsonify({"Release added successfully"})
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
							gr = addReleaseForm.gr.data,
							difficulty = addReleaseForm.difficulty.data,
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

	
