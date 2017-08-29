from namesfornumbers import app, db, Question, User
from flask import Blueprint, render_template, abort
from flask_login import current_user, login_required
from functools import wraps

teacher_blueprint = Blueprint("teacher", __name__, url_prefix='/teacher')


@teacher_blueprint.route('/home/')
@login_required
@User.must_be_role("teacher")
def teacher_home():
    """
    Renders the default teacher home page
    """
    return render_template('common/home.html', active="home")


@teacher_blueprint.route('/results/')
@login_required
@User.must_be_role("teacher")
def results():
    """
    Renders the results of all the students.
    """
    students = current_user.students

    student_scores = {
    }  # {student: (<User:student>, [average1, average2, average3])}
    for student in students:
        student_scores[student.username] = (student, [])
        student_avg_list = student_scores[student.username][1]

        questions = student.questions.paginate(page=1, per_page=10)

        for x in questions.items:
            print(x.question_text)

        def get_average(questions):
            i = []
            for question in questions.items:
                if question.correct:
                    i.append(question)
            return len(i) * 10

        student_avg_list.append(get_average(questions))

        while questions.has_next and questions.page <= 3:
            questions = questions.next()
            student_avg_list.append(get_average(questions))

        average = sum(student_avg_list) / 3

    return render_template(
        'teacher/results.html',
        active='results',
        student_scores=student_scores,
        average=average)
