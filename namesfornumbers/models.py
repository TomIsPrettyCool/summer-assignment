"""
Models for the entire app, used to map Python objects onto
the database and do nice things like add helper methods.
"""
from . import db, bcrypt  # Get the database controller from the base app
from flask import abort
from flask_login import current_user
from functools import wraps


class User(db.Model):
    """
    The base user model, used for auth and metadata.
    """
    id = db.Column(db.Integer, primary_key=True)  # All rows need a primary key
    name = db.Column(db.String(80))  # The name of the student
    username = db.Column(db.String(20))  # Username, should be uniqie
    password = db.Column(db.LargeBinary())  # Passwords are encrypted so should be stored as binary
    role = db.Column(db.String(10))  # Role, e.g. 'STU' = student

    # Flask login attributes
    is_authenticated = True     # These are needed so the app can check if a user is logged in
    is_active = True            # By calling User.is_authenticated, we can check that the user
    is_anonymous = False        # is logged in. More info: https://flask-login.readthedocs.io

    # Student attributes
    questions = db.relationship("Question", backref="student", lazy="dynamic")  # Create a relationship between students and questions

    # Teacher attributes
    students = db.relationship("User", backref="teacher", lazy="dynamic", 
                               remote_side=[id], uselist=True)  # This somehow made a many-to-many relationship
                                                              # No idea why. 
    def __init__(self, name, username, password, role, teacher=None):
        """
        Initialise the User object with required values
        """
        self.name = name
        self.username = username
        self.password = self.create_password_hash(password)  # Assigns hashed value as password
        self.role = role
        
    def get_id(self):
        """
        Required for flask-login
        """
        return str(self.id)

    def create_password_hash(self, password):
        """
        Uses the bcrypt libary to generate a secure password hash
        """
        return bcrypt.generate_password_hash(password)

    def check_password_hash(self, password):
        """
        Checks the password matches the hash
        """
        return bcrypt.check_password_hash(self.password, password)
    
    @staticmethod
    def must_be_role(role):
        def must_be_role_decorator(func):  # Check that the current user is actually a student
            @wraps(func)  # Use built-in boilerplate code
            def role_checker(*args, **kwargs):
                if current_user.role != role:
                    return abort(403)
                else:
                    return func(*args, **kwargs)  # If all fine, execute function anyway

            return role_checker
        return must_be_role_decorator


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
