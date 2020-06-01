# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# intialize a variable for our db by running SQLAlchemy. db is standard name
db = SQLAlchemy()

# associate Flask app with our db
# don't want to connect to a db every single time you run your models file
# so we wrap it in a function and make it callable
def connect_db(app):
    """Connect to db"""
    db.app = app
    db.init_app(app)