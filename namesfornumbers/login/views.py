from namesfornumbers.models import User
from .forms import LoginForm
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

login_blueprint = Blueprint("login", __name__, url_prefix='/auth')


@login_blueprint.route('/', methods=["GET", "POST"])
def main_auth():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user and user.check_password_hash(login_form.password.data):
            login_user(user)
            return redirect(url_for('home.home'))
        else:
            flash("Username or password incorrect")

    return render_template(
        'auth/login.html', login_form=login_form, no_side_nav=True)

@login_blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login.main_auth"))