"""
Placeholder for future homepage and redirect for
non-authed users
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

home_blueprint = Blueprint("home", __name__)


@home_blueprint.route('/')
@login_required
def home():
    if current_user.is_authenticated:
        if current_user.role == "teacher":
            return redirect(url_for("teacher.teacher_home"))
        elif current_user.role == "student":
            return redirect(url_for("student.student_home"))
    return "Something went wrong"
