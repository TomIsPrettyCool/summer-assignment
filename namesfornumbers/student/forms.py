from flask_wtf import FlaskForm
from wtforms.fields import IntegerField
from wtforms.validators import DataRequired

class AnswerForm(FlaskForm):
    answer = IntegerField("answer", validators=[DataRequired()])