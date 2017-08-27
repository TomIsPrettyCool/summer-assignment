from .forms import AnswerForm
from .utils import generate_and_add_question
from namesfornumbers import db, app, Question
from flask import Blueprint, render_template, session, abort, flash, redirect, url_for, request
from flask_login import login_required, current_user
from itsdangerous import Serializer
from functools import wraps
from sqlalchemy import desc

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
    return render_template("common/home.html", active="home")


@student_blueprint.route('/test/', methods=["GET", "POST"])
@login_required
@must_be_student
def test():
    """
    Not proud of this - needs to be refractored, probaly
    into a few different endpoints
    """
    answer_form = AnswerForm()
    if "test" in session:
        test_data = session["test"]

        if test_data["question_count"] == 10:
            unused_question = Question.query.get(int(test_data["question_id"]))
            db.session.delete(unused_question)
            db.session.commit()  # Delete unused record

            session.pop("test")
            return redirect(url_for("student.results", jumbo=True))

        print("attempting to validate...")
        if answer_form.validate_on_submit():

            question_id = int(test_data.get("question_id"))
            answer = Question.query.get(question_id)

            if answer.question_answer == answer_form.answer.data:
                # Whoop! Correct answer for question
                answer.correct = True
                flash("Correct!")
                test_data["correct_count"] += 1

            else:
                answer.correct = False
                flash("Wrong")

            db.session.add(answer)

            next_question = generate_and_add_question()

            db.session.commit()

            test_data["question_id"] = next_question.id
            test_data["question_count"] += 1  # increment question number

            session["test"] = test_data
            return render_template(
                "student/test.html",
                active="test",
                question=next_question,
                answer_form=answer_form,
                test_data=test_data)

        else:
            print('attempting again')
            question = Question.query.get(int(session["test"]["question_id"]))

            if not question:
                question = generate_and_add_question()
                db.session.commit()

                test_data["question_id"] = question.id

            session["test"] = test_data
            return render_template(
                "student/test.html",
                active="test",
                question=question,
                answer_form=answer_form)

    else:
        if request.args.get("start") == "true":
            test_data = {
                "question_count": 1,
                "question_id": 0,
                "correct_count": 0
            }

            session["test"] = test_data
            return redirect(url_for("student.test"))

        return render_template(
            "student/test.html", active="test", pretest=True)


@student_blueprint.route('/results/')
@login_required
@must_be_student
def results():
    completed_questions = current_user.questions.order_by(desc(Question.id)).limit(10)
    all_questions = current_user.questions.order_by(desc(Question.id)).limit(100)

    def decimal_correct(completed_questions):
        amount_correct = 0
        for question in completed_questions:
            print(question.correct)
            if question.correct:
                amount_correct += 1
        return amount_correct

    percent_correct = decimal_correct(completed_questions) * 10
    jumbo = request.args.get('jumbo')
    
    return render_template(
        'student/results.html',
        active="results",
        percent_correct=percent_correct,
        all_questions=all_questions,
        jumbo=jumbo)
