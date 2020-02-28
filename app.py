from flask import Flask, render_template
from config.lang_config import langs

from routes.api import api

app = Flask(__name__, static_folder='./static', static_url_path='/')


app.register_blueprint(api)


@app.route('/')
def home():
    return render_template('home.html', langs=langs)


app.run(host='0.0.0.0', port='8000',debug=True)
