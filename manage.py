"""
This uses flask_script to create commands to manage the web app and database.

Only really used for debugging and for creating users.
"""
from namesfornumbers import app, User, db
from flask_script import Manager
from flask import url_for

manager = Manager(app=app)  # This creates a 'command manager' to make
                            # creating commands easier

@manager.command  # The use of a decorator creates a command using the manager
def runserver():
    app.run(debug=True)  # This runs the debug webserver - ONLY for development


@manager.command
def adduser():
    new_user = User(        # This creates a new 'User' object using the User.__init__() function.
        input("name"),      # This new_user is created as a database object through SQLAlchemy,
        input("username"),  # meaning it can be interacted with using normal python without touching SQL
        input("password"),
        input("role")
    )
    if new_user.role == "student":  # We want to be able to connect students and teachers
        if input("Add teacher? (n, Y)").lower() == "y":
            teacher_username = input("teacher_username:")
            teacher = User.query.filter_by(username=teacher_username).first()
            teacher.students.append(new_user)

    db.session.add(new_user)  # This adds the new user object to the database, so it knows it needs to be added
    db.session.commit()  # This commits all changes to the database, we only do this once as commiting to the
                         # database is expensive in terms of performance

@manager.command
def dropdb():
    """
    DELETES the database - use with care!
    """
    db.drop_all()


@manager.command
def createdb():
    """
    Creates the database
    """
    db.create_all()

@manager.command
def list_routes():
    """
    I didn't write this code, this was written by a nice person on
    stackoverflow.com 

    However, this was only used for debugging so I think its OK
    """
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote(
            "{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


# Run the command manager, this will run the correct function
manager.run()