import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Initialise app object
#
# Flask is a popular web framework that allows writing web servers
# in python. The 'app' object allows the framework to manage the app
# and run the correct code when processing a http request for example.
#
# Functions are attatched to urls using the @<example_blueprint>.route()
# decorator. This is how the framework knows what to run.
# Blueprints are mini-apps that allow a project to be devided up into smaller pieces.
# To work, they must be registered with the 'app' object, which is done below.
app = Flask(__name__)

# Configure Bcrypt manager,
# this attatches the bcrypt password hashing libary to the app.
bcrypt = Bcrypt(app)

# Load the secret key from environment variables.
# If the secret key can't be found, we presume were running in a devlopment
# environment and use the insecure key 'devkey'
if os.environ.get("FLASK_APP_SECRE_KEY"):
    app.secret_key = os.environ.get("FLASK_APP_SECRET_KEY")
else:
    app.secret_key = "devkey"

# Same as above, but this time with the URI for our database
if os.environ.get("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# This attaches the database manager to the app, this is needed as the database manager
# needs to be aware of the requests and current state of the server
db = SQLAlchemy(app)
from .models import User, Question

# Configure user management
# This uses flask_login to authenticate users and keep them signed in
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login.main_auth"


@login_manager.user_loader
def user_loader(user_id):  # Required for flask-login to be able to load a user from database
    return User.query.get(user_id)


# Register views and blueprints
#
# As discussed above, this loads the blueprints from all the smaller
# 'mini-apps' and registers them to the main app.
# This allows the project to be broken up into chunks
from .home.views import home_blueprint
from .login.views import login_blueprint
from .student.views import student_blueprint
from .teacher.views import teacher_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(student_blueprint)
app.register_blueprint(teacher_blueprint)
