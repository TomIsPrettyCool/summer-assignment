"""
Models for the entire app, used to map Python objects onto
the database using SQLAlchemy.
"""
from . import db  # Get the database controller from the base app


class User(db.Model):
    """
    The base user model, used for auth and metadata.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(20))
    password = db.Column(db.LargeBinary())


class Student(User):
    """
    Student model, used to hold student specific data and methods
    """
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    questions = db.relationship("Question", backref="student", lazy="dynamic")
    teacher = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def previous_questions():
        pass


class Teacher(User):
    """
    Teacher model, used to hold teacher specific data and methods.
    """
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    students = db.relationship("Student", backref="teacher", lazy="dynamic")


class Question(db.Model):
    """
    Used to hold data about the induvidual questions asked.
    """
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.Integer)
    # Held as strings so anything can be thrown in.
    question_value = db.Column(db.String(80))
    question_answer = db.Column(db.String(80))
    correct = db.Column(db.Boolean)

    # Link back to the student
    student = db.Column(db.Integer, db.ForeignKey('student.id'))

    @property
    def type_of_question(self):
        pass
