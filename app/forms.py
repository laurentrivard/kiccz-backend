from flask.ext.wtf import Form
from wtforms.fields import TextField, BooleanField, SelectField, SubmitField, DateField, TextAreaField
from wtforms.validators import Required
from config import BRANDS
from werkzeug import secure_filename
from config import UPLOAD_FOLDER

class AddReleaseForm(Form):
	brand = SelectField('brand', choices = BRANDS, validators=[Required()])
	model = TextField('model', validators=[Required()])
	release_date = DateField('release_date', format="%m/%d/%Y")
	price = TextField('price', validators=[Required()])
	resell_value = TextField('resell_value', validators=[Required()])
	color1 = TextField('color1', validators=[Required()])
	color2 = TextField('color2', validators=[Required()])
	text = TextAreaField('text')
	#images are added separately
