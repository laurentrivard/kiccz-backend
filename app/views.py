from flask import render_template, request, flash, redirect, url_for, jsonify
from app import app, db
from models import User, Releases, Votes, ReleasePictures, ROLE_USER
from forms import AddReleaseForm
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug import secure_filename
import os, errno, datetime

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
	print releases[0].id
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


@app.route('/m_releases')
def get_m_releases():
	data = returnJsonReleaseInfo()
	return data	
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

@app.route('/add_release', methods = ['GET', 'POST'])
def add_release():
	addReleaseForm = AddReleaseForm()
	#if form was submitted
	if addReleaseForm.validate_on_submit():
		brand = addReleaseForm.brand.data
		model = addReleaseForm.model.data
		date = addReleaseForm.release_date.data
		#create a subfolder to uplaod pictures of the specifc release
		release_folder = 'releases/' + brand.replace(" ", "_") + "_" + model.replace(" ", "_") + "_" + datetime.datetime.now().strftime("%Y-%m-%d")
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
							date_added = datetime.datetime.now())
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

	if user == None:
		user = User(facebook_id = user_id,
					name = name,
					handle = handle,
					role = ROLE_USER
					)
		db.session.add(user)
		db.session.commit()
	else:
		m_login()	

	return_user = User.query.filter_by(facebook_id = user_id).first()
	new_user = {}
	new_user['user_id'] = return_user.id
	new_user['handle'] = return_user.handle
	new_user['name'] = return_user.name

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
	   resp = jsonify(new_user)
	   resp.status_code = 200
	   return resp	