# 📚 Summer Assignment 

This project contains the code for my 2017 summer assignemnt, it is a simple web app that can be run locally or on a server.

This is built upon Python 3.x (Tested on 3.5 and 3.6) and runs on [the Flask microframework](http://github.com/pallets/flask) on the backend and uses [materialize.css](https://github.com/Dogfalo/materialize) on the frontend.

## 🚀 Overview
![Screenshot](http://i.imgur.com/hXW8gK0.png)
Using the app, a student can take tests to see how good they are at converting cardinal numbers into integers. 
The teacher can then see the results of many students tests and get an average.

The app uses SQLAlchemy to communicate with a SQL database, this can be anything. By default it uses a SQLite3 database but this can be changed by setting the `DATABASE_URL` environment variable.

## 🏎️ Running
To running the app is simple-ish. You need virtualenv and python3 installed already

  *  First, clone the repository to get the code and enter the folder:  
  `git clone https://github.com/TomIsPrettyCool/summer-assignment.git && cd summer-assignment`

  *  Create the virtual environment and activate it:  
      ### Windows:
      * `virtualenv env`
      * `env\Scripts\activate`
      ### Actual OS's:
      * `virtualenv env`
      * `env/bin/activate`
  *  Install requirements: `pip install -r requirements.txt`
  *  Initialise the database `python manage.py createdb`
  *  Run the server `python manage.py runserver`
  *  Go to [127.0.0.1:5000](http://127.0.0.1:5000/) in your browser
