from flask import request, Response, Blueprint, json
from config.lang_config import langs
from config.languages import Lang_type
from models.Post import Post
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
        return Response(json.dumps({'success': False, 'err': 'Unsupported functions used.\nCannot use These Functions : '+ret}), mimetype="application/json", status=200)
    else:
        op = compile_and_run_code(lang, data['code'], data['ip'])
        if not op['success']:
            if op['timeout']:
                return Response(json.dumps({'success': False, 'err': 'Time out occured'}), mimetype="application/json", status=200)
            else:
                return Response(json.dumps({'success': False, 'err': 'Error '+op['err']}), mimetype="application/json", status=200)
        return Response(json.dumps({'success': True, 'output': op['output']}), mimetype="application/json", status=200)


@api.route('/api/test/<uuid:id>', methods=['POST'])
def test(id):
    data = request.form.to_dict()
    lang = langs[data['lang']]

    post = Post.objects(ID=id)[0].to_mongo()
    if any(bad in data['code'] for bad in lang.invalid):
        ret = ''
        for i in lang.invalid:
            ret += i
        return Response(json.dumps({'success': False, 'err': 'Unsupported functions used.\nCannot use These Functions : '+ret}), mimetype="application/json", status=200)
    else:
        op = compile_and_run_code(lang, data['code'], post['testcases'][0])
        if not op['success']:
            if op['timeout']:
                return Response(json.dumps({'success': False, 'err': 'Time out occured'}), mimetype="application/json", status=200)
            else:
                return Response(json.dumps({'success': False, 'err': 'Error '+op['err']}), mimetype="application/json", status=200)
        if op['output'] == post['outputs'][0]:
            return Response(json.dumps({'success': True, 'output': 'Test Case Passes' + op['output']}), mimetype="application/json", status=200)
        else:
            return Response(json.dumps({'success': False, 'err': 'Expected : '+post['outputs'][0]+' Got '+op['output']}), mimetype="application/json", status=200)

    #    return Response(json.dumps({'success': False, 'redirect': '/'}), mimetype="application/json", status=200)
