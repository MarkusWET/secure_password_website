from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as pgUUID, TEXT
import uuid

app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dbadmin@localhost:5432/secure_password_storage"
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"

    # Fields
    user_id = db.Column("user_id", pgUUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    username = db.Column("username", TEXT, unique=True)
    usernumber = db.Column("usernumber", db.Integer, primary_key=True)
    password = db.Column("password", TEXT)
    password_md5 = db.Column("password_md5", TEXT)
    password_pbkdf2 = db.Column("password_pbkdf2", TEXT)
    salt = db.Column("salt", TEXT)
    iterations = db.Column("iterations", db.Integer)

    # Methods
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.username)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    user_entered = request.form["username"]
    password_entered = request.form["password"]

    user = Users.query.filter_by(username=user_entered).first_or_404()

    if user.password == password_entered:
        return render_template("secret_page.html")
    else:
        return render_template("error.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]
    password_confirmation = request.form["password_confirmation"]

    if password == password_confirmation:
        user = Users(username, password)
        db.session.add(user)
        db.session.commit()

        print("REGISTERING WITH DATA: {}:{} ({})".format(username, password, password_confirmation))
        return render_template("success.html")
    else:
        return render_template("error.html")


if __name__ == "__main__":
    app.run()  # HTTP
    # app.run(ssl_context="adhoc")  # enable HTTPS with ssl_context
