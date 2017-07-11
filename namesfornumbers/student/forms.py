from flask_wtf import FlaskForm
from wtforms.fields import StringField

class AnswerForm(FlaskForm):
    answer = StringField("Answer")