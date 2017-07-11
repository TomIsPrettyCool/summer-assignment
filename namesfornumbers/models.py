"""
Models for the entire app, used to map Python objects onto
the database and do nice things like add helper methods.
"""
from . import db, bcrypt  # Get the database controller from the base app


class User(db.Model):
    """
    The base user model, used for auth and metadata.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(20))
    password = db.Column(db.LargeBinary())
    role = db.Column(db.String(10))

    # Flask login attributes
    is_authenticated = True
    is_active = True
    is_anonymous = False

    # Student attributes
    questions = db.relationship("Question", backref="student", lazy="dynamic")
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Teacher attributes
    students = db.relationship("User", backref="teacher", lazy="dynamic", 
                               remote_side=id, uselist=True)  # This somehow made a many-to-many relationship
                                                              # No idea why. 
    def __init__(self, name, username, password, role, teacher=None):
        self.name = name
        self.username = username
        self.password = self.create_password_hash(password)
        self.role = role

        if self.role == "student" and teacher:
            # Add to teacher
            self.teacher.id = teacher.id

    def get_id(self):
        """
        Required for flask-login
        """
        return str(self.id)

    def create_password_hash(self, password):
        return bcrypt.generate_password_hash(password)

    def check_password_hash(self, password):
        print(type(self.password))
        return bcrypt.check_password_hash(self.password, password)


class Question(db.Model):
    """
    Used to hold data about the induvidual questions asked.
    """
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.Integer)
    # Held as strings so anything can be thrown in.
    question_text = db.Column(db.String(80))
    question_answer = db.Column(db.Integer)
    correct = db.Column(db.Boolean)

    # Link back to the student
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, question_text, question_answer):
        self.question_type = 1
        self.question_text = question_text
        self.question_answer = question_answer

    @property
    def type_of_question(self):
        pass
