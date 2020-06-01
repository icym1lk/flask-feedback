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

class User(db.Model):
    """model for individual User"""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key = True, unique = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        """Show info about User"""

        u = self
        return f"<username={u.username} email={u.email} first name={u.first_name} last name={u.last_name}>"