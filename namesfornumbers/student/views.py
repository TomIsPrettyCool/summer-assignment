from flask import Blueprint, render_template

student_blueprint = Blueprint("student", __name__, url_prefix='/student')

@student_blueprint.route('/home/')
def student_home():
    return render_template("common/home.html")