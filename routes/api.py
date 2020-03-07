from flask import request, Response, Blueprint, json
from config.lang_config import langs
from config.languages import Lang_type


api = Blueprint('api', __name__)


@api.route('/api', methods=['POST'])
def handle():
    form = request.form.to_dict()
    try:
        lang = langs[form['lang']]
    except:
        return Response(json.dumps({'res': 'Form Not found'}), mimetype="application/json", status=400)
