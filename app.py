from flask import Flask

app = Flask(__name__)

@app.route('/')
def home_page():
    return f'<p>/user/create/(username) to create a user</p>'

@app.route('/user/create/<string:username>')
def create_user(username):
    return f'<p>creating user {username}</p>'

@app.route('/user/validate/<string:username>')
def validate_user(username):
    return f'<p>validating user {username}</p>'

