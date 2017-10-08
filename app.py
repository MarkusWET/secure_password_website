from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID as pgUUID, TEXT
import uuid
import os
import hashlib
import base64

app = Flask(__name__)
app.debug = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dbadmin@localhost:5432/secure_password_storage"
HASH_ALGORITHM = "sha256"
ITERATIONS = 100000
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
    def __init__(self, username, password, password_md5, password_pbkdf2, salt, iterations):
        self.username = username
        self.password = password
        self.password_md5 = password_md5
        self.password_pbkdf2 = password_pbkdf2
        self.salt = salt
        self.iterations = iterations

    def __repr__(self):
        return "<User {}>".format(self.username)


def digest_password_md5(password):
    """takes a password and returns the md5 digest"""
    digester = hashlib.md5()
    digester.update(password.encode("utf-8"))
    return digester.hexdigest()


def digest_password_pbkdf2(password, algo, salt, iterations):
    derived_key = hashlib.pbkdf2_hmac(hash_name=algo,
                                      password=str.encode(password),
                                      salt=salt,
                                      iterations=iterations)
    return base64.b64encode(derived_key)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    user = Users.query.filter_by(username=request.form["username"]).first()

    # Plaintext login
    # if user is not None and user.password == request.form["password"]:

    # MD5 login
    # if user is not None and user.password_md5 == digest_password_md5(request.form["password"]):

    # PBKDF2 login
    if user is not None:
        password = request.form["password"]
        salt = user.salt
        salt_b64_bytes = base64.b64decode(salt)
        iterations = user.iterations
        password_challenge = digest_password_pbkdf2(password, HASH_ALGORITHM, salt_b64_bytes, iterations)
        if user.password_pbkdf2.encode() == password_challenge:  # digest_password_pbkdf2(request.form["password"], HASH_ALGORITHM, base64.b64decode(user.salt), ITERATIONS):
            return render_template("secret_page.html")

    return render_template("index.html", error_text="User and password do not match.")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    username = request.form["username"]
    password = request.form["password"]
    password_confirmation = request.form["password_confirmation"]

    if password == password_confirmation:
        # Plaintext
        # user = Users(username, password, None, None, None)

        # MD5 hashed password
        # password_digest = digest_password_md5(password)
        # user = Users(username, None, password_digest, None, None)

        # PBKDF2 secure hashed and salted password
        salt = os.urandom(16)
        salt_b64 = base64.b64encode(salt).decode()  # salt bytes --> b64 bytes --> string

        password_digest_bytes = digest_password_pbkdf2(password,
                                                       HASH_ALGORITHM,
                                                       salt,
                                                       ITERATIONS)
        digest_string = password_digest_bytes.decode()
        user = Users(username, None, None, digest_string, salt_b64, ITERATIONS)
        db.session.add(user)
        db.session.commit()

        return render_template("index.html", response_text="Your account has been created. You can now log in.")
    else:
        return render_template("register.html", error_text="Passwords do not match.")


if __name__ == "__main__":
    app.run()  # HTTP
    # app.run(ssl_context="adhoc")  # enable HTTPS with ssl_context
