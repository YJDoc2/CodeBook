from flask import request, Response, Blueprint, json
from config.lang_config import langs
from config.languages import Lang_type
from util.compile import compile_and_run_code


api = Blueprint('api', __name__)


@api.route('/api/compile', methods=['POST'])
def handle():
    data = request.form.to_dict()
    lang = langs[data['lang']]
    if any(bad in data['code'] for bad in lang.invalid):
        ret = ''
        for i in lang.invalid:
            ret += i
        return Response(json.dumps({'Success': False, 'err': 'Unsupported functions used.\nCannot use These Functions : '+ret}), mimetype="application/json", status=200)
    else:
        op = compile_and_run_code(lang, data['code'], data['ip'])
        if not op['success']:
            if op['timeout']:
                return Response(json.dumps({'Success': False, 'err': 'Time out occured'}), mimetype="application/json", status=200)
            else:
                return Response(json.dumps({'Success': False, 'err': 'Error '+op['err']}), mimetype="application/json", status=200)
        return Response(json.dumps({'Success': True, 'output': op['output']}), mimetype="application/json", status=200)
