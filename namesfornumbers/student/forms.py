from flask_wtf import FlaskForm
from wtforms.fields import IntegerField
from wtforms.validators import DataRequired

class AnswerForm(FlaskForm):
    """
    Uses the 'FlaskForm' object to create a python object that can be rendered
    into a secure HTML form to get the answer to the question from the user
    """
    answer = IntegerField("answer", validators=[DataRequired()])