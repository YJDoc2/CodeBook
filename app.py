from flask import Flask, render_template
from config.lang_config import langs
from flask_mongoengine import MongoEngine
from models.User import User
from routes.api import api
from routes.user import user
from routes.post import post
db = MongoEngine()

app = Flask(__name__, static_folder='./static', static_url_path='/')

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(user)
app.register_blueprint(post)

@app.route('/')
def homepage():
	return render_template('homepage.html')

@app.route('/compiler')
def compiler():
    return render_template('home.html', langs=langs)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/challenge')
def challenge():
    return render_template('challengeform.html', langs=langs)



app.run(host='0.0.0.0', port='5000', debug=True)
