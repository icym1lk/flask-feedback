# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# import bcrypt
from flask_bcrypt import Bcrypt

# intialize a variable for our db by running SQLAlchemy. db is standard name
db = SQLAlchemy()
# intialize bcrypt
bcrypt = Bcrypt()

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

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register username with hashed pwd & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # hashing results in bytestring.  this line turns that into a normal (unicode utf8) string for db storage.
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pw
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and pwd is correct"""

        u = User.query.filter_by(username=username).first()

        # check if u was found & that pwd given matches pwd in db
        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

    def __repr__(self):
        """Show info about User"""

        u = self
        return f"<username={u.username} email={u.email} first name={u.first_name} last name={u.last_name}>"