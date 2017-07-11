from namesfornumbers import app, User, db
from flask_script import Manager

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


manager.run()