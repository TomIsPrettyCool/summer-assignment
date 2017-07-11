from .forms import AnswerForm
from .utils import generate_question
from namesfornumbers import db, app, Question
from flask import Blueprint, render_template, session, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from itsdangerous import Serializer
from functools import wraps

student_blueprint = Blueprint("student", __name__, url_prefix='/student')

s = Serializer(app.secret_key)


def must_be_student(func):  # Check that the current user is actually a student
    @wraps(func)  # Use built-in boilerplate code
    def mustbestudent(*args, **kwargs):
        if current_user.role != "student":
            return abort(401)
        else:
            return func(*args,
                        **kwargs)  # If all fine, execute function anyway

    return mustbestudent


@student_blueprint.route('/home/')
@login_required
@must_be_student
def student_home():
    return render_template("common/home.html")


@student_blueprint.route('/test/', methods=["GET", "POST"])
@login_required
@must_be_student
def test():
    answer_form = AnswerForm()
    if "test" in session:
        test_data = session["test"]

        if test_data["question_count"] == 10:
            session.pop("test")
            return redirect(url_for("student.results"))

        if answer_form.validate_on_submit():
            question_id = test_data.get("question_id")
            answer = Question.query.get(question_id)

            if answer.question_answer == answer_form.answer.data:
                # Whoop! Correct answer for question
                answer.correct = True
                flash("Correct!")
                test_data["correct_count"] += 1
            else:
                answer.correct = False
                flash("Wrong")

            number, words = generate_question()

            next_question = Question(words, number)
            db.session.add(answer)
            db.session.add(next_question)

            db.session.commit()

            test_data["question_count"] += 1

            return render_template(
                "student/test.html",
                active="test",
                question=next_question,
                answer_form=answer_form)
    else:
        test_data = {
            "question_count": 0,
            "question_id": 0,
            "correct_count": 0
        }

        flash("start?")

        

    return render_template("student/test.html", active="test")