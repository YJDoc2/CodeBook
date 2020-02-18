from flask import Flask

from routes.api import api

app = Flask(__name__,static_folder='./static',static_url_path='/')


app.register_blueprint(api)
app.run()
