from flask import request, render_template, flash, redirect, url_for
from flask import current_app as app
from .models import Profile
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(user_id):
    return Profile.query.get(user_id)


@app.route("/", methods=["GET", "POST"])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        return render_template("login.html")

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        profile = Profile.query.filter_by(name=username).first()
        
        if profile is None:
            flash('Invalid username')
            return render_template('login.html')
        elif not check_password_hash(profile.password, password):
            flash('Invalid password')
            return render_template('login.html')
        else:
            login_user(profile)
            return redirect(url_for("index"))


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        
        profile = Profile.query.filter_by(name=username).first()
        if profile:
            flash("Username already exists")
            return render_template("signup.html")

        if password != confirm_password:
            flash("Passwords do not match")
            return render_template("signup.html", username=username)
            
        profile = Profile(name=username, password=generate_password_hash(password, method="sha256"))

        db.session.add(profile)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            print("Rolling back")
        return redirect(url_for("login"))