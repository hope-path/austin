from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect

from src.common.database import Database

import src.models.users.errors as Usererror
from src.common.utils import Utils
from src.models.users import user
from src.models.alerts import alert

user_blueprint = Blueprint('users',__name__)
@user_blueprint.route('/login',methods = ['GET','POST'])
def login_user():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        if user.User.is_login_valid(email,password):
            session['email'] = email
            return redirect(url_for(".user_alerts"))


    return render_template("users/login.html")
@user_blueprint.route('/register',methods = ['GET','POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if user.User.registeruser(email,password):
            session['email']=email
            return redirect(url_for("alerts.index"))



    return render_template("users/register.html")
@user_blueprint.route('/alerts')
def user_alerts():
    User = user.User.find_by_email(session['email'])
    Alert = User.get_alerts()
    return render_template("users/alerts.html",alerts=Alert)
@user_blueprint.route('/logout')
def logout_user():
    session['email']= None
    return redirect(url_for("home"))

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
@user_blueprint.route('/home')
def home():
    render_template("home.html")
