"""Example flask app demonstrating cookies/sessions/g/auth."""

import os
import functools

from flask import Flask, request, render_template, redirect, url_for, make_response
from flask import session, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://localhost/authdemo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "abc1234")
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt()

toolbar = DebugToolbarExtension(app)


class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls, username, password):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).one()
        if user is not None:
            if bcrypt.check_password_hash(user.password, password):
                return user

        return False


###########################################################################
# Useful utilities


@app.before_request
def add_user_to_g():
    """If logged in, add logged-in user obj to g."""

    user_id = session.get("user_id")
    if user_id:
        user = User.query.get(user_id)
        if user is not None:
            g.user = user
        else:
            # couldn't find user -- perhaps user deleted from db?
            raise Exception(f"User #{user_id} missing")


def require_login(fn):
    """Decorator for a view function that requires logged-in user.

    If no logged in user, flashes msg & returns to login page.
    """

    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        if hasattr(g, 'user'):
            return fn(*args, **kwargs)
        else:
            flash("Not authorized.")
            return redirect(url_for("login"))

    return wrapped


###########################################################################
# Useful utilities


@app.route("/")
def index():
    """Show homepage with counter for # of visits."""

    # Get number-of-visits cookies & increment it (start at 1)

    if "n_visits" in request.cookies:
        n_visits = int(request.cookies['n_visits']) + 1
    else:
        n_visits = 1

    # Render homepage, attaching a cookie to the response

    html = render_template("index.html", n_visits=n_visits)
    response = make_response(html)
    response.set_cookie("n_visits", str(n_visits))
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.register(username, password)
        db.session.add(user)
        db.session.commit()
        flash("Registered.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.id
            flash("Logged in.")
            return redirect(url_for("index"))

        flash("Invalid login.")
        # fall through to login.html template

    return render_template("login.html")


@app.route('/logout', methods=['GET'])
def logout():
    """Handle logout & redirect to homepage."""

    if "user_id" in session:
        del session["user_id"]

    flash("Logged out.")
    return redirect(url_for("index"))


@app.route("/secret")
@require_login
def secret():
    """Secret page for logged-in members only."""

    print(f"SECURITY: {g.user.id} is visiting secret area!")

    return render_template("secret.html")
