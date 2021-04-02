from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class MovieTitleForm(FlaskForm):
	movie_title = StringField('Movie Title', validators=[DataRequired(), Length(min=2, max=150)])
	submit = SubmitField('Recommend Now')
