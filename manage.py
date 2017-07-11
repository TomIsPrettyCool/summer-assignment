from namesfornumbers import app, User, db
from flask_script import Manager
from flask import url_for

manager = Manager(app=app)


@manager.command
def runserver():
    app.run(debug=True)


@manager.command
def adduser():
    new_user = User(
        input("name"),
        input("username"),
        input("password"),
        input("role")
    )
    if new_user.role == "student":
        if input("Add teacher? (n, Y)").lower() == "y":
            teacher_username = input("teacher_username:")
            teacher = User.query.filter_by(username=teacher_username).first()
            new_user.teacher = [teacher]

    db.session.add(new_user)
    db.session.commit()


@manager.command
def dropdb():
    db.drop_all()


@manager.command
def createdb():
    db.create_all()

@manager.command
def list_routes():
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


manager.run()