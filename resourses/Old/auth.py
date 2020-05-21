# from flask import make_response, jsonify
# import HTTPBasicAuth
# auth = HTTPBasicAuth()
#
# @auth.get_password
# def get_password(username):
#     if username == 'miguel':
#         return 'python'
#     return None
#
# @auth.error_handler
# def unauthorized():
#     return make_response(jsonify({'error': 'Unauthorized access'}), 401)

import functools
from resourses.Old import db
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import json


bp = Blueprint("auth", __name__, url_prefix="/auth")

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            db.Users.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        # db = get_db()
        error = None

        if not login:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
                db.Users.execute("SELECT id FROM user WHERE username = ?", (login,)).fetchone()
                is not None
        ):
            error = f"User {login} is already registered."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            db.Users.execute(
                "INSERT INTO user (login, password) VALUES (?, ?)",
                (login, generate_password_hash(password)),
            )
            db.Users.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    #return render_template("auth/register.html")
    return render_template("'index.html'")


def json_reader():
    with open("resourses/response.json") as f:
        user_data = (json.loads(f.read()).get("payload"))
    return user_data

@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        login = request.form["login"]
        password = request.form["password"]
        #db = get_db()
        error = None
        user = db.Users.execute(
            "SELECT * FROM user WHERE login = ?", (login,)
        ).fetchone()

        if user is None:
            print('1111111111111111111111111111111111111')
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            print('22222222222222222222222222222222222222')
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            print(user["id"])
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")
    #return render_template('from_us.html', body = json_reader())


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))