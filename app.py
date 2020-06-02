# import Flask and any libraries you want to use
from flask import Flask, request, jsonify, render_template, redirect, flash, session
# get db related stuff from models.py
from models import db, connect_db, User, Feedback
# get forms from forms.py
from forms import UserDetailsForm, LoginUserForm, FeedbackForm

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

    if "username" in session:
        return redirect(f'/users/{session["username"]}')

    form = UserDetailsForm()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_user = User.register(**data)

        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username
        flash("Welcome! Your account was successfully created!", "success")
        return redirect(f"/users/{new_user.username}")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """login User to site"""

    if "username" in session:
        return redirect(f'/users/{session["username"]}')

    form = LoginUserForm()
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        user = User.authenticate(**data)

        if user:
            flash(f"Welcome back {user.username}!", "success")
            session["username"] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username or password"]

    return render_template("login.html", form=form)

@app.route("/users/<username>")
def user_details(username):

    if "username" not in session:
        flash("Please log in first.", "info")
        return redirect("/login")

    
    user = User.query.filter_by(username=username).first()
    feedback = Feedback.query.filter_by(username=username)
    form = FeedbackForm(obj=user)
    return render_template("user_details.html", form=form, user=user, feedback=feedback)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    if "username" in session:
        user = User.query.filter_by(username=username).first()

        db.session.delete(user)
        db.session.commit()
        flash(f'{session["username"]} deleted.', "success")
        session.pop("username")
        return redirect("/")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def feedback_form(username):
    """Form for users to add feeback"""

    if "username" in session:
        user = User.query.filter_by(username=username).first()
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title, content=content, username=username)

            db.session.add(feedback)
            db.session.commit()
            flash("Feedback submitted!", "success")
            return redirect(f"/users/{user.username}")

    return render_template("feedback.html", form=form)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def feedback_details_form(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.add(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.user.username}")
    else:
        return render_template("feedback.html", form=form, feedback=feedback)


@app.route("/logout")
def logout():
    flash(f'Goodbye {session["username"]}', "success")
    session.pop("username")
    return redirect("/")