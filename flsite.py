import sqlite3, os
from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from admin.admin import admin
from FdataBase import FdataBase
from UserLogin import UserLogin

# Config
# DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = "gggggghhhhh"
MAX_CONTETNT_LENGHT = 1024 * 1024 * 1024
SQLALCHEMY_DATABASE_URI = 'sqlite:///flsite.db'

app = Flask(__name__)
app.config.from_object(__name__)
# app.config['SECRET_KEY'] = SECRET_KEY
app.config.update(dict(DATABASE=os.path.join(app.root_path, "flsite.db")))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flsite.db'

# app.permanent_session_lifetime = 1
app.register_blueprint(admin, url_prefix="/admin")
al = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "To see the content you need to be login"
login_manager.login_message_category = "success"
fdb = None
menu = [{"name": "Login", "url": "login"},
        {"name": "First application", "url": "first-app"},
        {"name": "Add html", "url": "addHtml"},
        {"name": "Contacts", "url": "contact"}]


class users(al.Model):
    id = al.Column(al.Integer, primary_key=True)
    name = al.Column(al.String(50), nullable=True)
    email = al.Column(al.String(50), unique=True)
    psw = al.Column(al.String(2000), nullable=True)
    date = al.Column(al.DateTime, default=datetime.utcnow)
    avatar = al.Column(al.LargeBinary, default=None)

    pr = al.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"user  {self.id, self.email, self.date}"


class Profiles(al.Model):
    id = al.Column(al.Integer, primary_key=True)
    name = al.Column(al.String(50), nullable=True)
    age = al.Column(al.Integer)
    city = al.Column(al.String(150))

    user_id = al.Column(al.Integer, al.ForeignKey('users.id'))

    def __repr__(self):
        return f"profile  {self.id, self.name, self.age, self.city}"


def insert_blob(title, url):
    try:
        sqlite_connection = connect_db()
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_blob_query = """INSERT INTO mainmenu
                                        (title, url) VALUES (?, ?)"""

        data_tuple = (title, url)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблиу")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def read_db():
    table = "users"
    results = {}
    conn = sqlite3.connect(app.config["DATABASE"])
    cursor = conn.cursor()

    raw = "id"
    request = f"SELECT {raw} FROM {table} ORDER BY id"
    cursor.execute(request)
    ids = cursor.fetchall()

    raw = "name"
    request = f"SELECT {raw} FROM {table} ORDER BY id"
    cursor.execute(request)
    title = cursor.fetchall()

    raw = "email"
    request = f"SELECT {raw} FROM {table} ORDER BY id"
    cursor.execute(request)
    text = cursor.fetchall()

    raw = "psw"
    request = f"SELECT {raw} FROM {table} ORDER BY id"
    cursor.execute(request)
    url = cursor.fetchall()

    conn.close()

    for i in range(len(ids)):
        # results[ids[i][0]] = (title[i][0], url[i][0], text[i][0])
        print(ids[i][0], title[i][0], url[i][0], text[i][0])
    # print(results)

    return results


def deleteRecord(id):
    try:
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.cursor()

        table = "users"
        sql_delete_query = f"""DELETE from {table} where id = """ + str(id)
        cursor.execute(sql_delete_query)
        conn.commit()
        print(f"Record {id} deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete record from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")


def drop_table():
    try:
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.cursor()

        table = "users"
        sql_delete_query = f"""DROP TABLE {table} """
        cursor.execute(sql_delete_query)
        conn.commit()
        print(f"Table {table} deleted successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to delete table from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource("sq_db.sql", mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
        return g.link_db


@login_manager.user_loader
def load_user(user_id):
    print("load_user", user_id)
    return UserLogin().fromDB(user_id, fdb)


@app.teardown_appcontext
def close_db(error):
    # fdb.close()
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/index")
@app.route("/")
def index():
    print(url_for("index"))
    return render_template("index.html", menu=fdb.getMenu(), posts=fdb.getPostsAnince(), html=fdb.getPostsAnonce())


@app.route("/about")
def about():
    print(url_for("about"))
    return render_template("about.html", title=url_for("about") + ") site about v2", menu=fdb.getMenu())


@app.route("/visits")
def visits_f():
    session.permanent = True
    if "visits" in session:
        # session["visits"] = session.get("visits") + 1
        session["visits"] += 2
        session.modified = True
    else:
        session["visits"] = 1
    return f'visits on this page: {session.get("visits")} '


@app.route("/make_response_png")
def make_png_test():
    img = None
    with app.open_resource(app.root_path + "/static/Images/Por_troll/Pornhub.png", mode="rb") as f:
        img = f.read()
        if img is None:
            return "None image"
    res = make_response(img, 500)
    res.headers["Content-Type"] = "image/png"
    res.headers["Server"] = "flasksite"
    return res


@app.route("/make_response")
def make_resp_test():
    content = render_template("about.html", title=url_for("make_resp_test") + ") site about v2", menu=fdb.getMenu())
    res = make_response(content, 500)
    res.headers["Content-Type"] = "text/plain"
    res.headers["Server"] = "flasksite"
    return res


@app.route("/make_response_as_list")
def make_resp_list():
    return (render_template("about.html", title=url_for("make_resp_list") + ") site about v2", menu=fdb.getMenu()), 501,
            {"Content-Type": "text/html"})


@app.route("/transfer")
def transfer_fn():
    return redirect(url_for("index"), 302)


@app.route("/logout")
def logout():
    print(url_for("logout"))
    logout_user()
    print('You have logout successfully')
    flash("You have logout successfully", category='success')
    return redirect(url_for("login"))


@app.route("/profile")
@login_required
def profile():
    print(url_for("profile"))
    return render_template("profile.html", menu=fdb.getMenu(), title="profile")


@app.route("/userava")
@login_required
def userava():
    print(url_for("userava"))
    img = current_user.getAvatar(app)
    print(type(img))
    if not img:
        return ""
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    print(url_for("upload"))
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = fdb.updateUserAvatar(img, current_user.get_id())
                if not res:
                    print("Cannot update avatar error")
                    flash("Cannot update avatar", "error")
                print("Avatar is updated success")
                flash("Avatar is updated", 'success')
            except FileNotFoundError as e:
                print("Cannot read the file error " + str(e))
                flash("Cannot read the file", "error")
        else:
            print("Cannot update avatar error")
            flash("Cannot update avatar", "error")
    return redirect(url_for('profile'))


@app.route("/Html/<alias>")
def showHtml(alias):
    title, post = fdb.getHtml(alias)
    if not title:
        abort(404)
    return render_template("htmlShow.html", title=title, post=post)


@app.route("/post/<int:id_post>")
def showPost(id_post):
    title, post = fdb.getPost(id_post)
    if not title:
        abort(404)

    return render_template("post.html", title=title, post=post)


@app.route("/contact", methods=["POST", "GET"])
def contact():
    print(url_for("contact"))
    if request.method == 'POST':
        print(request.form["username"])
        if len(request.form["username"]) > 2:
            flash("Massage sent", category="success")
        else:
            flash("Error of sending", category="error")

    return render_template("contact.html", title=url_for("contact") + ") contact", menu=fdb.getMenu())


@app.route("/login_old", methods=["POST", "GET"])
def login_old():
    print(url_for("login_old"))
    if 'userLog' in session:
        return redirect(url_for("profile", username=session["userLog"]))
    elif request.method == "POST" and request.form["username"] == "ARX" and request.form["psw"] == "123":
        session['userLog'] = request.form["username"]
        return redirect(url_for("profile", username=session["userLog"]))

    return render_template("login.html", title="Authorization", menu=fdb.getMenu())


@app.route("/login", methods=["POST", "GET"])
def login():
    print(url_for("login"))
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = fdb.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))

        flash("Paswor or login is INCORRECT", category='error')
        flash("You shall not pass", category='error')
        print("Paswor or login is INCORRECT")
    return render_template("login.html", menu=fdb.getMenu(), title="Authorization", form=form)

@app.route("/users")
def Users_rote():
    print(url_for("Users_rote"))
    info = []
    try:
        info = users.query.all()
    except:
        print("Error in bd")
    return render_template("users.html", title="Users", list=info)


@app.route("/register", methods=["POST", "GET"])
def register():
    print(url_for("register"))
    form = RegisterForm()
    if form.validate_on_submit():
        # phash = generate_password_hash(form.psw.data)
        # res = fdb.addUser(form.name.data, form.email.data, phash)
        prof = addProfile(form)
        if prof:
            print('You have registered successfully')
            flash("You have registered successfully", category='success')
            return redirect(url_for("login"))
        else:
            print('error:  add in bd register')
            flash("error: add in bd", category='error')

    return render_template("register.html", title="Authorization", menu=fdb.getMenu(), form=form)


def addProfile(form):
    print("addProfile")
    try:
        phash = generate_password_hash(form.psw.data)
        u = users(name=form.name.data, email=form.email.data, psw=phash)
        al.session.add(u)
        al.session.flush()

        p = Profiles(name=form.name.data, age=form.age.data, city=form.city.data, user_id=u.id)
        al.session.add(p)
        al.session.commit()
    except sqlite3.Error as e:
        print("error addProfile  " + str(e))
        al.session.rollback()
        print("error in bd addProfile")
        return False
    return True


@app.route("/login_2")
def login_2():
    print(url_for("login_2"))
    log = ""
    if request.cookies.get("logged"):
        log = request.cookies.get("logged")
    content = f"<h1> Authorization form<h1><p>loged: {log}"
    res = make_response(content, 500)
    res.set_cookie("logged", "Yes", 30)
    res.headers["Server"] = "flasksite"
    return res


@app.route("/logout_2")
def logout_2():
    print(url_for("login_2"))
    content = f"<h1> You NOT Authorized anymore,               GOD DAY SIR <h1>"
    res = make_response(content, 500)
    res.set_cookie("logged", "", 0)
    res.headers["Server"] = "flasksite"
    return res


@app.route("/add_post", methods=["POST", "GET"])
@login_required
def addPost():
    print(url_for("addPost"))
    if request.method == 'POST':
        print("if request.method == 'POST'")
        if len(request.form["name"]) > 2 and len(request.form["post"]) > 2:
            print('if len(request.form["name"]) > 2')
            res = fdb.addPost(request.form["name"], request.form["post"])
            if not res:
                print("if not res")
                flash("error adding the post", category='error')
            else:
                print("if not res is False")
                flash("Massage sent successfully", category="success")

    return render_template("add_post.html", title=url_for("contact") + "add post", menu=fdb.getMenu())


@app.route("/addHtml", methods=["POST", "GET"])
@login_required
def addHtml():
    print(url_for("addHtml"))
    if request.method == 'POST':
        print("if request.method == 'POST'")
        if len(request.form["name"]) > 2 and len(request.form["post"]) > 2 and len(request.form["url"]) > 2:
            print('if len(request.form["name"]) > 2')
            res = fdb.addHTML(request.form["name"], request.form["post"], request.form["url"])
            if not res:
                print("if not res")
                flash("error adding the post", category='error')
            else:
                print("if not res is False")
                flash("Massage sent successfully", category="success")

    return render_template("addHtml.html", title="addHtml", menu=fdb.getMenu())


# @app.before_first_request
# def before_first_request_my():
#     print("before_first_request_my")


@app.before_request
def before_request_my():
    print("before_request_my")
    global fdb
    db = get_db()
    fdb = FdataBase(db)


@app.after_request
def after_request_my(response):
    # fdb.close_db()
    # print("after_request_my  ", response)
    return response


@app.teardown_request
def teardown_request_my(response):
    # print("teardown_request_my  ", response)
    return response


@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html", title="pageNotFound", menu=fdb.getMenu()), 404


if __name__ == '__main__':
    app.run(debug=DEBUG)
