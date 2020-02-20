from flask import Flask,render_template
from config import lang_config

from routes.api import api

app = Flask(__name__,static_folder='./static',static_url_path='/')


app.register_blueprint(api)

@app.route('/')
def home():
    return render_template('home.html',langs=lang_config.langs)
app.run()
