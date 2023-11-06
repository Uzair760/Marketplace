from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

class PostListing(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    desc = TextAreaField('Description')
    price = StringField('Price', validators=[DataRequired()])
    item_picture = FileField('Add an Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post Listing')
