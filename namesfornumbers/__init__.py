from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Register views and blueprints
from .home.views import home_blueprint
from .login.views import login_blueprint
from .student.views import student_blueprint
from .teacher.views import teacher_blueprint

# Initialise app object
app = Flask(__name__)

# Get database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Configure user management
login_manager = LoginManager()
login_manager.init_app(app)

from .models import Student, Teacher, Question

app.register_blueprint(home_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(student_blueprint)
app.register_blueprint(teacher_blueprint)
