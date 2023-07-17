import sqlite3

from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g

menu = [{"url": ".index", "title": "Panel"},
        {"url": ".listpubs", "title": "listpubs"},
        {"url": ".listusers", "title": "listusers"},
        {"url": ".logout", "title": "Logoff"}]

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

db = None


@admin.before_request
def before_request():
    print("admin before_request")
    global db
    db = g.get("link_db")


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', title='Admin-panel', menu=menu)


@admin.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "123":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Probably. You are not an admin. If you even cant hack the password...", "error")
    return render_template('admin/login.html', title='Admin-panel', menu=menu)


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))

@admin.route('/listpubs')
def listpubs():
    print("@admin.route('/listpubs')", db)
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text FROM posts")
            list = cur.fetchall()
            print("list", list)
        except sqlite3.Error as e:
            print("Error with bd"+str(e))

    return render_template('admin/listpubs.html', title='list of articles', menu=menu, list = list)

@admin.route('/listusers')
def listusers():
    print("@admin.route('/listusers')", db)
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list = cur.fetchall()
            print("list")
            for p in list:
                print(p[0])
                print(p[1])
        except sqlite3.Error as e:
            print("Error with bd"+str(e))

    return render_template('admin/listusers.html', title='list of users', menu=menu, list = list)
