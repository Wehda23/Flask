from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login.utils import login_required
from sqlalchemy.sql.functions import user
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,logout_user,current_user,login_required
auth = Blueprint('auth',__name__)

# Login Page/Function
@auth.route("/login/",methods =['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully!",category='success')
                login_user(user,remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect Password.",category='error')
        else:
            flash("Email does not exist.",category='error')
    return render_template("login.html",user=current_user)

# Logout Page/Function
@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Sign up Page/Function
@auth.route("/sign-up/",methods =['POST','GET'])
def sign_up():
    if request.method =='POST': 
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("This Email Already Exist.",category='error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters",category='error')
        elif len(first_name) < 2 :
            flash("First name must be greater than 1 characters",category='error')
        elif password1 != password2:
            flash("Password don\'t match",category='error')
        elif len(password1) < 7:
            flash("Password is weak at least 7 characters",category='error')
        else:
            new_user = User(email=email,first_name=first_name,password = generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!",category='success')
            login_user(user,remember=True)
            return redirect(url_for("views.home"))
            # add user to database
    return render_template("signup.html",user=current_user)


# LOGOUT FUCKERS ! 

