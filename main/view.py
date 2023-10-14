from main import view
from flask import (render_template, request, session, redirect)

from instance import MSQl

SQL = MSQl()


@view.route('/', methods=["GET", "POST"])
def index():
    """登陆"""
    userName = request.form.get("userName", None)
    password = request.form.get("password", None)
    if userName and password:
        if SQL.checkLogin(userName, password):
            session["user"] = userName
            return redirect('/user', 302)

    return render_template("login.html")


@view.route('/logup', methods=["GET", "POST"])
def logup():
    """注册"""
    print(request.form)
    userName = request.form.get("userName", None)
    password = request.form.get("password", None)
    print(userName, password)
    if userName and password:
        if SQL.insertUser(userName, password):
            return redirect('/', 302)
        else:
            return render_template("login.html")

    return render_template("logup.html")


@view.route('/user')
def manege():
    if session.get("user",None):
        info = SQL.showUserInfo()
        return render_template('user.html', users=info)
    else:
        return "You have been refused to visit here"


@view.route('/manage', methods=["POST"])
def manage():
    users = request.form.keys()
    for user in users:
        pw = request.form.get(user, None)
        SQL.changeUserInfo(user, pw)
    return redirect('/user', 302)
