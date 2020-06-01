# import Flask and any libraries you want to use
from flask import Flask, request, jsonify, render_template, redirect, flash, session
# get db related stuff from models.py
from models import db, connect_db, User
# get forms from forms.py
from forms import RegisterUserForm, LoginUserForm

# instantiate and instance of Flask. app is standard name
app = Flask(__name__)

# specify which RDBMS you're using (i.e. postgresql) and name of DB you want app to use. "postgresql://ownername:yourpassword@localhost/databasename" OR "postgresql:///databasename"
# must do before you associate to your app or else it will error out
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
# remove track modifications warning at startup
app.config["SQLALCHEMY_TRACKMODIFICATIONS"] = False
# print all SQL statements to terminal (helpful in debugging and learning the ORM method calls)
app.config["SQLALCHEMY_ECHO"] = True

# connect to db
connect_db(app)

# import debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
# required by debugtoolbar for debugging session
app.config["SECRET_KEY"] = "secret"
# makes sure redirects aren't stopped by the debugtoolbar
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# instantiate class on our app
debug = DebugToolbarExtension(app)

@app.route("/")
def homepage():
    """homepage route. redirects to /register"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """register User for site"""

    form = RegisterUserForm()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_user = User.register(**data)

        db.session.add(new_user)
        db.session.commit()
        flash("Welcome! Your account was successfully created!")
        return redirect("/secret")
    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """login User to site"""

    form = LoginUserForm()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user = User.authenticate(**data)

        flash("Logged in!")
        return redirect("/secret")
    return render_template("login.html", form=form)

@app.route("/secret")
def secret_route():
    return render_template("secret.html")