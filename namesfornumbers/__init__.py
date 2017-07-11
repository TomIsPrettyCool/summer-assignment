import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialise app object
app = Flask(__name__)

# Configure Bcrypt manager
bcrypt = Bcrypt(app)

# Get database
if os.environ.get("FLASK_APP_SECRE_KEY"):
    app.secret_key = os.environ.get("FLASK_APP_SECRE_KEY")
else:
    app.secret_key = "devkey"

if os.environ.get("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
from .models import User, Question

# Configure user management
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login.main_auth"


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


# Register views and blueprints
from .home.views import home_blueprint
from .login.views import login_blueprint
from .student.views import student_blueprint
from .teacher.views import teacher_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(student_blueprint)
app.register_blueprint(teacher_blueprint)
