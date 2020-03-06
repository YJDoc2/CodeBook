from flask import request, Response, Blueprint, json, session, render_template

from models.Post import Post
from config.lang_config import langs
post = Blueprint('post', __name__)


@post.route('/api/post', methods=['POST'])
def postChallenge():
    data = request.form.to_dict()
    data['testcases'] = json.loads(data['testcases'])
    #lang = langs[data.lang]
    # print(C.invalid)
    print(data)
    return Response(json.dumps({'Success': 'True'}), mimetype="application/json", status=201)
    # if data['code'] in lang.invalid:
    #     return Response(json.dumps({'Success': 'False'}), mimetype="application/json", status=404)

    # else:

    #     temp = Post(originalPostBy=data['originalPostBy'],
    #                 question=data['question'], code=data['code'])
    #     # testcases=data['testcases'], outputs=data['outputs'])
    #     # temp.save()
    #     return Response(json.dumps({'Success': 'True'}), mimetype="application/json", status=201)
