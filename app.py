from flask import Flask, render_template, redirect, Response, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from config import blacklist
from models.Post import Post
from config.lang_config import langs
from flask_mongoengine import MongoEngine
from models.User import User
from routes.api import api
from routes.user import user
from routes.post import post
import random

MAX_POSTS_GLOBAL_WALL = 100
MAX_POSTS_DASHBOARD = 100

db = MongoEngine()

app = Flask(__name__, static_folder='./static', static_url_path='/')
app.config['JWT_SECRET_KEY'] = '#OSTL@10@19@25@27#'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = True


jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(user)
app.register_blueprint(post)

@app.route('/')
def homepage():
	return render_template('homepage.html')

@jwt.invalid_token_loader
@jwt.unauthorized_loader
def invalid_token(reason):
    return redirect('/login')


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/compiler')
def compiler():
    return render_template('compiler.html', langs=langs)


@app.route('/dashboard')
@jwt_required
def dashboard():
    user = User.objects(username=get_jwt_identity())[0].to_mongo()
    posts = []
    for id in user['following']:
        u = User.objects(id=id)[0].to_mongo()
        for postid in u['posts']:
            p = Post.objects(ID=postid)[0].to_mongo()
            p['by'] = u['username']
            posts.append(p)

    random.shuffle(posts)
    return render_template('dashboard.html', logged_in=True, posts=posts[:MAX_POSTS_DASHBOARD])


@app.route('/challenge')
@jwt_required
def challenge():
    return render_template('challengeform.html', langs=langs, logged_in=True)


@app.route('/global')
@jwt_required
def globalwall():
    items = Post.objects(qtype='Global')
    items = [item.to_mongo() for item in items]
    items.reverse()
    return render_template('globalwall.html', posts=items[:MAX_POSTS_GLOBAL_WALL], logged_in=True)


@app.route('/find')
@jwt_required
def find_users():
    return render_template('findusers.html', logged_in=True)

@app.route('/solve')
#@jwt_required
def solve():
    return render_template('solve.html', langs=langs, logged_in=True)

app.run(host='0.0.0.0', port='5000', debug=True)
