from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    user = request.form['username']
    password = request.form['password']
    return "<p>{} - {}</p>".format(user, password)


if __name__ == '__main__':
    app.run()
