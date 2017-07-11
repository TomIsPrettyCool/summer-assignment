# Names for summers, summer assignment.
Summer assignment for A-Level

This project is my summer assignment for a-level. It is a simple web application based on the Flask framework designed to test children on
converting from Cardinal form to numbers.

e.g `two thousand -> 2000`

#### It is also designed to be run locally, and as such uses a sqlite3 database and automatically opens a web-browser

## Running
```
pip3 install -r requirements.txt  # Install requirements
python manage.py createdb  # Create the database
python manage.py adduser   # Add users to the database - you will need to do this to start
python manage.py runserver  # Take a guess
```