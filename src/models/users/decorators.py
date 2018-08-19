from functools import wraps

from flask import session, redirect, url_for, request
import src.app

def requires_login(fun):
    @wraps(fun)
    def decorated_function(*args,**kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect (url_for('users.login_user',next=request.path))
        return fun(*args,**kwargs)
    return decorated_function

def requires_admin_permission(fun):
    @wraps(fun)
    def decorated_function(*args,**kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user',next=request.path))
        if session['email'] not in src.app.app.config['ADMINS']:
            return redirect(url_for('users.login_user'))
        return fun(*args,**kwargs)
    return decorated_function