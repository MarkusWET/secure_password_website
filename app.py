from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as pgUUID, TEXT
import uuid
import hashlib

app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dbadmin@localhost:5432/secure_password_storage"
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = "users"

    # Fields
    user_id = db.Column("user_id", pgUUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4().hex)
    username = db.Column("username", TEXT, unique=True)
    usernumber = db.Column("usernumber", db.Integer, primary_key=True, autoincrement=True, unique=True)
    password = db.Column("password", TEXT)
    password_md5 = db.Column("password_md5", TEXT)
    password_pbkdf2 = db.Column("password_pbkdf2", TEXT)
    salt = db.Column("salt", TEXT)
    iterations = db.Column("iterations", db.Integer)

    # Methods
    def __init__(self, username, password, password_md5, password_pbkdf2, salt):
        self.username = username
        self.password = password
        self.password_md5 = password_md5
        self.password_pbkdf2 = password_pbkdf2
        self.salt = salt

    def __repr__(self):
        return "<User {}>".format(self.username)


def digest_password_md5(password):
    """takes a password and returns the md5 digest"""
    digester = hashlib.md5()
    digester.update(password.encode("utf-8"))
    return digester.hexdigest()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    user = Users.query.filter_by(username=request.form["username"]).first()

    if user is not None and user.password_md5 == digest_password_md5(request.form["password"]):
        return render_template("secret_page.html")
    else:
        return render_template("index.html", error_text="User and password do not match.")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]
    password_confirmation = request.form["password_confirmation"]

    if password == password_confirmation:
        password_digest = digest_password_md5(password)
        user = Users(username, None, password_digest, None, None)
        db.session.add(user)
        db.session.commit()

        return render_template("index.html", response_text="Your account has been created. You can now log in.")
    else:
        return render_template("register.html", error_text="Passwords do not match.")


if __name__ == "__main__":
    app.run()  # HTTP
    # app.run(ssl_context="adhoc")  # enable HTTPS with ssl_context
