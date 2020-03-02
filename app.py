from flask import Flask, render_template
from config.lang_config import langs
from flask_mongoengine import MongoEngine
from models.User import User
from routes.api import api
from routes.user import user

db = MongoEngine()

app = Flask(__name__, static_folder='./static', static_url_path='/')

db.init_app(app)

app.register_blueprint(api)
app.register_blueprint(user)


@app.route('/')
def home():
    return render_template('home.html', langs=langs)


app.run(host='0.0.0.0', port='8000', debug=True)
