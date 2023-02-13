from flask import render_template, request, flash, redirect, url_for
from web.models import User
from web import db
from flask_login import login_user, login_required, logout_user, current_user
from web.auth import bp
from web.auth.forms import LoginForm, SignupForm

#-----STARTING METRICS-----
from prometheus_client import (Counter,)

#Login counter
LOGIN_REQUESTS = Counter('login_requests_total', 'Total number of requests to login endpoint')
SIGNUP_REQUESTS = Counter('signup_requests_total', 'Total number of requests to signup endpoint')

#-----FINISHED METRICS-----

#Login view
@bp.route("/login", methods=["GET", "POST"])
def login():

    # Increment counter used for register the total number of calls in the login endpoint
    LOGIN_REQUESTS.inc()

    if current_user.is_authenticated:
        flash("You are already logged in.", category="error")
        return redirect(url_for("pastebins.home"))

    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            flash("Logged in successfully!", category="success")
            return redirect(url_for("pastebins.home"))
        else:
            flash("Wrong password.", category="error")

    return render_template("auth/login.html", user=current_user, form=form)

#Sign up view
@bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    # Increment counter used for register the total number of calls in the signup endpoint
    SIGNUP_REQUESTS.inc()

    form = SignupForm()

    if request.method == "POST" and form.validate_on_submit():
        new_user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash("Account successfully created!", category="success")
        return redirect(url_for("pastebins.home"))
            
    return render_template("auth/sign_up.html", user=current_user, form=form)

#Log out view
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
